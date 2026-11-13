# Learn & Iterate — análise e avaliação

Confira cálculos e compare interpretações antes de recomendar uma evolução. O contexto didático se relaciona ao desafio Moinho, mas os dados abaixo são inteiramente fictícios.

A unidade é empresa, a janela comum é de 60 dias e as etapas são acumuladas. Os segmentos A/B não representam setores reais. O exercício não substitui a análise das bases e a pesquisa do desafio.

## Estado do projeto

Guia de exploração, dados e prompt disponíveis. Integração com modelo e aplicação interativa ainda em desenvolvimento. Respostas esperadas abaixo são referências didáticas, não execuções de IA registradas.

## Como experimentar

1. Abra [os dados fictícios](#dados-fictícios).
2. Copie o prompt abaixo junto dos dados fictícios para um assistente de texto ao qual tenha acesso, ou examine manualmente o exercício.
3. Compare a resposta com a referência e os critérios abaixo.
4. Registre a alteração feita, o resultado e os erros encontrados.

## Prompt

```text
Analise a tabela fictícia, com unidade empresa e janela comum de 60 dias.
Liste numerador, denominador e fórmula das taxas. Separe observações, hipóteses, informações ausentes e próximas perguntas.
Não conclua causalidade, significância estatística ou desempenho futuro.
Não escolha uma solução de IA ou dashboard sem justificar a necessidade.
```

## Dados fictícios

```json
[
  {
    "segmento": "A",
    "contatadas": 10,
    "reunioes": 7,
    "propostas": 4,
    "contratos": 2
  },
  {
    "segmento": "B",
    "contatadas": 10,
    "reunioes": 5,
    "propostas": 4,
    "contratos": 1
  }
]
```

## Resultado esperado e revisão

Totais: 20 contatadas, 12 reuniões, 8 propostas, 3 contratos. Taxas: 60% reunião/contato; aproximadamente 66,7% proposta/reunião; 37,5% contrato/proposta; 15% contrato/contato. A teve dois contratos e B um: isso não demonstra superioridade causal. “A conversão geral é 37,5% e a IA elevará contratos em 40%” troca o denominador e inventa uma projeção.

- Cálculos, unidades e períodos estão corretos?
- A fonte sustenta cada observação?
- Hipóteses foram diferenciadas de resultados?
- A recomendação responde a uma lacuna real?

## Adaptação ao projeto

Compare duas análises com uma rubrica de correção numérica, fidelidade, limites e próximo passo. Para custo, distinga horas liberadas de benefício financeiro realizado.

## Saiba mais

- [Product Talk — avaliação de IA](https://www.producttalk.org/ai-evals/)
- [FinOps — custo e valor por unidade](https://www.finops.org/framework/capabilities/unit-economics/)

Referências públicas consultadas em 13/11/2026. Exemplos e perguntas autorais de Laura Napoles, com apoio de Ada.

[Voltar ao início](../README.md)
