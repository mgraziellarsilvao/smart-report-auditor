from __future__ import annotations

import unicodedata
from typing import Dict, List, Tuple

import pandas as pd


COLUNAS_RECOMENDADAS = [
    "data_lancamento",
    "area",
    "categoria",
    "unidade",
    "centro_custo",
    "tipo_custo",
    "valor",
    "status",
    "competencia",
]


def normalizar_texto(texto: object) -> str:
    """Padroniza texto para comparação simples."""
    if pd.isna(texto):
        return ""
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join([c for c in texto if not unicodedata.combining(c)])
    return texto


def carregar_arquivo(uploaded_file) -> pd.DataFrame:
    """Lê CSV ou Excel enviado pelo usuário."""
    nome = uploaded_file.name.lower()

    if nome.endswith(".csv"):
        return pd.read_csv(uploaded_file)

    if nome.endswith((".xlsx", ".xls")):
        return pd.read_excel(uploaded_file)

    raise ValueError("Formato não suportado. Envie um arquivo CSV ou Excel.")


def classificar_colunas(df: pd.DataFrame) -> Dict[str, List[str]]:
    """Classifica colunas por tipo para apoiar análise automática."""
    numericas = df.select_dtypes(include=["number"]).columns.tolist()
    datas = []
    categorias = []

    for coluna in df.columns:
        serie = df[coluna]
        nome_coluna = normalizar_texto(coluna)

        if coluna not in numericas:
            amostra = serie.dropna().astype(str).head(30)
            if "data" in nome_coluna or "mes" in nome_coluna or "competencia" in nome_coluna:
                datas.append(coluna)
            elif len(amostra.unique()) <= max(20, int(len(df) * 0.5)):
                categorias.append(coluna)

    return {
        "numericas": numericas,
        "datas": datas,
        "categoricas": categorias,
    }


def verificar_colunas_recomendadas(df: pd.DataFrame) -> pd.DataFrame:
    existentes = [normalizar_texto(c) for c in df.columns]
    registros = []

    for coluna in COLUNAS_RECOMENDADAS:
        registros.append({
            "validacao": "Coluna recomendada",
            "campo": coluna,
            "status": "OK" if coluna in existentes else "Ausente",
            "criticidade": "Alta" if coluna in ["data_lancamento", "categoria", "valor"] and coluna not in existentes else "Média",
            "detalhe": "Campo encontrado." if coluna in existentes else "Campo não identificado na base."
        })

    return pd.DataFrame(registros)


def verificar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    registros = []
    total_linhas = len(df)

    for coluna in df.columns:
        qtd = int(df[coluna].isna().sum() + (df[coluna].astype(str).str.strip() == "").sum())
        pct = (qtd / total_linhas * 100) if total_linhas else 0

        if qtd > 0:
            registros.append({
                "validacao": "Campos vazios",
                "campo": coluna,
                "status": "Alerta",
                "criticidade": "Alta" if pct >= 10 else "Média",
                "detalhe": f"{qtd} registros vazios ({pct:.1f}% da base)."
            })

    return pd.DataFrame(registros)


def verificar_duplicidades(df: pd.DataFrame) -> pd.DataFrame:
    qtd = int(df.duplicated().sum())

    if qtd == 0:
        return pd.DataFrame([{
            "validacao": "Duplicidades",
            "campo": "linha completa",
            "status": "OK",
            "criticidade": "Baixa",
            "detalhe": "Nenhuma linha totalmente duplicada identificada."
        }])

    return pd.DataFrame([{
        "validacao": "Duplicidades",
        "campo": "linha completa",
        "status": "Alerta",
        "criticidade": "Alta" if qtd > 5 else "Média",
        "detalhe": f"{qtd} linhas duplicadas foram identificadas."
    }])


def verificar_valores_numericos(df: pd.DataFrame) -> pd.DataFrame:
    registros = []
    numericas = df.select_dtypes(include=["number"]).columns.tolist()

    for coluna in numericas:
        negativos = int((df[coluna] < 0).sum())
        zeros = int((df[coluna] == 0).sum())

        if negativos > 0:
            registros.append({
                "validacao": "Valores negativos",
                "campo": coluna,
                "status": "Alerta",
                "criticidade": "Alta",
                "detalhe": f"{negativos} registros negativos identificados."
            })

        if zeros > 0:
            registros.append({
                "validacao": "Valores zerados",
                "campo": coluna,
                "status": "Atenção",
                "criticidade": "Média",
                "detalhe": f"{zeros} registros zerados identificados."
            })

        if len(df[coluna].dropna()) > 0:
            q1 = df[coluna].quantile(0.25)
            q3 = df[coluna].quantile(0.75)
            iqr = q3 - q1
            limite_superior = q3 + 1.5 * iqr
            outliers = int((df[coluna] > limite_superior).sum())

            if outliers > 0:
                registros.append({
                    "validacao": "Possíveis outliers",
                    "campo": coluna,
                    "status": "Atenção",
                    "criticidade": "Média",
                    "detalhe": f"{outliers} valores acima do comportamento esperado pelo IQR."
                })

    return pd.DataFrame(registros)


def verificar_categorias_similares(df: pd.DataFrame) -> pd.DataFrame:
    registros = []
    candidatas = [c for c in df.columns if df[c].dtype == "object"]

    for coluna in candidatas:
        valores = df[coluna].dropna().astype(str).str.strip()
        normalizados = valores.apply(normalizar_texto)
        mapa = pd.DataFrame({"original": valores, "normalizado": normalizados}).drop_duplicates()

        grupos = mapa.groupby("normalizado")["original"].nunique().reset_index()
        inconsistentes = grupos[grupos["original"] > 1]

        if not inconsistentes.empty:
            registros.append({
                "validacao": "Padronização textual",
                "campo": coluna,
                "status": "Atenção",
                "criticidade": "Média",
                "detalhe": "Possíveis variações de escrita ou acentuação encontradas."
            })

    return pd.DataFrame(registros)



def verificar_possiveis_dados_pessoais(df: pd.DataFrame) -> pd.DataFrame:
    """Identifica nomes de colunas que podem indicar dados pessoais ou sensíveis.

    A função não confirma a existência de dado pessoal. Ela apenas gera um alerta
    preventivo para que o usuário revise a base antes de usar o app.
    """
    termos_pessoais = [
        "nome", "cpf", "cnpj", "rg", "email", "e-mail", "telefone", "celular",
        "endereco", "endereço", "cep", "matricula", "matrícula", "colaborador",
        "funcionario", "funcionário", "usuario", "usuário", "login", "id_pessoa",
        "id_funcionario", "employee", "person", "documento"
    ]

    termos_sensiveis = [
        "saude", "saúde", "doenca", "doença", "diagnostico", "diagnóstico",
        "religiao", "religião", "sindicato", "politica", "política",
        "biometria", "racial", "etnia", "genero", "gênero", "vida_sexual"
    ]

    registros = []

    for coluna in df.columns:
        nome_normalizado = normalizar_texto(coluna)

        termos_encontrados = [
            termo for termo in termos_pessoais
            if normalizar_texto(termo) in nome_normalizado
        ]

        termos_sensiveis_encontrados = [
            termo for termo in termos_sensiveis
            if normalizar_texto(termo) in nome_normalizado
        ]

        if termos_sensiveis_encontrados:
            registros.append({
                "validacao": "Possível dado sensível",
                "campo": coluna,
                "status": "Alerta",
                "criticidade": "Alta",
                "detalhe": (
                    "O nome da coluna sugere possível dado pessoal sensível. "
                    "Revise a base e utilize apenas dados fictícios, públicos ou anonimizados."
                )
            })
        elif termos_encontrados:
            registros.append({
                "validacao": "Possível dado pessoal",
                "campo": coluna,
                "status": "Atenção",
                "criticidade": "Alta",
                "detalhe": (
                    "O nome da coluna sugere possível dado pessoal. "
                    "Evite enviar dados identificáveis e prefira bases anonimizadas."
                )
            })

    return pd.DataFrame(registros)


def executar_auditoria(df: pd.DataFrame) -> pd.DataFrame:
    """Executa todas as regras de auditoria e devolve tabela consolidada."""
    checks = [
        verificar_possiveis_dados_pessoais(df),
        verificar_colunas_recomendadas(df),
        verificar_nulos(df),
        verificar_duplicidades(df),
        verificar_valores_numericos(df),
        verificar_categorias_similares(df),
    ]

    resultado = pd.concat([c for c in checks if not c.empty], ignore_index=True)

    if resultado.empty:
        return pd.DataFrame([{
            "validacao": "Auditoria geral",
            "campo": "base",
            "status": "OK",
            "criticidade": "Baixa",
            "detalhe": "Nenhum alerta relevante identificado."
        }])

    return resultado


def calcular_score_qualidade(resultado: pd.DataFrame) -> Tuple[int, str]:
    """Calcula nota simples de qualidade da base."""
    score = 100

    pesos = {
        "Alta": 12,
        "Média": 7,
        "Baixa": 3,
    }

    alertas = resultado[resultado["status"].isin(["Alerta", "Atenção", "Ausente"])]

    for criticidade in alertas["criticidade"].fillna("Baixa"):
        score -= pesos.get(criticidade, 3)

    score = max(score, 0)

    if score >= 85:
        status = "Base saudável"
    elif score >= 65:
        status = "Base com pontos de atenção"
    else:
        status = "Base crítica para uso analítico"

    return score, status


def gerar_diagnostico_executivo(df: pd.DataFrame, auditoria: pd.DataFrame) -> str:
    score, status = calcular_score_qualidade(auditoria)
    total_linhas = len(df)
    total_colunas = len(df.columns)

    criticos = auditoria[auditoria["criticidade"] == "Alta"]
    alertas = auditoria[auditoria["status"].isin(["Alerta", "Atenção", "Ausente"])]

    texto = [
        f"A base analisada possui {total_linhas} linhas e {total_colunas} colunas.",
        f"O score de qualidade calculado foi {score}/100, classificando a base como: {status}.",
    ]

    if len(alertas) == 0:
        texto.append("Não foram encontrados alertas relevantes. A base apresenta boa consistência inicial para análise.")
    else:
        texto.append(f"Foram encontrados {len(alertas)} pontos de atenção, sendo {len(criticos)} classificados como criticidade alta.")

    principais = alertas.head(3)

    if not principais.empty:
        texto.append("Principais recomendações:")
        for _, linha in principais.iterrows():
            texto.append(f"- Revisar {linha['campo']}: {linha['detalhe']}")

    texto.append(
        "Recomendação executiva: antes de usar a base em dashboards ou apresentações, trate os alertas críticos "
        "e padronize os campos mais usados para segmentação, como categoria, área, competência e centro de custo."
    )

    return "\n".join(texto)


def preparar_resumo_por_categoria(df: pd.DataFrame) -> pd.DataFrame:
    """Cria resumo simples quando há coluna numérica e categórica."""
    tipos = classificar_colunas(df)
    numericas = tipos["numericas"]
    categoricas = tipos["categoricas"]

    if not numericas or not categoricas:
        return pd.DataFrame()

    metrica = numericas[0]
    dimensao = categoricas[0]

    resumo = (
        df.groupby(dimensao, dropna=False)[metrica]
        .sum()
        .reset_index()
        .sort_values(metrica, ascending=False)
        .head(10)
    )

    return resumo