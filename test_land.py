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
        for field, value in [('hipoteses', [{'hipotese':'Investigar integração','fontes':['X99']}]),
                             ('limites', []), ('comparacao', 'texto livre')]:
            result = copy.deepcopy(self.result)
            result[field] = value
            with self.subTest(field=field), self.assertRaises(land.LandError):
                land.validate_result(result, self.cards)

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
        self.assertEqual(payload['text']['format']['schema']['properties']['comparacao']['items']['properties']['fonte_id']['enum'], ['M01','M02','M03'])
        self.assertEqual(json.loads(payload['input'])['fontes'][0]['trecho'], self.cards[0]['trecho'])
        self.assertNotIn('credencial-ficticia', req.data.decode())

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
