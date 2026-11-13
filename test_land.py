"""Testes sem rede: regras, contrato da API e tratamento de respostas."""
import copy
import io
import json
from pathlib import Path
import unittest
from unittest.mock import Mock
from urllib import error
import land_core as land

CARDS = json.loads(Path(__file__).with_name('dados-land.json').read_text())
QUESTION = land.DEFAULT_QUESTION


def research_result(cards=CARDS):
    """Resposta didática, não gerada por IA nem resultado de pesquisa real."""
    result = land.organize_offline(QUESTION, cards)
    result['perguntas_pesquisa'] = [{'pergunta': 'Quais ERPs são compatíveis?', 'fontes': ['M02']}]
    result['hipoteses'] = [{
        'hipotese': 'Consultar pedidos no atendimento reduz o tempo de resposta.',
        'fontes': ['M02'],
        'como_testar': 'Comparar tempo e correção das respostas em tarefas equivalentes com e sem integração.',
        'o_que_enfraquece': 'Tempo igual ou maior, ou piora na correção das respostas.',
    }]
    return result


def completed(result):
    return {'status': 'completed', 'output': [
        {'type': 'reasoning', 'summary': []},
        {'type': 'message', 'role': 'assistant', 'content': [
            {'type': 'output_text', 'text': json.dumps(result)}]}],
        'usage': {'input_tokens': 400, 'output_tokens': 200, 'total_tokens': 600}}


class LandTests(unittest.TestCase):
    def setUp(self):
        self.cards = copy.deepcopy(CARDS)
        self.result = land.organize_offline(QUESTION, self.cards)

    def test_input_limits_and_duplicate_ids(self):
        for question, cards in [('', CARDS), ('x'*1001, CARDS), (QUESTION, []),
                                (QUESTION, [None]), (QUESTION, [CARDS[0]]*2),
                                (QUESTION, [{'id':'M01','fornecedor':'Alfa','trecho':''}])]:
            with self.subTest(question=question[:10], cards=cards):
                with self.assertRaises(land.LandError):
                    land.validate_inputs(question, cards)

    def test_normalization_and_offline_edits(self):
        self.cards[0]['trecho'] = '  Novo recorte fictício.  '
        question, cards = land.validate_inputs(' Questão? ', self.cards)
        self.assertEqual(question, 'Questão?')
        result = land.organize_offline(question, cards)
        self.assertEqual(result['comparacao'][0]['evidencia'], 'Novo recorte fictício.')
        self.assertEqual(result['hipoteses'], [])
        self.assertIn('Novo recorte fictício.', land.build_prompt(question, cards))
        self.assertNotEqual(land.fingerprint(question, cards, 'ia'), land.fingerprint(question, cards, 'offline'))

    def test_rejects_unknown_repeated_and_missing_sources(self):
        for mutation in ('unknown', 'repeated', 'missing'):
            result = copy.deepcopy(self.result)
            if mutation == 'missing':
                result['comparacao'].pop()
            else:
                result['comparacao'][1]['fonte_id'] = 'X99' if mutation == 'unknown' else 'M01'
            with self.subTest(mutation=mutation), self.assertRaises(land.LandError):
                land.validate_result(result, self.cards)

    def test_quotes_must_exist_but_semantics_need_human_review(self):
        self.result['comparacao'][0]['evidencia'] = 'Preço: R$ 1.'
        with self.assertRaises(land.LandError):
            land.validate_result(self.result, self.cards)
        self.result['comparacao'][0]['evidencia'] = 'Caixa de entrada\n compartilhada'
        self.result['comparacao'][0]['afirmacao'] = 'Afirmação deliberadamente não sustentada.'
        # Este teste registra o limite: a presença literal não prova a interpretação.
        self.assertEqual(land.validate_result(self.result, self.cards), self.result)

    def test_invalid_hypothesis_reference_and_missing_limits(self):
        bad_hypothesis = research_result()['hipoteses'][0]
        bad_hypothesis['fontes'] = ['X99']
        for field, value in [('hipoteses', [bad_hypothesis]), ('limites', []), ('comparacao', 'texto livre')]:
            result = copy.deepcopy(self.result)
            result[field] = value
            with self.subTest(field=field), self.assertRaises(land.LandError):
                land.validate_result(result, self.cards)

    def test_research_questions_and_testable_hypotheses_contract(self):
        result = research_result()
        self.assertEqual(land.parse_response(completed(result), self.cards), result)
        # Rejeita versões antigas/incompletas, campos em branco e referências inválidas.
        for section, field, value in [
            ('hipoteses', 'como_testar', None), ('hipoteses', 'o_que_enfraquece', ''),
            ('hipoteses', 'fontes', []), ('hipoteses', 'fontes', ['M02', 'M02']),
            ('perguntas_pesquisa', 'pergunta', ' '), ('perguntas_pesquisa', 'fontes', ['X99']),
            ('perguntas_pesquisa', 'fontes', []),
        ]:
            invalid = copy.deepcopy(result)
            if value is None:
                del invalid[section][0][field]
            else:
                invalid[section][0][field] = value
            with self.subTest(section=section, field=field, value=value), self.assertRaises(land.LandError):
                land.validate_result(invalid, self.cards)
        for section in ('hipoteses', 'perguntas_pesquisa'):
            invalid = copy.deepcopy(result)
            invalid[section] *= 4
            with self.subTest(section=section), self.assertRaises(land.LandError):
                land.validate_result(invalid, self.cards)
        # O sistema aceita a decisão de não propor hipóteses; não as fabrica por regra.
        result['hipoteses'] = []
        self.assertEqual(land.validate_result(result, self.cards), result)

    def test_export_preserves_research_and_test_plan(self):
        result = research_result()
        review = {'hipoteses_separadas': True, 'testes_revisados': True, 'anotacao': 'Teste ainda não realizado.'}
        exported = json.loads(json.dumps(land.report(QUESTION, self.cards, 'ia', 'modelo-de-teste', result, {}, review)))
        self.assertEqual(exported['versao'], 2)
        self.assertEqual(exported['resultado'], result)
        self.assertEqual(exported['revisao_humana'], review)

    def test_schema_and_terminal_prompt_match_the_app(self):
        from preparar_prompt import montar_prompt
        self.assertEqual(montar_prompt(self.cards), land.build_prompt(QUESTION, self.cards))
        schema = land.make_payload(QUESTION, self.cards, 'modelo-de-teste')['text']['format']['schema']
        self.assertIn('perguntas_pesquisa', schema['required'])
        hypothesis_schema = schema['properties']['hipoteses']['items']
        self.assertEqual(set(hypothesis_schema['required']), {'hipotese', 'fontes', 'como_testar', 'o_que_enfraquece'})
        self.assertFalse(hypothesis_schema['additionalProperties'])

    def test_responses_protocol_and_usage_without_network(self):
        transport = Mock(return_value=io.BytesIO(json.dumps(completed(self.result)).encode()))
        result, usage = land.call_model(QUESTION, self.cards, 'modelo-de-teste', 'credencial-ficticia', transport)
        self.assertEqual(result, self.result)
        self.assertEqual(usage['total_tokens'], 600)
        transport.assert_called_once()
        req = transport.call_args.args[0]
        self.assertEqual(req.full_url, land.API_URL)
        self.assertEqual(transport.call_args.kwargs['timeout'], 45)
        self.assertEqual(req.get_header('Authorization'), 'Bearer credencial-ficticia')
        payload = json.loads(req.data)
        self.assertFalse(payload['store'])
        self.assertTrue(payload['text']['format']['strict'])
        branches = payload['text']['format']['schema']['properties']['comparacao']['items']['anyOf']
        self.assertEqual([b['properties']['fonte_id']['enum'] for b in branches], [['M01'], ['M02'], ['M03']])
        self.assertEqual(json.loads(payload['input'])['fontes'][0]['trecho'], self.cards[0]['trecho'])
        self.assertNotIn('credencial-ficticia', req.data.decode())

    def test_allowed_quotes_are_literal_and_bound_to_their_source(self):
        self.cards[0]['trecho'] = 'Integração com ERP: "Ação".\nNão informa preço!  Consulte a fonte.'
        schema = land.make_payload(QUESTION, self.cards, 'modelo-de-teste')['text']['format']['schema']
        branches = schema['properties']['comparacao']['items']['anyOf']
        for branch, card in zip(branches, self.cards):
            props = branch['properties']
            self.assertEqual(props['fonte_id']['enum'], [card['id']])
            self.assertIn(card['trecho'], props['evidencia']['enum'])
            self.assertTrue(all(q and q in card['trecho'] for q in props['evidencia']['enum']))
            for quote in props['evidencia']['enum']:
                result = land.organize_offline(QUESTION, self.cards)
                row = next(r for r in result['comparacao'] if r['fonte_id'] == card['id'])
                row['evidencia'] = quote
                self.assertEqual(land.parse_response(completed(result), self.cards), result)
        self.assertNotIn(self.cards[1]['trecho'], branches[0]['properties']['evidencia']['enum'])
        dense = 'X. ' * 600
        options = land.citation_options(dense)
        self.assertLessEqual(len(options), 13)
        self.assertIn(dense, options)

    def test_nonliteral_or_wrong_source_quotes_still_fail_without_retry(self):
        for quote in ['Caixa compartilhada entre atendentes.',
                      'Caixa de entrada compartilhada…',
                      CARDS[1]['trecho']]:
            result = research_result()
            result['comparacao'][0]['evidencia'] = quote
            transport = Mock(return_value=io.BytesIO(json.dumps(completed(result)).encode()))
            with self.subTest(quote=quote), self.assertRaisesRegex(land.LandError, 'fonte M01'):
                land.call_model(QUESTION, CARDS, 'modelo-de-teste', 'credencial-ficticia', transport)
            transport.assert_called_once()

    def test_refusal_incomplete_and_malformed_response(self):
        bodies = [{'status':'incomplete'}, {'status':'completed','output':[]},
                  {'status':'completed','output':[{'type':'message','content':[
                      {'type':'refusal','refusal':'Não posso.'}]}]},
                  {'status':'completed','output':[{'type':'message','content':'errado'}]}]
        for body in bodies:
            with self.subTest(body=body), self.assertRaises(land.LandError):
                land.parse_response(body, self.cards)

    def test_safe_http_and_connection_errors_without_retry(self):
        failures = [error.HTTPError(land.API_URL, code, 'credencial-ficticia', {}, None)
                    for code in (400, 401, 403, 429, 500)]
        failures += [error.URLError('credencial-ficticia'), TimeoutError('credencial-ficticia')]
        for failure in failures:
            transport = Mock(side_effect=failure)
            with self.subTest(failure=type(failure).__name__), self.assertRaises(land.LandError) as ctx:
                land.call_model(QUESTION, self.cards, 'modelo-de-teste', 'credencial-ficticia', transport)
            transport.assert_called_once()
            self.assertNotIn('credencial-ficticia', str(ctx.exception))

    def test_unreadable_response_and_excessive_size(self):
        for raw in (b'<html>error</html>', b'\xff', b'x'*2_000_001):
            with self.subTest(size=len(raw)), self.assertRaises(land.LandError):
                land.call_model(QUESTION, self.cards, 'modelo-de-teste', 'credencial-ficticia',
                                Mock(return_value=io.BytesIO(raw)))

    def test_invalid_inputs_do_not_contact_service(self):
        for question, model, key in [('', 'modelo', 'fake'), (QUESTION, 'bad model', 'fake'),
                                    (QUESTION, 'modelo', 'fake\nkey')]:
            transport = Mock()
            with self.subTest(model=model), self.assertRaises(land.LandError):
                land.call_model(question, self.cards, model, key, transport)
            transport.assert_not_called()

    def test_export_is_explicit_and_offline_has_no_model(self):
        result = land.report(QUESTION, self.cards, 'offline', 'modelo', self.result, {}, {'anotacao':'Revisar'})
        self.assertIsNone(result['modelo'])
        self.assertNotIn('api_key', result)
        self.assertEqual(result['revisao_humana']['anotacao'], 'Revisar')
        self.assertEqual(result['fontes'], self.cards)


if __name__ == '__main__':
    unittest.main()
