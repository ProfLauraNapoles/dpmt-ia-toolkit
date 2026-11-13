# Registro de testes — Land

Data: **13/11/2026**. Aplicação local no macOS, Python 3.12, Streamlit 1.67.0. Dados fictícios. Os testes automatizados e a primeira conferência no navegador não usaram chamadas reais. Posteriormente, Laura executou uma chamada real; o alcance da revisão está registrado abaixo.

## Testes automatizados

Comando executado:

```sh
python -m unittest -v test_land test_app
```

**Resultado atual: 20 testes aprovados** (14 de regras/integração simulada e seis da interface simulada), executados após o ajuste do bloco de hipóteses. A rodada original tinha 15 testes.

Cobertura relevante:

- Campos vazios, limites, IDs duplicados e fontes inválidas são rejeitados.
- Edições aparecem no modo sem IA, que não chama modelo.
- Fontes desconhecidas/repetidas, cobertura incompleta, citações inventadas, hipóteses com referências inválidas e ausência de limites são rejeitadas.
- O teste registra expressamente que uma interpretação errada com citação literal pode passar: revisão humana continua necessária.
- Transporte simulado verifica endereço fixo, autenticação fora do prompt, JSON Schema, `store: false`, timeout e uma chamada por clique.
- Respostas incompletas, recusas, formato inválido, conteúdo excessivo, falhas de rede e erros HTTP 400/401/403/429/500 geram mensagens compreensíveis sem expor a credencial fictícia.
- A interface exige campos e opção de envio para habilitar IA. O modelo só é chamado ao clicar. Nova entrada, troca de modo e falha retiram o resultado anterior.
- Inclusão/remoção de fonte e restauração do exemplo foram verificadas.

O AppTest pode emitir o aviso “missing ScriptRunContext” no processo de teste; os testes passaram sem exceção da aplicação. Isso não é evidência de uma chamada externa.

## Verificação no navegador

Chrome no macOS: abertura local, execução sem IA, três fontes na tabela, leitura integral das citações, preenchimento da revisão e download JSON conferidos. O arquivo baixado preservou as três fontes e a anotação de revisão. A marcação da revisão foi conferida na interface e no arquivo. Também confirmadas a retirada do resultado após editar a pergunta, a restauração do exemplo e a desabilitação da chamada de IA sem configuração.

## Primeira execução real — revisão da tela enviada por Laura

Evidência: captura e texto da interface enviados por Laura em 13/11/2026, às 22:29 no nome da captura. Execução no modo Com IA, modelo informado `gpt-6-luna`, com os três cartões fictícios originais M01–M03. A tela apresenta uma resposta, a confirmação dos controles de formato/identificadores/citações e o consumo informado pelo serviço: 534 tokens de entrada, 712 de saída, 1.246 no total. A soma é consistente; o custo efetivamente cobrado não foi conferido.

Revisão de conteúdo por Ada, comparando o texto visível com `dados-land.json`:

| Fonte | Afirmação observada | Resultado da revisão |
| --- | --- | --- |
| M01 — Alfa | Caixa de entrada compartilhada e distribuição de conversas entre atendentes. | Sustentada pelo trecho, com citação literal correspondente. Integração com pedidos e preço permanecem sem informação. |
| M02 — Beta | Consulta a pedidos por integração com ERP. | Sustentada pelo trecho, com citação literal correspondente. Caixa compartilhada e tempo de implantação permanecem sem informação. |
| M03 — Gama | Geração de rascunhos de resposta com revisão humana. | Sustentada pelo trecho, com citação literal correspondente. Bases e taxa de acerto permanecem sem informação. |

Os limites explicam corretamente que ausência de menção não comprova ausência da funcionalidade e que os recortes não representam todo o mercado. Não foi observada invenção de preço, taxa de acerto ou superioridade de um fornecedor no resultado mostrado.

**Ajuste pedagógico identificado:** os três itens chamados de “Hipóteses para investigar” são sugestões de pesquisa: descobrir canais/regras de distribuição, ERPs/dados disponíveis e bases/medição dos rascunhos. Não são hipóteses testáveis. Antes da gravação, ajustar o rótulo e a orientação ou solicitar hipóteses explícitas com modo de verificação. Exemplo de hipótese proposta por Ada, ainda não validada: “Consultar pedidos dentro do atendimento reduz o tempo necessário para responder sobre o status de um pedido.” Verificação possível: comparar tempo e correção das respostas em tarefas equivalentes com e sem integração. Os trechos motivam essa investigação, mas não demonstram o benefício.

**Ajuste de redação:** nas lacunas de M01/M02, a expressão “essas capacidades” agrupa funcionalidades com preço ou tempo de implantação. Preferir “O trecho não informa X; é necessário consultar outra fonte”.

**Limites desta conferência:** o download `comparacao-land.json` foi indicado, mas o arquivo não estava disponível para leitura no ambiente de revisão; a busca pelos nomes `comparacao-land*.json` também não localizou uma cópia. Portanto, esta revisão usa a tela enviada, não certifica o JSON exportado, seus metadados ou a ausência de credenciais no arquivo desta execução. Os controles de revisão aparecem desmarcados na captura; a avaliação de Ada não foi registrada como marcação feita por Laura. Nenhuma nova chamada, leitura de chave ou alteração da aplicação foi realizada nesta revisão.

Resultado: **integração real e comparação factual observadas com sucesso neste exemplo; exportação da execução real ainda não conferida e ajuste pedagógico pendente**. Uma execução não valida outros modelos, entradas ou ambientes. Esta é a evidência da versão anterior do bloco; não equivale a um teste real do novo formato.

## Ajuste de perguntas e hipóteses — 13/11/2026

- Prompt e formato de resposta passam a separar `perguntas_pesquisa` de `hipoteses`. Para cada hipótese, exigidos `como_testar`, `o_que_enfraquece` e ao menos uma fonte existente que motive a ideia. Listas podem ficar vazias; o programa não força hipóteses.
- Interface mostra a distinção, o plano de teste, o resultado que enfraqueceria a hipótese e uma revisão humana específica. Removido o aviso desatualizado de que nunca houve teste real; o alcance dos testes permanece documentado aqui.
- Exportação usa `versao: 2`. Resultados antigos em sessão são retirados antes de acessar os campos novos, sem repetir automaticamente chamadas. Downloads antigos não são alterados.
- O preparador de prompt do terminal reutiliza as instruções da aplicação, e o guia da fase foi alinhado.
- Os 20 testes passaram sem chamadas externas: novos casos cobrem resposta completa/incompleta, campos de teste vazios, referências inválidas/repetidas/ausentes, limite de três itens, hipóteses vazias, exportação dos novos campos e revisão, títulos e conteúdo da tela, atualização de sessão antiga e equivalência do prompt de terminal.
- Os testes verificam estrutura e fluxo. Não detectam automaticamente toda pergunta disfarçada de hipótese, nem comprovam adequação do método proposto. Essa revisão é humana. A resposta didática usada nos testes não foi gerada por IA.
- Documentação oficial de [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs) reconsultada em 13/11/2026: campos obrigatórios e objetos sem propriedades extras; checagens de negócio e revisão de conteúdo continuam necessárias.

## Pendências antes da gravação com IA

- Conferir o JSON exportado desta execução quando estiver disponível e registrar a revisão humana.
- Executar uma comparação real com o novo formato e revisar se as hipóteses e seus testes são pertinentes; conferir se a redação específica das lacunas melhorou.
- Ensaiar os nove minutos da demonstração e a alternativa sem IA.

Não validados: instalação em Windows/Linux, celulares, ambiente multiusuário, hospedagem pública, carga ou acessibilidade integral. O projeto é um exemplo didático local, não um serviço publicado.
