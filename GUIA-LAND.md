# Land — do recorte à comparação revisável

Um exemplo para entender onde a IA entra em um produto digital. Você fornece uma pergunta e de uma a seis fontes, acompanha a preparação do contexto e revisa o resultado. O caso inicial usa Alfa, Beta e Gama, fornecedores **fictícios** no cenário DistribuiConecta.

**Objetivo de aprendizagem:** explicar o caminho interface → programa → contexto → modelo → checagens → revisão humana e distinguir evidência, informação ausente, pergunta de pesquisa e hipótese testável.

## Escolha como explorar

| Caminho | O que acontece | Acesso |
| --- | --- | --- |
| Sem IA | O programa organiza literalmente os recortes. Você interpreta e anota as lacunas. | Sem conta de IA; depois da instalação, não precisa consultar serviços externos. |
| Com IA | O programa envia a pergunta e os cartões à API da OpenAI e solicita uma comparação estruturada. | Chave de API e modelo compatível na sua conta; pode haver cobrança. |
| Só o prompt | Você baixa o pedido e o usa em um assistente de sua preferência. | Conforme as condições desse assistente; a resposta externa não passa pelas checagens do aplicativo. |

Uma primeira chamada real foi observada e revisada com os três cartões fictícios. Depois, o bloco de hipóteses foi ajustado e passou por **20 testes automatizados sem rede**. **A nova versão ainda precisa de uma execução real para revisar as hipóteses geradas.** Veja o [registro de testes](TESTES-LAND.md). Nenhum crédito institucional é necessário para o caminho sem IA; não há promessa de créditos para o outro caminho.

## Abra no seu computador

Não é necessário saber programar para explorar os campos. A primeira instalação exige copiar alguns comandos. Separe cerca de 15–25 minutos; é uma estimativa, não parte da gravação.

1. Instale Python 3.12 pelo [site oficial do Python](https://www.python.org/downloads/), se ainda não estiver instalado. A versão testada foi 3.12.
2. No repositório, use **Code → Download ZIP** e extraia a pasta. Se o repositório estiver privado, você precisa de acesso concedido pela responsável.
3. Abra o Terminal dentro da pasta extraída. No Mac, você pode digitar `cd `, arrastar a pasta para a janela e pressionar Enter.
4. No macOS/Linux, execute uma linha de cada vez:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py --server.address 127.0.0.1 --browser.gatherUsageStats false
```

No Windows, os comandos correspondentes são:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --browser.gatherUsageStats false
```

O terminal informa o endereço local, normalmente `http://127.0.0.1:8501`. Abra-o no navegador. Mantenha o terminal aberto enquanto usa o aplicativo. Para encerrar, pressione **Ctrl+C** no terminal. Os comandos de Windows e Linux ainda não foram executados nesta validação.

Na próxima vez, entre na mesma pasta, ative o ambiente no Mac/Linux e execute apenas a última linha. No Windows, execute a última linha diretamente. Se aparecer “porta em uso”, encerre a execução anterior ou acrescente `--server.port 8502`.

## Explore sem IA

1. Mantenha **Sem IA** selecionado. Leia a pergunta e os três cartões.
2. Clique em **Organizar fontes sem IA**. Compare os recortes com a tabela; não houve resumo nem geração de hipóteses.
3. Abra **Ler afirmações e citações completas** para conferir textos longos.
4. Registre uma lacuna: “Beta informa integração com ERP, mas o recorte não informa tempo de implantação”.
5. Marque somente as revisões que fez e escreva o que precisa investigar.
6. Use **Baixar comparação e revisão** para salvar pergunta, fontes, resultado e anotações em JSON, um formato de texto estruturado.
7. Altere uma fonte. O resultado anterior será retirado da tela; execute novamente para ver a nova entrada.

As URLs no campo referência são apenas anotações. O aplicativo não abre essas páginas e não realiza pesquisa de mercado.

## Experimente com um modelo

1. Escolha **Com IA** no painel lateral.
2. Informe o identificador de um modelo disponível na sua conta que aceite a Responses API e Structured Outputs. Não há modelo nem preço fixado neste exemplo; confirme ambos na documentação e na sua conta antes do uso.
3. Digite sua chave no campo **Chave de API**, que oculta o texto. Faça isso somente no aplicativo local. Não coloque a chave nos cartões, em capturas de tela ou no GitHub.
4. Leia os dados, marque a opção de envio e clique em **Comparar com IA**.
5. Revise afirmações, citações e lacunas; depois, confira **Perguntas para pesquisar** e **Hipóteses a testar — não validadas**. Cada hipótese apresenta **Como testar** e **O que enfraqueceria a hipótese**. O programa exige uma linha por fonte e descarta citações que não aparecem nos recortes.
6. Anote correções e baixe a revisão. Uma nova execução pode ter resposta diferente e consumir uso adicional.

A chamada envia pergunta, identificadores, fornecedores, recortes e referências para a OpenAI. A chave autentica a requisição; não integra o prompt nem a exportação. Usuários técnicos podem fornecer `OPENAI_API_KEY` e `OPENAI_MODEL` no ambiente local; esses campos são opcionais. Não é necessário criar um arquivo de credenciais.

Há uma única tentativa por clique, com espera de conexão de até 45 segundos e limite de saída de 4.000 tokens. Se o modelo não completar a resposta nesse limite, o aplicativo mostra uma mensagem em vez de aceitar uma tabela parcial. Não há cálculo de preço: os tokens eventualmente exibidos são os informados pelo serviço.

A requisição usa `store: false`, que controla o armazenamento da resposta pela API. Isso **não equivale a garantia de ausência de retenção** de todos os dados do serviço; consulte as condições aplicáveis à sua conta. Este exemplo foi preparado para uso local individual, sem autenticação própria para hospedagem compartilhada.

## Diferencie pergunta e hipótese

- **Evidência:** “Consulta a pedidos por integração com ERP”, no recorte M02.
- **Pergunta de pesquisa:** “Quais ERPs são compatíveis?” Preenche uma lacuna.
- **Hipótese não validada:** “Consultar pedidos dentro do atendimento reduz o tempo de resposta.” Propõe um efeito observável.
- **Como testar:** comparar tempo e correção das respostas em tarefas equivalentes com e sem integração.
- **O que enfraqueceria:** tempo igual ou maior, ou piora na correção das respostas.

Este é um exemplo didático escrito para ensino. A fonte motiva a hipótese, mas não comprova o benefício; nenhum teste com participantes foi realizado. O modelo pode não propor hipóteses quando faltarem elementos. Ter todos os campos preenchidos não garante que a hipótese ou o teste sejam bons: a revisão continua humana.

O arquivo baixado usa a versão 2: perguntas ficam em `perguntas_pesquisa`, hipóteses em `hipoteses`, com `como_testar` e `o_que_enfraquece`. Downloads antigos continuam sendo registros da versão anterior; o aplicativo não os importa nem converte. Depois de atualizar o programa, gere uma nova comparação para obter o novo formato. Uma nova chamada com IA pode gerar cobrança.

## Se algo falhar

| Situação | Como continuar |
| --- | --- |
| Botão de IA desabilitado | Confira os campos das fontes, o modelo, a chave e a opção de envio. |
| Chave recusada ou operação sem acesso | Confira a configuração da sua conta, sem divulgar a chave. |
| Limite de uso ou saldo | Verifique a conta antes de tentar novamente; use Sem IA como alternativa. |
| Modelo/formato incompatível | Confirme suporte a Responses e Structured Outputs. |
| Citação inválida, resposta incompleta ou erro de rede | A comparação não é aceita. Reduza os recortes, revise a configuração ou use o prompt manualmente. |

## Demonstração sugerida: 9 minutos

Este recorte cabe no bloco de demonstração de Land; não substitui a aula de 60 minutos. Instalação e configuração ficam prontas antes de gravar. O tempo ainda precisa de ensaio.

| Tempo | Tela e fala sugerida | Verificação |
| --- | --- | --- |
| 0–2 min | Mostre pergunta e cartões: “Nosso contexto vem destes recortes fictícios. O sistema não está pesquisando a internet.” | Distinguir entrada de pesquisa completa. |
| 2–3 min | Abra o pedido preparado: “A interface coleta; o programa organiza os dados e as instruções.” | Relacionar interface, código e contexto. |
| 3–5 min | Execute com IA após validar a conta previamente. Na alternativa sem IA, organize os trechos e declare que a interpretação é manual. | Identificar qual etapa usa modelo e qual é regra. |
| 5–7 min | Compare afirmações e citações: “Não encontrar preço neste trecho não significa que o fornecedor não divulga preço.” | Preservar a lacuna. |
| 7–9 min | Registre uma hipótese e uma pergunta de pesquisa. Mostre o download com a revisão. | Explicar o que ainda precisa de evidência. |

## Atividade posterior: 10–15 minutos

Acrescente um cartão fictício sobre um quarto fornecedor, mencionando uma capacidade e omitindo uma informação relevante. Gere ou organize a comparação e escreva duas perguntas para pesquisa posterior. Essa atividade não é uma nova entrega obrigatória da FIAP.

Critérios: cada afirmação tem fonte; as citações são pertinentes; ausência de informação permanece como lacuna; perguntas não são apresentadas como hipóteses; cada hipótese tem uma forma de teste e um resultado que a enfraqueceria; o aluno explica o que mudaria sua conclusão. A aparência da tabela não é critério de qualidade.

## O que este projeto verifica — e o que não verifica

- Confere campos, identificadores únicos, cobertura de todas as fontes e presença literal das citações, tolerando diferenças de espaços e quebras de linha.
- Confere a presença de perguntas/hipóteses em listas separadas, campos de teste não vazios e referências existentes.
- Não prova que uma citação sustenta a interpretação, que uma hipótese é testável ou que o plano de teste é adequado. Uma conclusão errada pode citar um trecho verdadeiro.
- Não confirma autenticidade, atualidade ou completude dos recortes, nem neutraliza todas as tentativas de instruções maliciosas dentro das fontes.
- Não valida mercado ou vantagem competitiva. Os dados iniciais são inventados para ensinar o método.

## Para quem quer olhar o código

| Arquivo | Função |
| --- | --- |
| [app.py](app.py) | Campos, estados da tela, execução e revisão. |
| [land_core.py](land_core.py) | Regras de entrada, prompt, contrato de resposta, chamada HTTP e checagens. |
| [dados-land.json](dados-land.json) | Três cartões fictícios iniciais. |
| [requirements.txt](requirements.txt) | Versão de Streamlit usada na interface. |
| [test_land.py](test_land.py) e [test_app.py](test_app.py) | Testes sem rede e sem credenciais reais. |
| [preparar_prompt.py](preparar_prompt.py) | Alternativa simples de terminal, sem bibliotecas adicionais. |

Para repetir os testes no ambiente instalado:

```sh
python -m unittest -v test_land test_app
```

## Fontes técnicas

Documentação consultada em **13/11/2026**, com leitura dos trechos pertinentes, não dos sites inteiros:

- [OpenAI — Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs): formato JSON Schema e limites das respostas estruturadas.
- [OpenAI — criação de uma resposta](https://developers.openai.com/api/reference/resources/responses/methods/create): campos do pedido e estrutura da resposta.
- [Streamlit — campos de texto](https://docs.streamlit.io/develop/api-reference/widgets/st.text_area): entradas editáveis.
- [Streamlit — estado da sessão](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state): preservação de dados durante interações.
- [Streamlit — AppTest](https://docs.streamlit.io/develop/api-reference/app-testing/st.testing.v1.apptest): testes simulados da interface.

Dados, exemplos, código e proposta de demonstração autorais de Laura Napoles, com apoio de Ada. [Voltar ao Toolkit](README.md).
