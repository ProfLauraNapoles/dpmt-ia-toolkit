# Land — comparação de mercado com fontes

Investigue quais capacidades aparecem em três recortes de fornecedores fictícios. O objetivo é produzir uma comparação rastreável e perguntas para investigar depois.

Você aprenderá a distinguir uma fonte fornecida ao modelo de uma pesquisa na internet, e uma hipótese de uma evidência. A ferramenta `preparar_prompt.py`, na raiz, monta o contexto deste exemplo.

## Estado do projeto

Aplicação interativa disponível com organização literal sem IA e integração opcional por API. Veja o **[guia de instalação e uso](../GUIA-LAND.md)**. Uma primeira resposta real foi observada com os três cartões fictícios. O bloco de hipóteses foi aprimorado depois: perguntas separadas, plano de teste e critério de refutação. Vinte testes automatizados aprovados; a geração real com o novo formato ainda precisa ser conferida. [Registro de testes](../TESTES-LAND.md).

As respostas esperadas abaixo continuam sendo referências didáticas, não execuções de IA registradas.

## Como experimentar

1. Abra [os dados fictícios](#dados-fictícios).
2. Copie o prompt abaixo junto dos dados fictícios para um assistente de texto ao qual tenha acesso, ou examine manualmente o exercício.
3. Compare a resposta com a referência e os critérios abaixo.
4. Registre a alteração feita, o resultado e os erros encontrados.

## Prompt

```text
Compare somente os cartões M01, M02 e M03 fornecidos. Eles são fictícios.
Pergunta: quais capacidades de atendimento e operação estão mencionadas e quais dúvidas merecem pesquisa posterior?
Entregue: fornecedor | capacidade mencionada | ID da fonte | informação ausente.
Separe até três perguntas de pesquisa para preencher lacunas, com IDs das fontes.
Proponha até três hipóteses testáveis, identificadas como não validadas.
Para cada hipótese, escreva o efeito esperado, as fontes que motivam a ideia,
como testar (comparação/observação e medida) e qual resultado a enfraqueceria.
As fontes não comprovam a hipótese. Não apresente perguntas ou tarefas de pesquisa
como hipóteses nem invente metas numéricas. Se faltarem elementos, não force uma hipótese.
Não converta ausência de menção em ausência de funcionalidade.
Não invente preços, clientes, participação de mercado ou indicadores.
```

## Dados fictícios

```json
[
  {
    "id": "M01",
    "fornecedor": "Alfa",
    "trecho": "Caixa de entrada compartilhada e distribuição de conversas entre atendentes. O trecho não menciona integração com pedidos nem preço."
  },
  {
    "id": "M02",
    "fornecedor": "Beta",
    "trecho": "Consulta a pedidos por integração com ERP. O trecho não descreve caixa de entrada compartilhada nem informa tempo de implantação."
  },
  {
    "id": "M03",
    "fornecedor": "Gama",
    "trecho": "Geração de rascunhos de resposta com revisão humana. O trecho não informa as bases utilizadas nem taxa de acerto."
  }
]
```

## Resultado esperado e revisão

Alfa menciona caixa compartilhada (M01); Beta, consulta a pedidos via ERP (M02); Gama, rascunhos com revisão (M03). Informações não mencionadas devem permanecer como lacunas. Uma pergunta de pesquisa é “Quais ERPs são compatíveis?”. Uma hipótese não validada seria “Consultar pedidos dentro do atendimento reduz o tempo de resposta”. Para testá-la, compare tempo e correção em tarefas equivalentes com e sem integração. Tempo igual ou maior, ou piora na correção, enfraqueceriam a hipótese. Os cartões não comprovam esse benefício; o teste é uma proposta, não uma pesquisa realizada.

- Cada afirmação tem uma fonte que realmente a sustenta?
- Ausência de menção permaneceu diferente de ausência de funcionalidade?
- Perguntas de pesquisa e hipóteses foram separadas das capacidades documentadas?
- Cada hipótese expressa um efeito observável, uma forma de teste e um resultado que a enfraqueceria?

## Adaptação ao projeto

Acrescente um cartão fictício com informação incompleta e revise se a comparação preserva a lacuna.

## Saiba mais

- [MDN — como a web funciona](https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Web_standards/How_the_web_works)
- [Google — modelos de linguagem](https://developers.google.com/machine-learning/crash-course/llm)
- [Artificial Analysis — metodologia](https://artificialanalysis.ai/methodology/)

Referências públicas consultadas em 13/11/2026. Exemplos e perguntas autorais de Laura Napoles, com apoio de Ada.

[Voltar ao início](../README.md)
