# Discover — síntese rastreável de entrevistas

Organize temas em seis registros fictícios e volte às falas para conferir a interpretação. O objetivo é apoiar a pesquisa e a decisão de MVP, preservando contradições.

Estes personagens não são participantes reais. Usar o exercício não substitui a pesquisa do seu projeto.

## Estado do projeto

Guia de exploração, dados e prompt disponíveis. Integração com modelo e aplicação interativa ainda em desenvolvimento. Respostas esperadas abaixo são referências didáticas, não execuções de IA registradas.

## Como experimentar

1. Abra [os dados fictícios](#dados-fictícios).
2. Copie o prompt abaixo junto dos dados fictícios para um assistente de texto ao qual tenha acesso, ou examine manualmente o exercício.
3. Compare a resposta com a referência e os critérios abaixo.
4. Registre a alteração feita, o resultado e os erros encontrados.

## Prompt

```text
Analise somente os registros fictícios E01–E06.
Decisão: que obstáculo investigar antes de definir o MVP de atendimento a pedidos?
Para até quatro temas, informe IDs, pequenos trechos literais, interpretação, contraponto e próxima pergunta de pesquisa.
Não invente falas ou porcentagens. Não confunda confirmação de recebimento com mudança de prazo.
Não conclua que uma solução foi validada. Preserve diferenças entre papéis.
```

## Dados fictícios

```json
[
  {
    "id": "E01",
    "papel": "Atendente",
    "fala": "Abro o ERP e depois mando mensagem para o estoque. Se o ERP está atualizado, respondo sem dificuldade."
  },
  {
    "id": "E02",
    "papel": "Supervisora",
    "fala": "Aceitaria um rascunho, mas o atendente precisa conferir o prazo antes de enviar."
  },
  {
    "id": "E03",
    "papel": "Atendente",
    "fala": "O texto é fácil. O que demora é descobrir se a mercadoria já foi separada."
  },
  {
    "id": "E04",
    "papel": "Integração",
    "fala": "A situação é atualizada a cada hora. Algumas contas menores não têm integração configurada."
  },
  {
    "id": "E05",
    "papel": "Compradora",
    "fala": "Só aprovo se mostrarmos menos retrabalho. Ainda não medimos quantas consultas são refeitas."
  },
  {
    "id": "E06",
    "papel": "Atendente",
    "fala": "Confirmar recebimento da mensagem pode ser automático. Para mudar prazo, quero falar com a operação."
  }
]
```

## Resultado esperado e revisão

E01/E03/E04 sugerem investigar acesso e atualização da informação. E02/E06 diferenciam níveis de automação e revisão. E05 indica uma lacuna de medição. A frase “todos querem resposta automática e o retrabalho cairá 40%” é deliberadamente inadequada: contradiz registros e inventa um resultado.

- Os IDs e trechos existem nos dados?
- A interpretação respeita contrapontos e papéis?
- Frequência no exercício não foi tratada como prevalência no mercado?

## Adaptação ao projeto

Revise a frase inadequada e formule uma pergunta que possa mudar a escolha do MVP.

## Saiba mais

- [NNG — planejar pesquisa com IA](https://www.nngroup.com/articles/plan-research-ai/)
- [Product Talk — avaliação de IA](https://www.producttalk.org/ai-evals/)

Referências públicas consultadas em 13/11/2026. Exemplos e perguntas autorais de Laura Napoles, com apoio de Ada.

[Voltar ao início](../README.md)
