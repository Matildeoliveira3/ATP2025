"""
Módulo: interface.py
Interface Gráfica
"""

import FreeSimpleGUI as sg
import simulacao
import analise
import json
import os
import matplotlib as mpl
mpl.rcParams['toolbar'] = 'None'



def carregar_dataset():
    if os.path.exists("pessoas.json"):
        try:
            with open("pessoas.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except: 
            return []
    return []
def carregar_config():
    if os.path.exists("config.json"):
        with open("config.json","r",encoding="utf-8") as f:
            return json.load(f)
        return{}
def guardar_config(config):
    with open("config.json","w",encoding="utf-8") as f:
        json.dump(config,f,indent=4,ensure_ascii=False)
    
sg.theme("DarkBlue")


# Dicionário de utilizadores
utilizadores = {"admin": "1234"}

def verificaUser(utilizadores, utilizador, password):
    return utilizador in utilizadores and utilizadores[utilizador] == password

# Layout do login
layout_login = [
    [sg.Image(filename="logotipos.png",size=(450,200))],
    [sg.Text("Bem-vindo", font=("Helvetica", 24), justification='center', expand_x=True)],
    [sg.Text("Utilizador:", size=(12,1), justification='right'), sg.InputText(key='Utilizador', size=(25,1))],
    [sg.Text("Palavra-passe:", size=(12,1), justification='right'), sg.InputText(key='password', password_char="*", size=(25,1))],
    [sg.Checkbox("Manter sessão iniciada", key='manter_sessao', pad=((12,0),0))],
    [sg.Text("", key='mensagem', text_color='red', size=(40,1), justification='center')],
    [sg.Button("Entrar", key='ok', size=(12,1)), sg.Button("Cancelar", key='cancelar', size=(12,1))]
]

# Janela do login
janela = sg.Window(
    "Entrada no Sistema da Clínica",
    layout_login,
    element_justification='center',
    font=('Arial', 14),
    size=(500,550),
    resizable=True
)

stop = False
autenticacao = False
user_autenticado = ""

while not stop:
    event, values = janela.read()
    
    if event in [sg.WIN_CLOSED, "cancelar"]:
        stop = True
    
    elif event == 'ok':
        user = values["Utilizador"].strip()
        pw = values["password"].strip()
        
        if verificaUser(utilizadores, user, pw):
            autenticacao = True
            user_autenticado = user
            stop = True  
        else:
            janela['Utilizador'].update('')
            janela['password'].update('')
            janela['mensagem'].update('Credenciais inválidas! Tente novamente...')

janela.close()
if autenticacao:
    coluna_botoes=[
        [sg.Button("Executar")]
    ]
    config_json=carregar_config()
    dados_tabela=[]
    coluna_esquerda=sg.Column([
        [sg.Frame("Configuração da Simulação",[
            [sg.Text("Taxa Chegada:"),sg.Spin([i for i in range(10,31)],initial_value=config_json.get("taxa_chegada",10), key='-TAXA-',size=(5,1))],
            [sg.Text("Número de Médicos:"), sg.Spin(list(range(1,15)),initial_value=config_json.get("num_medicos",3),key='-MEDICOS-',size=(5,1))],
            [sg.Text("Tempo Médio:"), sg.Input(config_json.get("tempo_med",15), size=(5,1), key='-TEMPO-')],
            [sg.Text("Duração (min):"), sg.Input(config_json.get("tempo_max",480), size=(5,1), key='-DURACAO-')],
            [sg.Text("Distribuição:"), sg.Combo(["exponential","normal","uniform"],default_value=config_json.get("distribuicao","exponential"), key='-DIST-')]
        ])],
        [sg.Button("Executar Simulação", size=(22,2), key='Botao_Simulacao')],
        [sg.Button("Sair", size=(25,2))]
    ], vertical_alignment="top",expand_y=True)
    
    frame_estatisticas = sg.Frame("Estatísticas", [
        [sg.Text("Atendidos:"), sg.Text("-", key="-EST_ATEND-")],
        [sg.Text("Espera média:"), sg.Text("-", key="-EST_ESPERA-")],
        [sg.Text("Tempo médio clínica:"), sg.Text("-", key="-EST_CLIN-")],
        [sg.Text("Ocupação média:"), sg.Text("-", key="-EST_OCUP-")],
        [sg.Text("Fila máxima:"), sg.Text("-", key="-EST_FILA-")],
        [sg.Text("Desistências:"), sg.Text("-", key="-EST_DES-")],
        [sg.Text("Taxa desistência:"), sg.Text("-", key="-EST_TAXA-")]
    ], expand_x=True)

    coluna_direita=sg.Column([
        [sg.Text("Relatório da Simulação",font=("Arial",16))],
        [sg.Table(
            values=dados_tabela, 
            headings=[" Nome Completo ", "Idade", "Prioridade", "Especialidade","Espera(min)","Clínica(min)"],
            key="-Tabela-",
            justification="center",
            num_rows=5,
            expand_x=True,

        )],
        [frame_estatisticas]
    ],expand_x=True,expand_y=True)


    layout_graficos=[
            [sg.Button("Análise Sensibilidade", key='Botao_Sensibilidade')],
            [sg.Button("Evolução da Fila",key="-G_FILA-")],
            [sg.Button("Ocupação Médicos",key="-G_OCUP-")],
            [sg.Button("Histograma Clínica",key="-G_CLIN-")],
            [sg.Button("Histograma Desistências",key="-G_DES-")]
        ]

    layout_principal =[
        [sg.Image("logotipos.png", pad=(10, 0),size=(150,150)),sg.Push(),sg.Button("Ajuda(?)", key="Botao_Ajuda_top", size=(10, 1), pad=(0, 20))],
        [sg.Text(f"Bem-vindo, {user_autenticado}!", font=('Arial', 20))],
        [sg.TabGroup([
            [
            sg.Tab("Simulação",[
            [
                sg.Column([[coluna_esquerda]], expand_x=True,expand_y=True),
                sg.VerticalSeparator(),
                sg.Column([[coluna_direita]], expand_x=True, expand_y=True)
            ]
        ]),
        sg.Tab("Gráficos",layout_graficos)
        ]
    ], expand_x=True, expand_y=True)]]
    
    

    janela_principal = sg.Window("Simulador Clínica", layout_principal, resizable=True,finalize=True,size=(1200,700),element_padding=(5,5))
    running=True
    resultado=None
    dados_tabela=[]
    while running:
        event,values=janela_principal.read()
        if event =="Botao_Ajuda_top":
            sg.popup(
                "AJUDA\n\n"
                "1. Configure os parâmetros à esquerda\n"
                "2. Clique em 'Executar Simulação'\n"
                "3. Veja os resultados na tabela e nas estatísticas abaixo\n"
                "4. Consulte os gráficos na aba 'Gráficos'"
            )

                
        if event in (sg.WIN_CLOSED,"Sair"):
            confirmar=sg.popup_yes_no("Tem a certeza que pretende sair?",title="Confirmação de saída")
            if confirmar=="Yes":
                running=False
            else:
                continue
        if event == 'Botao_Simulacao':
            config = {
                "taxa_chegada": int(values['-TAXA-']),
                "num_medicos": int(values['-MEDICOS-']),
                "tempo_max": int(values['-DURACAO-']),
                "tempo_med":float(values["-TEMPO-"]),
                "distribuicao":values['-DIST-']
            }
            
            pessoas=carregar_dataset()
            resultado=simulacao.simular_atendimento(config,pessoas)
            dados_tabela=[]
            for p in resultado["pessoas"]:
                dados_tabela.append([
                    p["nome"],
                    p["idade"],
                    p["prioridade"],
                    p["especialidade"],
                    f'{p["tempo_espera"]:.1f}',
                    f'{p["tempo_clinica"]:.1f}'
                ])
            janela_principal["-Tabela-"].update(values=dados_tabela)
            sg.popup("Simulação Concluida com Sucesso! \n" \
            "Ficheiro completo do relatório guardado!")
            janela_principal["-EST_ATEND-"].update(resultado.get("doentes_atendidos", "-"))
            janela_principal["-EST_ESPERA-"].update(f"{resultado.get('media_espera',0):.1f}")
            janela_principal["-EST_CLIN-"].update(f"{resultado.get('media_clinica',0):.1f}")
            janela_principal["-EST_OCUP-"].update(f"{resultado.get('ocupacao_media',0):.1f}")
            janela_principal["-EST_FILA-"].update(resultado.get("max_fila","-"))
            janela_principal["-EST_DES-"].update(resultado.get("desistencias_verdes","-"))
            janela_principal["-EST_TAXA-"].update(f"{resultado.get('taxa_desistencia_verdes',0)*100:.1f}%")
                
        if event=="-G_FILA-":
            if resultado:
                analise.plot_evolucao_fila(resultado["hist_fila"])
            else:
                sg.popup("Execute a simulação primeiro!")
        if event=="-G_OCUP-":
            if resultado:
                analise.plot_ocupacao(resultado["hist_ocupacao"])
            else:
                sg.popup("Execute a simulação primeiro!")
        if event=="-G_CLIN-":
            if resultado:
                analise.plot_histograma_clinica(
                [p["tempo_clinica"] for p in resultado["pessoas"]]
            )
            else:
                sg.popup("Execute a simulação primeiro!")
        if event=="-G_DES-":
            if resultado and resultado["tempos_desistencia"]:
                analise.plot_histograma_desistencias(resultado["tempos_desistencia"])
            else:
                sg.popup("Não houve desistências nesta simulação!")
        
        if event=="Botao_Sensibilidade":
            if resultado:
                analise.plot_sensibilidade(config)
            else:
                sg.popup("Execute a simulação primeiro!")

        
        janela_principal["-Tabela-"].update(values=dados_tabela)
