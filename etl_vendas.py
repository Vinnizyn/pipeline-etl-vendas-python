import os
import pandas as pd
import numpy as np

def gerar_base_exemplo(caminho_ficheiro: str) -> None:
    """
    Gera um ficheiro CSV de vendas brutas simulando problemas reais de sistemas
    (valores nulos, linhas duplicadas e formatação inconsistente) caso não exista.
    """
    dados_brutos = {
        "id_transacao": [1001, 1002, 1003, 1003, 1004, 1005, 1006, 1007, 1008],
        "data_venda": [
            "2026-01-15", "2026-01-16", "2026-01-16", "2026-01-16",
            "2026-02-02", "2026-02-10", None, "2026-03-05", "2026-03-12"
        ],
        "cliente": [
            "  Empresa Alpha ", "Beta Comércio", "Gama Tech", "Gama Tech",
            "Delta Serviços", "Omega Pagamentos", "Cliente Sem Data", "Zeta Corp", "Eta Logística"
        ],
        "categoria": [
            "Software", "Hardware", "software", "software",
            "Consultoria", "Meios de Pagamento", "Hardware", "MEIOS DE PAGAMENTO", "Consultoria"
        ],
        "quantidade": [2, 1, 5, 5, 1, 10, 2, -3, 4],
        "valor_unitario": [1500.00, 3200.50, 450.00, 450.00, 5000.00, 120.00, 800.00, 250.00, None],
        "status_pagamento": [
            "Aprovado", "Aprovado", "Pendente", "Pendente",
            "Aprovado", "Aprovado", "Cancelado", "Aprovado", "Aprovado"
        ]
    }
    df_bruto = pd.DataFrame(dados_brutos)
    df_bruto.to_csv(caminho_ficheiro, index=False, encoding="utf-8")
    print(f"[INFO] Base bruta de exemplo gerada em: {caminho_ficheiro}")


def extrair_dados(caminho_ficheiro: str) -> pd.DataFrame:
    """1. EXTRACT: Lê a base de dados bruta em formato CSV."""
    if not os.path.exists(caminho_ficheiro):
        gerar_base_exemplo(caminho_ficheiro)
    
    print("[1/3 - EXTRACT] A carregar dados brutos de vendas...")
    return pd.read_csv(caminho_ficheiro, encoding="utf-8")


def transformar_dados(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    2. TRANSFORM: Realiza higienização, padronização, tratamento de nulos
    e aplicação de regras de negócio para geração de indicadores (KPIs).
    """
    print("[2/3 - TRANSFORM] A iniciar limpeza e transformação de dados...")
    df_limpo = df.copy()

    # 1. Remoção de registos duplicados pelo ID da transação
    total_inicial = len(df_limpo)
    df_limpo = df_limpo.drop_duplicates(subset=["id_transacao"], keep="first")
    print(f" -> Duplicados removidos: {total_inicial - len(df_limpo)}")

    # 2. Exclusão de vendas sem data registada ou com quantidades inválidas (<= 0)
    df_limpo = df_limpo.dropna(subset=["data_venda"])
    df_limpo = df_limpo[df_limpo["quantidade"] > 0]

    # 3. Padronização de textos (remoção de espaços extras e capitalização)
    df_limpo["cliente"] = df_limpo["cliente"].astype(str).str.strip().str.title()
    df_limpo["categoria"] = df_limpo["categoria"].astype(str).str.strip().str.title()
    df_limpo["status_pagamento"] = df_limpo["status_pagamento"].astype(str).str.strip().str.title()

    # 4. Tratamento de valores nulos no preço unitário usando a mediana da categoria
    mediana_geral = df_limpo["valor_unitario"].median()
    df_limpo["valor_unitario"] = df_limpo["valor_unitario"].fillna(mediana_geral)

    # 5. Conversão de datas e criação de colunas de período (Ano-Mês)
    df_limpo["data_venda"] = pd.to_datetime(df_limpo["data_venda"], errors="coerce")
    df_limpo["ano_mes"] = df_limpo["data_venda"].dt.to_period("M").astype(str)

    # 6. Cálculo de Faturação Total por transação
    df_limpo["faturacao_total"] = (df_limpo["quantidade"] * df_limpo["valor_unitario"]).round(2)

    # 7. Agregação Gerencial: Resumo por Categoria (apenas vendas Aprovadas)
    df_aprovadas = df_limpo[df_limpo["status_pagamento"] == "Aprovado"]
    resumo_categorias = (
        df_aprovadas.groupby("categoria", as_index=False)
        .agg(
            total_transacoes=("id_transacao", "count"),
            itens_vendidos=("quantidade", "sum"),
            receita_total=("faturacao_total", "sum"),
            ticket_medio=("faturacao_total", "mean")
        )
        .sort_values(by="receita_total", ascending=False)
    )
    resumo_categorias["ticket_medio"] = resumo_categorias["ticket_medio"].round(2)

    return df_limpo, resumo_categorias


def carregar_dados(df_tratado: pd.DataFrame, df_resumo: pd.DataFrame) -> None:
    """3. LOAD: Exporta as bases tratadas e o relatório executivo para consumo em BI."""
    print("[3/3 - LOAD] A exportar bases tratadas e relatórios...")
    df_tratado.to_csv("vendas_tratadas_etl.csv", index=False, encoding="utf-8")
    df_resumo.to_csv("relatorio_kpi_categorias.csv", index=False, encoding="utf-8")

    print("\n=== RESUMO EXECUTIVO DE VENDAS APROVADAS ===")
    print(df_resumo.to_string(index=False))
    print("\n[SUCESSO] Pipeline ETL concluído! Ficheiros exportados com sucesso.")


if __name__ == "__main__":
    ficheiro_entrada = "vendas_brutas.csv"
    df_raw = extrair_dados(ficheiro_entrada)
    df_clean, df_kpis = transformar_dados(df_raw)
    carregar_dados(df_clean, df_kpis)
