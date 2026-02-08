📊 Sistema Integrado de Acompanhamento de Metas
Este projeto é uma solução de automação em Python desenvolvida para monitorar a produtividade de equipes técnicas. O sistema gera relatórios visuais em PDF detalhados, permitindo a análise de desempenho através de calendários de atividades e gráficos comparativos de metas.
A grande vantagem desta versão é a sua flexibilidade de ingestão de dados: o sistema pode operar tanto offline (lendo arquivos CSV locais) quanto online (buscando dados em tempo real via integração com API).
🚀 Funcionalidades Principais
• Ingestão Híbrida de Dados:
    ◦ Modo Arquivo: Processamento de planilhas CSV exportadas manualmente.
    ◦ Modo API: Conexão direta para busca automática de dados de execução atualizados.
• Visualização Estratégica:
    ◦ Calendário mensal com status visual (mapa de calor/cores) da produtividade diária.
    ◦ Gráficos de barras comparando "Realizado vs. Meta".
    ◦ Linha de tendência de média diária.
• Relatórios Automatizados: Geração de PDFs prontos para impressão com timestamp único, paginação e rodapé.
• Execução Simplificada: Scripts .bat para execução em ambiente Windows com um clique.
📂 Estrutura do Projeto
A organização do código separa a lógica de execução, configuração e testes:

.
├── config/                 # Credenciais da API e parâmetros do sistema
├── scripts/                # Módulos de processamento (ETL via CSV ou API) e geração de gráficos
├── data/                   # Pasta para depósito dos arquivos .csv (se usar Modo Arquivo)
├── tests/                  # Testes unitários
├── run_relatorio.py        # Script principal (Entry point)
├── gerar_relatorio_visitas.bat # Executável Windows (Automação)
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação

📍 Modos de Operação e Configuração
O sistema pode ser alimentado de duas formas. Escolha a que se adapta ao seu fluxo de trabalho:
Opção A: Integração via API (Automático)
Ideal para dados em tempo real. O script conecta-se diretamente à fonte de dados.
• Certifique-se de que as credenciais de acesso e endpoints estão configurados corretamente dentro da pasta config/.
• Neste modo, o sistema ignora a pasta data/ e busca as visitas e atividades do período estipulado.
Opção B: Importação via CSV (Manual)
Ideal para análises pontuais ou dados históricos offline. Salve os arquivos na pasta data/ seguindo a formatação rigorosa abaixo:
Arquivo
	
Colunas Obrigatórias (Separador ;)
	
Formato Data
visitas.csv
	
DADOS DE EXECUÇÃO > Data da realização da atividade, Criado por
	
dd/mm/yyyy
coletivas.csv
	
Dados de Execução > Data, Criado por, ATIVIDADE PRÉ-FIXADA > ATIVIDADES
	
dd/mm/yyyy
metas.csv
	
Tecnico, Meta Mensal
	
N/A
🛠️ Instalação e Execução
Pré-requisitos
• Python 3.8+ instalado.
• Instalação das bibliotecas:
Como Gerar os Relatórios
1. Via Windows (Usuário Final)
Para facilitar a rotina, utilize os arquivos de lote. Basta clicar duas vezes em:
• gerar_relatorio_visitas.bat
2. Via Linha de Comando (Desenvolvedor)
Para alterar parâmetros como mês/ano de referência ou forçar o modo de operação (API/CSV), edite as variáveis no início do arquivo run_relatorio.py e execute:

python run_relatorio.py

⚙️ Tecnologias
• Linguagem: Python (96.5%)
• Automação: Batchfile (3.5%)
• Bibliotecas: Pandas (manipulação de dados), ReportLab/Fpdf (geração de PDF), Requests (Integração API).

--------------------------------------------------------------------------------
Projeto mantido por amarcossousa.