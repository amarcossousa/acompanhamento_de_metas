# 📊 Relatório de Acompanhamento de Metas

Este projeto gera relatórios em PDF para acompanhamento das metas de visitas realizadas por técnicos.

## 🚀 Funcionalidades
- Leitura de dados de execução (`data/visista.csv`).
- Leitura de metas personalizadas (`data/metas.csv`).
- Relatório em PDF com:
  - Calendário colorido (cinza, verde, vermelho).
  - Resumo de desempenho (meta, executado, percentual).
  - Gráfico de barras com linha de meta diária média.
- Rodapé fixo com data/hora e número da página.
- Nome único para cada relatório (com timestamp).

## 📂 Estrutura
acompanhamento_de_metas/
├── data/
│   ├── exemplo_visista.csv
│   ├── exemplo_metas.csv
│   └── .gitignore
├── reports/
├── relatorio.py
├── run_relatorio.py
└── README.md


## 📑 Formato dos CSVs

### `visitas.csv`
Colunas obrigatórias:
- `DADOS DE EXECUÇÃO > Data da realização da atividade`
- `Criado por`

### `metas.csv`
