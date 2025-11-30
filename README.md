# 📈 Análise de Séries Temporais Climáticas — GHCN-GSN

Este projeto realiza análises exploratórias e modelagens iniciais de séries temporais utilizando dados climáticos diários da rede **Global Historical Climatology Network** (GHCN), em sua versão reduzida **GHCN-GSN**. O objetivo é estudar padrões, tendências e comportamentos meteorológicos ao longo do tempo, com foco em eficiência no tratamento dos dados.

---

## 📂 Dataset Utilizado

- O dataset oficial **GHCND (Global Historical Climatology Network – Daily)** possui aproximadamente **36 GB** em sua versão completa.  
- Para este trabalho, optou-se por utilizar a versão reduzida **GHCN-GSN**, com cerca de **2 GB**, contendo apenas as estações da *Global Surface Network*.  
- Os arquivos originais vêm no formato **.dly**, cada um representando anos de dados de uma estação.
- link para o download do dataset: https://www.ncei.noaa.gov/pub/data/ghcn/daily/ghcnd_gsn.tar.gz
---

## 🛠️ Pipeline de Processamento dos Dados

A pasta **`source/`** contém os scripts responsáveis por todo o processamento dos dados:

1. **Leitura e decodificação dos arquivos `.dly`**  
   - Extração das variáveis climáticas (temperatura mínima, máxima, precipitação etc.).  
   - Padronização da estrutura de cada registro.

2. **Geração de um único arquivo `.CSV` consolidado**  
   - Todos os arquivos `.dly` são unidos em um dataset tabular único, organizado por estação e data.

3. **Conversão do `.CSV` para `.PARQUET`**  
   - O formato Parquet foi escolhido por ser mais eficiente, comprimido e otimizado para análise em Python.  
   - Facilita a leitura rápida durante o processo de análise, este por sua vez não esta na pasta src, mas sim no
   - Notebook **analises**
   - Para facilitar a geração do arquivo .PARQUET você pode baixar diretamente aqui e o colocar na pasta dataset
   - Link: https://drive.google.com/drive/folders/1NHgAyrvNQwsPuaix9YMXXQhOHxd23o8b?usp=sharing
---

## 📊 Tipos de Análises Realizadas

Os notebooks contém as seguintes análises:

### 🔍 1. Análise Exploratória dos Dados (EDA)
- Estatísticas descritivas gerais das variáveis climáticas.
- Verificação da distribuição temporal dos dados.
- Identificação de valores ausentes, outliers e possíveis erros de medição.
- Análise da disponibilidade de dados por estação.

### 📅 2. Análises de Séries Temporais
- Visualizações da tendência ao longo do tempo para diferentes variáveis climáticas.  
- Gráficos de temperaturas (máximas e mínimas), acumulo de neve e outras métricas.  
- Agregações: diária → mensal → anual.
- Análise de padrões sazonais e comportamento interanual.

### 🌡️ 3. Análise de Mudanças e Tendências
- Avaliação de tendências de longo prazo para variáveis de interesse.  
- Comparação temporal entre diferentes períodos.

### 🌡️ 3. Uso de memória caches
- Utilização do banco de dados REDIS para o armazenamento de estações de interesses
- Consultas comunc ao banco em cache para o aumento de performances

---

## 🤖 Modelos e Métodos Utilizados

Dependendo da análise presente no notebook:

- **Modelos estatísticos de séries temporais**, como:
  - ARIMA / PROFHET  
  - Decomposição sazonal  
  - Previsão de eventos futuros

- **Métodos exploratórios**, incluindo:
  - Correlação entre variáveis  
  - Plot de tendências por periodo.

*Obs.: O foco principal deste trabalho está nas visualizações e análises exploratórias; modelos preditivos são utilizados apenas quando apropriado.*

---

## 🚀 Como Reproduzir

1. Baixe o dataset **GHCN-GSN** no formato `.dly`.
2. Execute os scripts na pasta **`source/`** para gerar o arquivo consolidado `.csv`.
3. Converta o arquivo `.csv` final para o formato `.parquet` e o coloque na pasta dataset.
4. Abra o notebook **`visualizacao.ipynb`** e execute as análises.

---

## 📁 Estrutura do Repositório

```text
/
| -- Data/
|   |- csv/
|   |- dataset/
|   |- dly/
|-- Analise/
|   |-- notebook/
|   |-- arima_profeth.ipynb
|   |-- analises.ipynb
|   |-- visualizacao.ipynb
|   L-- redis.ipynb
|-- source/
|   |-- dly_to_csv.py
|   |-- db_import.py
|   |-- generate_dataset.py
L-- README.md (este arquivo)