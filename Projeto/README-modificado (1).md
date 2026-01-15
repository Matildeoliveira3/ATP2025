
# Simulação de Atendimento em Clínica Médica

## Identificação do Aluno
* **Nome:** [Ana Matilde Fernandes Oliveira, Matilde Laurido Arede, Sofia Lopes Milhases Ferreira]
* **Número:** [a112014,a110034,a111094]
* **Curso:** [Engenharia Biomédica]
* **Unidade Curricular:** [Algoritmos e Técnicas de Programação]

## Descrição do Projeto
Esta aplicação, desenvolvida em Python, implementa uma simulação de eventos discretos para modelar o funcionamento de uma clínica médica. O objetivo é analisar filas de espera, ocupação de médicos e tempos de atendimento sob diferentes condições.

## Credenciais de Acesso
Para aceder à área de gestão e configuração da simulação, utilize os seguintes dados de login:

* **Utilizador:** `admin`
* **Palavra-passe:** `1234`

A simulação contempla lógica complexa, incluindo:
* **Triagem de Manchester Simplificada:** Atribuição de prioridades (Verde, Amarela, Vermelha) baseada na idade e probabilidade.
* **Especialidades Médicas:** Gestão de médicos e doentes de diferentes áreas (Geral, Medicina Interna, Ortopedia, Cardiologia e Pediatria).
* **Comportamento de Desistência:** Doentes com pulseira Verde desistem se o tempo de espera exceder um limite (90 ou 180 min, dependendo da idade).
* **Alocação Dinâmica:** Algoritmo inteligente que direciona crianças para Pediatras e outros doentes para as respetivas especialidades.

## Funcionalidades Principais
1. **Autenticação Segura:** Sistema de login para acesso à área de gestão.
2. **Configuração Flexível:** Permite alterar em tempo real:
   - Alterar o tempo de simulação 
   - Taxa de chegada de doentes (λ).
   - Número de médicos disponíveis.
   - Tempo médio de consulta.
   - Distribuição estatística (Exponencial, Normal ou Uniforme).
3. **Dashboard Estatístico:** Visualização imediata de métricas como o tempo médio de espera, taxa de desistência e ocupação, número de atendidos, número de desistências e fila máxima 
4. **Visualização Gráfica:**
   - Evolução da fila ao longo do tempo.
   - Ocupação instantânea dos médicos.
   - Histogramas de tempos de clínica e desistências.
   - Análise de sensibilidade (Stress Test).
5. **Relatórios:** Geração automática de relatórios detalhados (`relatorio_final.txt`) e exportação de configurações (`config.json`).

## Estrutura do Projeto
O projeto está organizado nos seguintes módulos:

* **`interface.py` (App Principal):** Contém a interface gráfica (GUI) construída com `FreeSimpleGUI`. Gere a interação com o utilizador e a atualização dos dados.
* **`simulacao.py`:** O motor da simulação. Contém a lógica de geração de doentes, filas de prioridade, gestão de eventos e algoritmos de decisão.
* **`analise.py`:** Módulo responsável pelo tratamento de dados e geração de gráficos estatísticos utilizando `Matplotlib`.
* **Ficheiros de Dados:**
    * `pessoas.json`: Base de dados inicial de utentes.
    * `logotipos.png`: Imagem utilizada na interface gráfica.

## Pré-requisitos e Instalação

Para executar este projeto, é necessário ter as seguintes bibliotecas externas instaladas:
pip install numpy matplotlib FreeSimpleGUI 
