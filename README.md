VERSÃO ATUAL: v1.0 (estrutura congelada)
# 📊 Relatório de Acompanhamento de Metas

Este projeto gera relatórios em PDF para acompanhamento das metas de visitas e atividades coletivas realizadas por técnicos.

## 🚀 Funcionalidades

- Leitura de dados de execução (`data/visitas.csv`)
- Leitura de metas personalizadas (`data/metas.csv`)
- Leitura de atividades coletivas (`data/coletivas.csv`)
- Relatório em PDF com:
  - Calendário colorido (cinza, verde, vermelho)
  - Dados de visitas por técnico
  - Dados de atividades coletivas (quando existirem)
  - Resumo de desempenho (meta, executado, percentual)
  - Gráfico de barras com linha de meta diária média
- Rodapé fixo com data/hora e número da página
- Nome único para cada relatório (com timestamp)

## 📂 Estrutura do Projeto


## 📑 Formato dos CSVs

### `visitas.csv`

Colunas obrigatórias:

- `DADOS DE EXECUÇÃO > Data da realização da atividade`
- `Criado por`

Observação: o arquivo deve estar com separador `;` e com data no formato `dd/mm/yyyy`.

### `metas.csv`

Colunas obrigatórias:

- `Tecnico`
- `Meta Mensal`

Observação: o arquivo deve estar com separador `;`.

### `coletivas.csv`

Colunas obrigatórias:

- `Dados de Execução > Data`
- `Criado por`
- `ATIVIDADE PRÉ-FIXADA > ATIVIDADES`

Observação: o arquivo deve estar com separador `;` e com data no formato `dd/mm/yyyy`.

## ▶️ Como gerar o relatório

Edite o arquivo `run_relatorio.py` e defina:

```python
mes = 1   # exemplo: Janeiro
ano = 2026
