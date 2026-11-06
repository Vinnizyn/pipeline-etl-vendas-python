# 📊 Pipeline ETL e Análise de Indicadores de Vendas (Python & Pandas)

Projeto de Engenharia e Análise de Dados desenvolvido em **Python** com foco na automação do processo de **ETL (Extração, Transformação e Carga)** de bases comerciais, tratamento de inconsistências e geração de indicadores de negócio (KPIs) prontos para ferramentas de Business Intelligence e Dashboards.

---

## 🎯 Objetivo do Projeto
Em ambientes corporativos e operacionais, relatórios manuais em folhas de cálculo frequentemente sofrem com registos duplicados, falhas de digitação e campos nulos. Este script automatiza a higienização dos dados brutos e gera tabelas consolidadas de faturação e ticket médio em segundos.

---

## ⚙️ Etapas do Pipeline (Arquitetura ETL)

1. **Extract (Extração):**
   - Leitura automatizada de bases brutas em formato `.csv` (com gerador integrado de base de testes caso o ficheiro de origem ainda não exista no diretório).
2. **Transform (Transformação e Regras de Negócio):**
   - **Deduplicação:** Remoção automática de transações duplicadas com base no `id_transacao`.
   - **Data Quality & Higienização:** Padronização de strings (`strip`, `title`), filtragem de quantidades inválidas e tratamento de valores nulos (`fillna` com mediana estatística).
   - **Enriquecimento de Dados:** Cálculo de faturação total por linha, extração de safra mensal (`ano_mes`) e agregação de vendas aprovadas por categoria.
3. **Load (Carga e Relatórios):**
   - Exportação da base limpa (`vendas_tratadas_etl.csv`) e do relatório executivo de performance (`relatorio_kpi_categorias.csv`).

---

## 🛠️ Tecnologias Utilizadas
- **Python 3.x**
- **Pandas** (Manipulação, limpeza e agregação de DataFrames)
- **NumPy** (Apoio em operações matemáticas e vetoriais)

---

## 🚀 Como Executar Localmente

```bash
# 1. Clonar o repositório
git clone [https://github.com/SEU-USUARIO/pipeline-etl-vendas-python.git](https://github.com/SEU-USUARIO/pipeline-etl-vendas-python.git)

# 2. Instalar a biblioteca Pandas
pip install pandas numpy

# 3. Executar o pipeline ETL
python etl_vendas.py
