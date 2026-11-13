# Registro de testes — Land

Data: **13/11/2026**. Aplicação local no macOS, Python 3.12, Streamlit 1.67.0. Dados fictícios. Os testes automatizados e a primeira conferência no navegador não usaram chamadas reais. Posteriormente, Laura executou uma chamada real; o alcance da revisão está registrado abaixo.

## Testes automatizados

Comando executado:

```sh
python -m unittest -v test_land test_app
```

**Resultado atual: 22 testes aprovados** (16 de regras/integração simulada e seis da interface simulada), executados após a correção das opções de citação. A rodada original tinha 15 testes.

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

## Citações literais por fonte — 13/11/2026

Após o ajuste de hipóteses, uma nova execução de Laura foi bloqueada com a mensagem de citação não correspondente. A resposta rejeitada não foi preservada; não é possível afirmar se houve paráfrase, pontuação alterada ou troca de fonte.

O campo `evidencia` antes aceitava texto livre no formato da API, embora a conferência local exigisse correspondência literal. Agora o formato associa cada `fonte_id` a opções de citação copiadas de seu próprio recorte: texto inteiro e até 12 segmentos, sem alterar palavras. O formato usa alternativas `anyOf`, com valores `enum` por fonte. A verificação local continua ativa; nenhum texto rejeitado é corrigido silenciosamente ou aceito por semelhança. Mensagens de falha identificam a fonte e não repetem a chamada automaticamente.

Dois novos testes exercitam opções com acentos, aspas, pontuação e quebras de linha, vínculo entre fonte e citação, limite de opções e rejeição de paráfrase, reticências e citação de outra fonte. Uma evidência literal ainda pode não sustentar uma interpretação: isso depende da revisão humana.

## Execução real após a correção das citações

Executada **uma chamada** no aplicativo local com a configuração já preenchida e consentida por Laura, após aplicar a alteração. Não houve repetição automática nem acesso ao valor da chave. Modelo informado: `gpt-6-luna`; três fontes fictícias originais.

- Resultado aceito: três afirmações sustentadas pelos recortes e três citações literais da fonte correta. Lacunas preservadas, sem preços ou resultados inventados.
- Três perguntas de pesquisa separadas de três hipóteses não validadas. As hipóteses propõem efeitos sobre tempo de resposta/atendimento/elaboração, com medidas de qualidade; cada uma tem comparação proposta e resultado que a enfraqueceria.
- Exemplo observado: “A consulta de pedidos por integração com ERP reduz o tempo de atendimento sem prejudicar a correção das informações fornecidas.” Teste proposto: comparar tarefas equivalentes com consulta integrada e processo usual, medindo tempo e correção. Tempo igual/maior ou piora na correção enfraqueceriam a hipótese.
- Revisão de Ada: adequado como ponto de partida didático. Antes de executar pesquisas, definir participantes, equivalência das tarefas, critérios de correção e controle de diferenças entre grupos/períodos. Nenhuma dessas hipóteses foi validada com participantes.
- Uso informado pelo serviço: **1.392 tokens de entrada + 1.352 de saída = 2.744**. Valor cobrado não conferido.
- Download `comparacao-land.json` lido e verificado: versão 2, modo IA, fontes, perguntas, hipóteses, planos, critérios e uso preservados. Campos de revisão de Laura continuam desmarcados; não foram preenchidos pelo agente. Campos exportados conferidos sem credenciais.
- A captura do resultado e o arquivo foram preservados no material interno de preparação, fora dos arquivos do repositório. O sucesso desta execução não garante o comportamento de todos os modelos/entradas.

## Pendências antes da gravação com IA

- Laura registrar sua própria revisão na aplicação; a revisão de Ada e o download da nova execução estão conferidos acima.
- Ensaiar os nove minutos da demonstração e a alternativa sem IA.

Não validados: instalação em Windows/Linux, celulares, ambiente multiusuário, hospedagem pública, carga ou acessibilidade integral. O projeto é um exemplo didático local, não um serviço publicado.
