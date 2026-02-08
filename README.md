<h1 align="center">
📊 Sistema Integrado de Acompanhamento de Metas
</h1>

<p align="center">
Automação em Python para monitoramento de produtividade e geração de relatórios gerenciais em PDF.
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
![Platform](https://img.shields.io/badge/platform-Windows-blue)

</p>

---

## 📌 Visão Geral

Sistema desenvolvido para consolidar dados operacionais e gerar relatórios estratégicos de acompanhamento de metas de equipes técnicas.

Permite análise visual de desempenho por meio de:

- Calendário mensal de execução
- Indicadores de produtividade
- Comparação entre metas e resultados
- Gráficos automáticos

---

## 🚀 Funcionalidades Principais

### Ingestão Híbrida de Dados

- **Modo CSV (Offline)**  
  Processamento de planilhas exportadas manualmente.

- **Modo API (Online)**  
  Integração direta com fonte de dados para atualização automática.

---

### Visualização Estratégica

- Calendário mensal com mapa visual de produtividade
- Gráficos de barras:
  - Realizado vs Meta
- Linha de tendência de média diária

---

### Relatórios Automatizados

- Geração de PDF profissional
- Paginação automática
- Rodapé padronizado
- Nome único com timestamp

---

### Execução Simplificada

- Execução via script `.bat`
- Execução via terminal Python

---

## 📂 Estrutura do Projeto

acompanhamento_de_metas/
│
├── config/ # Credenciais da API e parâmetros do sistema
├── scripts/ # ETL de dados (CSV/API) e geração de gráficos
├── data/ # Arquivos CSV (modo offline)
├── tests/ # Testes automatizados
│
├── run_relatorio.py # Script principal (Entry Point)
├── gerar_relatorio_visitas.bat
├── requirements.txt

---

## ⚙️ Modos de Operação

### Integração via API (Automático)

- Configure credenciais e endpoints na pasta:
- O sistema buscará dados automaticamente.

---

### Importação via CSV (Manual)

Salvar arquivos na pasta:
Separador obrigatório:

| Arquivo | Colunas Obrigatórias | Formato Data |
|--------|----------------------|-------------|
| visitas.csv | DADOS DE EXECUÇÃO > Data da realização da atividade, Criado por | dd/mm/yyyy |
| coletivas.csv | Dados de Execução > Data, Criado por, ATIVIDADE PRÉ-FIXADA > ATIVIDADES | dd/mm/yyyy |
| metas.csv | Tecnico, Meta Mensal | N/A |

---

## 🛠️ Instalação

Pré-requisito:

- Python 3.8+

Instalar dependências:

```bash
pip install -r requirements.txt


▶️ Execução
Usuário Final (Windows)
Clique duas vezes em:
gerar_relatorio_visitas.bat
Desenvolvedor (Linha de Comando)
Edite parâmetros no início do:
run_relatorio.py
Execute:
python run_relatorio.py

🧰 Tecnologias Utilizadas
Python
Pandas
ReportLab / FPDF
Requests
Batchfile

🗺️ Roadmap
Interface gráfica
Dashboard Web
Integração com banco de dados
Comparativo entre períodos

👤 Autor
Antonio Marcos Sousa

📄 Licença
MIT


