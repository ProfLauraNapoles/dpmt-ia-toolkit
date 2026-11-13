"""Land: explorar fontes, comparar com IA e revisar. Execute com streamlit run app.py."""
import json
import os
from pathlib import Path
import streamlit as st
from land_core import (DEFAULT_QUESTION, MAX_SOURCES, LandError, build_prompt,
                       call_model, fingerprint, organize_offline, report, validate_inputs)

BASE = Path(__file__).resolve().parent
st.set_page_config(page_title="Land | Toolkit de IA", page_icon="📚", layout="wide")
SEEDS = json.loads((BASE / "dados-land.json").read_text(encoding="utf-8"))


def reset_example():
    for key in list(st.session_state):
        if key.startswith(("supplier_", "excerpt_", "reference_", "review_", "note_")):
            del st.session_state[key]
    st.session_state.source_count = len(SEEDS)
    st.session_state.question = DEFAULT_QUESTION
    st.session_state.pop("execution", None)


def change_count(delta):
    st.session_state.source_count += delta
    st.session_state.pop("execution", None)


st.session_state.setdefault("source_count", len(SEEDS))
st.session_state.setdefault("question", DEFAULT_QUESTION)
with st.sidebar:
    st.caption("TOOLKIT DE IA · LAURA NAPOLES")
    st.header("Seu caminho")
    mode_label = st.radio("Como explorar", ["Sem IA", "Com IA"], key="mode")
    mode = "offline" if mode_label == "Sem IA" else "ia"
    model, api_key, consent = "", "", False
    if mode == "ia":
        st.caption("A pergunta e os trechos serão enviados à OpenAI somente ao clicar em Comparar com IA.")
        model = st.text_input("Modelo disponível na sua conta", value=os.getenv("OPENAI_MODEL", ""),
                              placeholder="Identificador do modelo", key="model")
        supplied_key = st.text_input("Chave de API", type="password", key="api_key",
                                     help="Uso nesta sessão. Não é incluída nos arquivos baixados.")
        api_key = supplied_key or os.getenv("OPENAI_API_KEY", "")
        if not supplied_key and api_key:
            st.caption("Chave configurada no ambiente local.")
        consent = st.checkbox("Quero enviar estes dados à OpenAI; o uso pode gerar cobrança.", key="consent")
        st.caption("A qualidade da comparação depende das fontes e do modelo. Revise cada resultado antes de usá-lo.")
    else:
        st.info("Sem conta e sem envio de dados. O programa organiza literalmente os trechos; a interpretação é sua.")
    st.button("Restaurar exemplo fictício", on_click=reset_example, key="reset")
    st.divider()
    st.caption("Land · Fundamentos de tecnologia e IA")
    st.markdown("[Guia do projeto](https://github.com/ProfLauraNapoles/dpmt-ia-toolkit/blob/main/GUIA-LAND.md)")

st.caption("FASE 01 / LAND")
st.title("Compare fontes. Confira as conclusões.")
st.write("Transforme recortes de informação em uma comparação que você consegue revisar.")
st.caption("O exemplo inicial usa fornecedores fictícios. Referências e URLs são anotações: o aplicativo não abre páginas nem pesquisa na internet.")

st.subheader("1. Qual é a sua pergunta?")
question = st.text_area("Pergunta de investigação",
                        max_chars=1000, height=90, key="question")
st.subheader("2. Quais informações você tem?")
st.caption("Edite os recortes. Inclua apenas dados fictícios ou que você tem autorização para utilizar.")
cards = []
columns = st.columns(min(st.session_state.source_count, 3))
for i in range(st.session_state.source_count):
    seed = SEEDS[i] if i < len(SEEDS) else {"fornecedor": "", "trecho": ""}
    with columns[i % len(columns)]:
        with st.container(border=True):
            st.markdown(f"**Fonte M{i + 1:02d}**")
            supplier = st.text_input(f"Fornecedor da fonte {i + 1}", value=seed["fornecedor"],
                                     max_chars=80, key=f"supplier_{i}")
            excerpt = st.text_area(f"Trecho da fonte {i + 1}", value=seed["trecho"],
                                   height=150, max_chars=1800, key=f"excerpt_{i}")
            reference = st.text_input(f"Referência da fonte {i + 1} (opcional)", max_chars=300,
                                      placeholder="Título, URL ou data do recorte", key=f"reference_{i}")
            cards.append({"id": f"M{i+1:02d}", "fornecedor": supplier,
                          "trecho": excerpt, "referencia": reference})
add_col, remove_col, _ = st.columns([1, 1, 4])
with add_col:
    st.button("Adicionar fonte", key="add", on_click=change_count, args=(1,),
              disabled=st.session_state.source_count >= MAX_SOURCES)
with remove_col:
    st.button("Remover última", key="remove", on_click=change_count, args=(-1,),
              disabled=st.session_state.source_count <= 1)

signature = fingerprint(question, cards, mode, model)
old = st.session_state.get("execution")
if old and old["signature"] != signature:
    del st.session_state["execution"]
    st.info("A entrada ou o formato do resultado mudou. Gere uma nova comparação com as fontes atuais.")

valid, prompt = True, ""
try:
    q, checked_cards = validate_inputs(question, cards)
    prompt = build_prompt(q, checked_cards)
except LandError as exc:
    valid = False
    st.warning(str(exc))

with st.expander("Veja o pedido que será usado"):
    if prompt:
        st.code(prompt, language="text")
        st.download_button("Baixar prompt", prompt, "prompt-land.txt", mime="text/plain", key="prompt_download")

ready = valid and (mode == "offline" or bool(api_key and model.strip() and consent))
if mode == "ia" and not ready and valid:
    st.caption("Para executar com IA, informe modelo e chave no painel lateral e marque a opção de envio.")
button_label = "Organizar fontes sem IA" if mode == "offline" else "Comparar com IA"
if st.button(button_label, type="primary", disabled=not ready, key="run"):
    st.session_state.pop("execution", None)
    try:
        with st.spinner("Preparando a comparação…"):
            if mode == "offline":
                result, usage = organize_offline(q, checked_cards), {}
            else:
                result, usage = call_model(q, checked_cards, model, api_key)
        st.session_state["execution"] = {"signature": signature, "question": q,
            "cards": checked_cards, "mode": mode, "model": model,
            "result": result, "usage": usage, "run_id": os.urandom(8).hex()}
    except LandError as exc:
        st.error(str(exc))

execution = st.session_state.get("execution")
if execution:
    st.divider()
    st.subheader("3. Revise o resultado")
    result = execution["result"]
    if execution["mode"] == "offline":
        st.info("Resultado sem IA: os trechos foram organizados literalmente. Não houve análise automática nem geração de hipóteses.")
    else:
        st.success("Formato, identificadores e presença das citações conferidos. Revise o sentido de cada afirmação.")
    by_id = {c["id"]: c for c in execution["cards"]}
    rows = [{"Fonte": row["fonte_id"], "Fornecedor": by_id[row["fonte_id"]]["fornecedor"],
             "Afirmação ou trecho": row["afirmacao"], "Evidência literal": row["evidencia"],
             "Lacunas": " • ".join(row["lacunas"])} for row in result["comparacao"]]
    st.dataframe(rows, hide_index=True, width="stretch", key="comparison_table")
    with st.expander("Ler afirmações e citações completas"):
        for row in result["comparacao"]:
            st.text(f"{row['fonte_id']} · {by_id[row['fonte_id']]['fornecedor']}")
            st.text("Afirmação ou trecho: " + row["afirmacao"])
            st.text("Evidência literal: " + row["evidencia"])
            st.text("Lacunas: " + ("; ".join(row["lacunas"]) or "Nenhuma declarada pelo modelo; confira."))
            st.divider()
    if result["perguntas_pesquisa"]:
        st.markdown("**Perguntas para pesquisar**")
        st.caption("Informações que ainda faltam. Uma pergunta de pesquisa não é uma hipótese.")
        for i, item in enumerate(result["perguntas_pesquisa"], 1):
            st.text(f"{i}. {item['pergunta']}\nFontes que motivam a pergunta: {', '.join(item['fontes'])}")
    if result["hipoteses"]:
        st.markdown("**Hipóteses a testar — não validadas**")
        st.caption("As fontes motivam estas ideias, mas não comprovam o efeito proposto. Os testes abaixo ainda não foram realizados.")
        for i, item in enumerate(result["hipoteses"], 1):
            with st.container(border=True):
                st.text(f"{i}. {item['hipotese']}")
                st.text("Fontes que motivam a hipótese: " + ', '.join(item['fontes']))
                st.text("Como testar: " + item['como_testar'])
                st.text("O que enfraqueceria a hipótese: " + item['o_que_enfraquece'])
    elif execution["mode"] == "ia":
        st.info("Nenhuma hipótese foi proposta. Confira os limites e as perguntas para decidir o que investigar.")
    for limitation in result["limites"]:
        st.text(limitation)
    if execution["usage"]:
        st.caption("Tokens informados pelo serviço: " + json.dumps(execution["usage"], ensure_ascii=False))
    st.markdown("**Sua revisão**")
    run_id = execution["run_id"]
    review = {
        "afirmacoes_sustentadas": st.checkbox("Conferi se as fontes sustentam as afirmações.", key=f"review_claims_{run_id}"),
        "lacunas_preservadas": st.checkbox("Conferi se informação ausente permaneceu como lacuna.", key=f"review_gaps_{run_id}"),
        "hipoteses_separadas": st.checkbox("Distingui evidências, perguntas de pesquisa e hipóteses não validadas.", key=f"review_hypotheses_{run_id}"),
        "testes_revisados": st.checkbox("Revisei como testar cada hipótese e o que a enfraqueceria.", key=f"review_tests_{run_id}",
                                        disabled=not bool(result["hipoteses"])),
        "anotacao": st.text_area("O que precisa ser corrigido ou investigado?", max_chars=3000, key=f"note_{run_id}"),
    }
    document = report(execution["question"], execution["cards"], execution["mode"],
                      execution["model"], result, execution["usage"], review)
    st.download_button("Baixar comparação e revisão", json.dumps(document, ensure_ascii=False, indent=2),
                       file_name="comparacao-land.json", mime="application/json", key="report_download")

with st.expander("Como as peças se conectam"):
    st.write("Sua pergunta e os recortes entram pela interface. O programa confere os campos e prepara o contexto. No modo com IA, uma chamada ao modelo produz a comparação. Depois, o programa verifica o formato, os IDs e os trechos citados. Você revisa a interpretação.")
    st.caption("Interface → validação → contexto → modelo (opcional) → checagens → revisão humana")
    st.markdown("[Documentação da API](https://developers.openai.com/api/docs/guides/structured-outputs) · [Materiais do Toolkit](https://github.com/ProfLauraNapoles/dpmt-ia-toolkit)")
