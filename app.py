import io

import pandas as pd
import plotly.express as px
import streamlit as st

from auditor import (
    carregar_arquivo,
    classificar_colunas,
    calcular_score_qualidade,
    calcular_score_aderencia_modelo,
    executar_auditoria,
    gerar_diagnostico_executivo,
    preparar_resumo_por_categoria,
)


st.set_page_config(
    page_title="Smart Report Auditor",
    page_icon="🧭",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 0rem;
    }
    .subtitle {
        font-size: 1rem;
        color: #5f6368;
        margin-bottom: 1.5rem;
    }
    .insight-box {
        background-color: #F7F4FF;
        border-left: 5px solid #6D28D9;
        padding: 1rem;
        border-radius: 0.75rem;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">🧭 Smart Report Auditor</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Auditoria automática de relatórios operacionais: qualidade da base, alertas, gráficos e diagnóstico executivo.</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Upload do relatório")

    st.warning(
        "Privacidade e LGPD: não envie arquivos com dados pessoais, sensíveis, "
        "confidenciais ou estratégicos. Para testes, utilize bases fictícias, públicas "
        "ou devidamente anonimizadas."
    )

    confirmacao_lgpd = st.checkbox(
        "Confirmo que o arquivo enviado não contém dados pessoais, sensíveis ou confidenciais.",
        value=False,
    )

    uploaded_file = st.file_uploader(
        "Envie um arquivo CSV ou Excel",
        type=["csv", "xlsx", "xls"],
        disabled=not confirmacao_lgpd,
    )

    st.caption("Use o arquivo de exemplo em data/exemplo_relatorio_operacional.csv para testar o projeto.")

if uploaded_file is None:
    if not confirmacao_lgpd:
        st.info("Antes de enviar um arquivo, confirme a orientação de privacidade e LGPD na barra lateral.")
    else:
        st.info("Envie um arquivo CSV ou Excel para iniciar a auditoria.")
    st.markdown(
        """
        ### O que este app avalia?
        - Campos vazios
        - Colunas recomendadas ausentes
        - Duplicidades
        - Valores negativos ou zerados
        - Possíveis outliers
        - Inconsistências textuais
        - Score de qualidade da base
        - Diagnóstico executivo automático
        """
    )
    st.stop()

try:
    df = carregar_arquivo(uploaded_file)
except Exception as erro:
    st.error(f"Não foi possível carregar o arquivo: {erro}")
    st.stop()

auditoria = executar_auditoria(df)
score, status = calcular_score_qualidade(auditoria)
score_aderencia, status_aderencia = calcular_score_aderencia_modelo(auditoria)
tipos = classificar_colunas(df)

alertas_lgpd = auditoria[auditoria["validacao"].isin(["Possível dado pessoal", "Possível dado sensível"])]
if not alertas_lgpd.empty:
    st.error(
        "Atenção: foram identificadas colunas com nomes que podem indicar dados pessoais "
        "ou sensíveis. Revise a base antes de prosseguir e utilize apenas dados fictícios, "
        "públicos ou anonimizados."
    )

col1, col2, col3, col4 = st.columns(4)
col1.metric("Linhas", f"{len(df):,}".replace(",", "."))
col2.metric("Colunas", len(df.columns))
col3.metric("Score de qualidade", f"{score}/100")
col4.metric("Aderência ao modelo", f"{score_aderencia}/100")

st.caption(f"Status da base: **{status}** | Modelo recomendado: **{status_aderencia}**")

st.divider()

tab1, tab2, tab3, tab4 = st.tabs(
    ["Visão Executiva", "Auditoria da Base", "Gráficos Automáticos", "Prévia dos Dados"]
)

with tab1:
    st.subheader("Diagnóstico executivo")
    diagnostico = gerar_diagnostico_executivo(df, auditoria)
    st.markdown(
        f"<div class='insight-box'>{diagnostico.replace(chr(10), '<br>')}</div>",
        unsafe_allow_html=True,
    )

    st.subheader("Leitura estrutural da base")
    c1, c2, c3 = st.columns(3)
    c1.write("**Colunas numéricas identificadas**")
    c1.write(tipos["numericas"] or "Nenhuma coluna numérica identificada.")

    c2.write("**Colunas categóricas identificadas**")
    c2.write(tipos["categoricas"] or "Nenhuma coluna categórica identificada.")

    c3.write("**Possíveis colunas de data/período**")
    c3.write(tipos["datas"] or "Nenhuma coluna de data/período identificada.")

with tab2:
    st.subheader("Resultado da auditoria")
    st.dataframe(auditoria, use_container_width=True)

    csv_buffer = io.StringIO()
    auditoria.to_csv(csv_buffer, index=False, encoding="utf-8-sig")

    st.download_button(
        label="Baixar relatório de auditoria em CSV",
        data=csv_buffer.getvalue(),
        file_name="relatorio_auditoria.csv",
        mime="text/csv",
    )

with tab3:
    st.subheader("Gráficos gerados automaticamente")

    resumo = preparar_resumo_por_categoria(df)

    if resumo.empty:
        st.warning("Não foi possível gerar gráfico automático. A base precisa ter pelo menos uma coluna numérica e uma categórica.")
    else:
        dimensao = resumo.columns[0]
        metrica = resumo.columns[1]

        fig = px.bar(
            resumo,
            x=dimensao,
            y=metrica,
            title=f"Top 10 por {dimensao} considerando {metrica}",
            text_auto=True,
        )
        st.plotly_chart(fig, use_container_width=True)

    if len(tipos["numericas"]) >= 1 and len(tipos["datas"]) >= 1:
        data_col = tipos["datas"][0]
        metrica = tipos["numericas"][0]

        temp = df.copy()
        temp[data_col] = pd.to_datetime(temp[data_col], errors="coerce")
        temp = temp.dropna(subset=[data_col])

        if not temp.empty:
            serie = (
                temp.groupby(pd.Grouper(key=data_col, freq="ME"))[metrica]
                .sum()
                .reset_index()
            )

            fig_linha = px.line(
                serie,
                x=data_col,
                y=metrica,
                markers=True,
                title=f"Evolução temporal de {metrica}",
            )
            st.plotly_chart(fig_linha, use_container_width=True)

with tab4:
    st.subheader("Prévia dos dados enviados")
    st.dataframe(df.head(100), use_container_width=True)

    st.caption("Exibindo até 100 primeiras linhas para revisão visual.")