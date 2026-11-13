# Build & Ship — assistente de políticas

Especifique um assistente que consulta políticas fictícias e prepara um rascunho com referências. A exploração manual ajuda a entender RAG: recuperar informação antes de gerar uma resposta.

A aplicação com recuperação automática ainda será implementada. Selecionar trechos manualmente neste exercício não é executar uma busca vetorial.

## Estado do projeto

Guia de exploração, dados e prompt disponíveis. Integração com modelo e aplicação interativa ainda em desenvolvimento. Respostas esperadas abaixo são referências didáticas, não execuções de IA registradas.

## Como experimentar

1. Abra [os dados fictícios](#dados-fictícios).
2. Copie o prompt abaixo junto dos dados fictícios para um assistente de texto ao qual tenha acesso, ou examine manualmente o exercício.
3. Compare a resposta com a referência e os critérios abaixo.
4. Registre a alteração feita, o resultado e os erros encontrados.

## Prompt

```text
Prepare um rascunho usando apenas os documentos D01–D03.
Pergunta: Recebi duas caixas avariadas. Posso trocar imediatamente?
Entregue: rascunho; fontes; informação ausente; próximo passo.
Preserve condições e limites. Não invente prazo, status ou aprovação.
Não execute ações nem envie mensagens. Cite todas as fontes que sustentam sua resposta.
```

## Dados fictícios

```json
[
  {
    "id": "D01",
    "titulo": "Consulta de pedidos",
    "texto": "Esta política não contém dados de pedidos específicos. Status e previsão devem ser consultados no sistema operacional. Não prometer data sem previsão confirmada."
  },
  {
    "id": "D02",
    "titulo": "Avaria",
    "texto": "Para abrir análise, registrar pedido, itens afetados, descrição e fotos quando disponíveis. O registro não representa aprovação de troca ou reembolso."
  },
  {
    "id": "D03",
    "titulo": "Encaminhamento",
    "texto": "Quando faltar informação ou houver divergência, encaminhar à equipe responsável. O operador revisa o rascunho antes de enviar. Não há prazo de retorno definido."
  }
]
```

## Resultado esperado e revisão

A resposta deve orientar o registro para análise (D02), sem aprovar troca imediata, e preservar a revisão do operador (D03). Para “o pedido 1042 chega amanhã?”, deve indicar a necessidade de consulta operacional (D01), sem inventar data.

- A resposta distingue abertura de análise e aprovação?
- Cada afirmação está sustentada pelo documento citado?
- Perguntas sem dado recebem uma explicação da lacuna?
- O sistema não alega ter enviado ou alterado algo?

## Adaptação ao projeto

Teste uma pergunta fora do escopo e escreva o comportamento esperado antes de executar o prompt.

## Saiba mais

- [Lewis et al. — artigo de RAG](https://arxiv.org/abs/2005.11401)
- [Anthropic — workflows e agentes](https://www.anthropic.com/research/building-effective-agents)
- [Hugging Face — ferramentas](https://huggingface.co/learn/agents-course/unit1/tools)

Referências públicas consultadas em 13/11/2026. Exemplos e perguntas autorais de Laura Napoles, com apoio de Ada.

[Voltar ao início](../README.md)
