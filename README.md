# Toolkit de IA para profissionais de produto

Material autoral de **Laura Napoles**, organizado em cinco projetos complementares às fases do DPMT. Para profissionais de produto iniciantes em tecnologia e inteligência artificial.

## Comece aqui

1. Escolha a fase na tabela abaixo.
2. Leia o problema e os dados fictícios do exemplo.
3. Use o prompt e confira o resultado com os critérios de revisão.
4. Adapte a tarefa ao seu projeto, preservando a distinção entre evidência e hipótese.

**Estado atual:** guias das cinco fases e **aplicação interativa de Land disponível**. Land permite editar fontes, organizar recortes sem IA, comparar com um modelo por API e baixar a revisão. Uma primeira chamada real com os cartões fictícios foi observada e revisada pela tela. O bloco foi depois aprimorado para separar perguntas de pesquisa de hipóteses, com plano de teste e critério de refutação. Essa revisão passou por 20 testes sem rede; a nova geração real ainda precisa ser conferida. As respostas de referência dos guias são didáticas.

**[Abrir o guia de instalação e uso de Land →](GUIA-LAND.md)** · [Ver os testes e limites](TESTES-LAND.md)

| Fase | Projeto | O que aprender |
| --- | --- | --- |
| [1 — Land](fase-01/README.md) | Comparador de mercado com fontes | Relacionar pergunta, contexto, programa e resposta verificável |
| [2 — Discover](fase-02/README.md) | Analisador de entrevistas | Conferir temas, trechos, contradições e hipóteses |
| [3 — Build & Ship](fase-03/README.md) | Assistente de políticas | Entender recuperação de documentos, geração e limites de ação |
| [4 — Growth](fase-04/README.md) | Onboarding contextualizado | Combinar eventos, regras de segmentação e redação assistida |
| [5 — Learn & Iterate](fase-05/README.md) | Laboratório de avaliação | Conferir indicadores, qualidade, custos e decisões de evolução |

## Dois caminhos de aprendizagem

**Exploração guiada:** leia os exemplos e as referências de resposta. Não exige conta de IA nem credenciais.

**Execução com modelo:** os prompts podem ser experimentados em um assistente ao qual você já tenha acesso. Recursos, condições de dados e possíveis custos dependem da ferramenta. Land já inclui integração opcional por API, com configuração no painel lateral; consulte o guia e o alcance dos testes. As demais fases ainda são guias de exploração.

## Alternativa simples pelo terminal

Com Python 3 instalado, abra um terminal na pasta do projeto e execute:

```sh
python3 preparar_prompt.py
```

O programa lê `dados-land.json`, confere os identificadores e imprime o prompt com as fontes. Ele não consulta a internet, não chama um modelo e não exige bibliotecas adicionais. Você pode copiar o texto produzido para um assistente e revisar a resposta com o guia de Land.

## Como acompanhar a evolução

- [x] Organização das cinco fases e guias de exploração.
- [x] Dados fictícios, prompts e critérios de revisão.
- [x] Preparador de prompt de Land com validação básica dos dados.
- [x] Interface local de Land e integração implementada, com testes simulados registrados.
- [x] Primeira resposta real de Land observada e revisada com os três cartões fictícios.
- [x] Perguntas de pesquisa separadas de hipóteses, com como testar e o que enfraqueceria cada hipótese.
- [ ] Nova execução real após o ajuste das hipóteses e ensaio da demonstração.
- [ ] Aplicações das demais fases e interface compartilhada.
- [x] Guia de execução e alternativa sem IA para Land.
- [ ] Instruções de execução das integrações das demais fases.

Os exemplos das fases 1–4 usam a startup fictícia **DistribuiConecta**. A fase 5 usa um cenário didático ligado ao desafio Moinho; todos os números são inventados e não descrevem a organização real.

## Referências e autoria

Cada guia inclui links públicos para aprofundamento. Dados, prompts e exemplos são autorais. Os materiais internos dos cursos não integram este repositório. Não envie credenciais ou dados de participantes reais nos exemplos.

Responsável pelo material: **Laura Napoles**. Organização inicial em novembro de 2026.
