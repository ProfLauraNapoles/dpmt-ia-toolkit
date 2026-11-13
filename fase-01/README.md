# Land — comparação de mercado com fontes

Investigue quais capacidades aparecem em três recortes de fornecedores fictícios. O objetivo é produzir uma comparação rastreável e perguntas para investigar depois.

Você aprenderá a distinguir uma fonte fornecida ao modelo de uma pesquisa na internet, e uma hipótese de uma evidência. A ferramenta `preparar_prompt.py`, na raiz, monta o contexto deste exemplo.

## Estado do projeto

Aplicação interativa disponível com organização literal sem IA e integração opcional por API. Veja o **[guia de instalação e uso](../GUIA-LAND.md)**. Quinze testes automatizados aprovados; integração testada com respostas simuladas. A chamada com conta real ainda está pendente. [Registro de testes](../TESTES-LAND.md).

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
Proponha duas hipóteses, identificadas como hipóteses.
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

Alfa menciona caixa compartilhada (M01); Beta, consulta a pedidos via ERP (M02); Gama, rascunhos com revisão (M03). Informações não mencionadas devem permanecer como lacunas. Uma hipótese possível é investigar se aproximar conversa e pedido reduz alternância entre sistemas; os cartões não comprovam esse benefício.

- Cada afirmação tem uma fonte que realmente a sustenta?
- Ausência de menção permaneceu diferente de ausência de funcionalidade?
- As hipóteses foram separadas das capacidades documentadas?

## Adaptação ao projeto

Acrescente um cartão fictício com informação incompleta e revise se a comparação preserva a lacuna.

## Saiba mais

- [MDN — como a web funciona](https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Web_standards/How_the_web_works)
- [Google — modelos de linguagem](https://developers.google.com/machine-learning/crash-course/llm)
- [Artificial Analysis — metodologia](https://artificialanalysis.ai/methodology/)

Referências públicas consultadas em 13/11/2026. Exemplos e perguntas autorais de Laura Napoles, com apoio de Ada.

[Voltar ao início](../README.md)
