# Growth — onboarding contextualizado

Use eventos para selecionar um próximo passo e preparar uma comunicação. A unidade é conta, e todas as contas fictícias têm sete dias completos de observação.

O fluxo combina segmentação por regras e redação assistida. As mensagens são rascunhos; não haverá envio externo neste exercício.

## Estado do projeto

Atividade guiada com dados fictícios, prompt, exemplos de referência e critérios de revisão. Você pode estudar os exemplos sem conta de IA ou experimentar o prompt em um assistente ao qual já tenha acesso. Aplicativo próprio e integração automática não fazem parte do escopo desta fase. As respostas esperadas abaixo são referências didáticas, não execuções de IA registradas.

## Como experimentar

1. Abra [os dados fictícios](#dados-fictícios).
2. Copie o prompt abaixo junto dos dados fictícios para um assistente de texto ao qual tenha acesso, ou examine manualmente o exercício.
3. Compare a resposta com a referência e os critérios abaixo.
4. Registre a alteração feita, o resultado e os erros encontrados.

## Prompt

```text
Prepare um rascunho para C04: integração concluída, pedido válido disponível e nenhuma primeira resposta revisada nos sete dias observados.
Oriente abrir o pedido, preparar um rascunho e conferir status, fonte e prazo antes da revisão.
Até 70 palavras, uma ação principal. Não presuma motivo de não uso, prometa economia ou invente links.
Não envie. Entregue rascunho e itens para conferir.
```

## Dados fictícios

```json
[
  {
    "conta": "C01",
    "integracao": 1,
    "pedido": 1,
    "resposta_revisada": 1
  },
  {
    "conta": "C02",
    "integracao": 1,
    "pedido": 1,
    "resposta_revisada": 1
  },
  {
    "conta": "C03",
    "integracao": 1,
    "pedido": 1,
    "resposta_revisada": 1
  },
  {
    "conta": "C04",
    "integracao": 1,
    "pedido": 1,
    "resposta_revisada": 0
  },
  {
    "conta": "C05",
    "integracao": 1,
    "pedido": 1,
    "resposta_revisada": 0
  },
  {
    "conta": "C06",
    "integracao": 1,
    "pedido": 0,
    "resposta_revisada": 0
  },
  {
    "conta": "C07",
    "integracao": 1,
    "pedido": 0,
    "resposta_revisada": 0
  },
  {
    "conta": "C08",
    "integracao": 0,
    "pedido": 0,
    "resposta_revisada": 0
  },
  {
    "conta": "C09",
    "integracao": 0,
    "pedido": 0,
    "resposta_revisada": 0
  },
  {
    "conta": "C10",
    "integracao": 0,
    "pedido": 0,
    "resposta_revisada": 0
  }
]
```

## Resultado esperado e revisão

Há 7/10 contas com integração, 5/10 com pedido e 3/10 com primeira revisão. A ativação definida pelo exercício é 30%; entre as contas com pedido, a taxa de revisão é 60%. Regras: se revisou, ativada; senão, sem integração → configuração; sem pedido → primeiro pedido; demais → primeira revisão. Segmentos: 3, 3, 2 e 2 contas.

- Unidade, janela e denominador estão explícitos?
- A segmentação segue as regras sem inferir motivação?
- O próximo passo é compatível com o estado da conta?
- Melhoria posterior não foi atribuída à IA sem comparação adequada?

## Adaptação ao projeto

Escreva uma hipótese de experimento com comparação, janela, métrica principal e uma medida de proteção de qualidade.

## Saiba mais

- [NNG — proposta de valor](https://www.nngroup.com/articles/powered-by-ai-is-not-a-value-proposition/)
- [Kohavi et al. — experimentação](https://exp-platform.com/large-scale/)

Referências públicas consultadas em 13/11/2026. Exemplos e perguntas autorais de Laura Napoles, com apoio de Ada.

[Voltar ao início](../README.md)
