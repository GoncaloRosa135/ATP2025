import FreeSimpleGUI as sg
import Base

sg.theme('DarkTeal9') 

FONT_HEADER = ('Helvetica', 16, 'bold')
FONT_TITLE = ('Helvetica', 12, 'bold')
FONT_TEXT = ('Arial', 10)
FONT_MONO = ('Consolas', 10) 
BTN_SIZE_L = (25, 2)
BTN_SIZE_M = (25, 1)

def criar_janela_login():
    sg.set_options(font=FONT_TEXT)
    col_layout = [
        [sg.Text("CLÍNICA MÉDICA", font=('Helvetica', 20, 'bold'), text_color='#ecf0f1', pad=((0,0),(20,5)))],
        [sg.Text("Sistema de Simulação e Gestão", font=('Arial', 10, 'italic'), text_color='#95a5a6', pad=((0,0),(0,20)))],
        [sg.Text("ID Utilizador", font=('Arial', 8, 'bold'), text_color='#bdc3c7')],
        [sg.Input(key='-USER-', size=(30,1), border_width=0, background_color='#ecf0f1', text_color='#2c3e50')],
        [sg.Text("Palavra-Passe", font=('Arial', 8, 'bold'), text_color='#bdc3c7', pad=((0,0),(10,0)))],
        [sg.Input(key='-PASS-', password_char='●', size=(30,1), border_width=0, background_color='#ecf0f1', text_color='#2c3e50')],
        [sg.Text("", key='-MSG-', size=(30,1), text_color='#e74c3c', justification='center', pad=(0,10))],
        [sg.Button("ENTRAR ", key='-OK-', size=(20,1), button_color=('#ffffff', '#2980b9'), bind_return_key=True, font=('Arial', 10, 'bold'))],
        [sg.Text("ou", font=('Arial', 8))],
        [sg.Button("Criar nova conta", key='-REG-', size=(20,1), button_color=('white', '#7f8c8d'), border_width=0)]
    ]
    layout = [[sg.Column(col_layout, element_justification='center', pad=(20, 20))]]
    return sg.Window("Login", layout, finalize=True, element_justification='center', margins=(0,0))

def criar_janela_registo():
    layout = [
        [sg.Text(" Novo Registo", font=FONT_TITLE, pad=((0,0),(10,20)))],
        [sg.Text("ID (Login):", size=(10,1)), sg.Input(key='-NU-', focus=True)],
        [sg.Text("Password:", size=(10,1)), sg.Input(key='-NP-', password_char='●')],
        [sg.Text("Nome Real:", size=(10,1)), sg.Input(key='-NN-')],
        [sg.HSep(pad=(0,15))],
        [sg.Button("Salvar", size=(10,1), button_color='#27ae60'), sg.Push(), sg.Button("Cancelar", button_color='#c0392b')]
    ]
    return sg.Window("Registo de Utilizador", layout, modal=True, finalize=True)

def criar_janela_principal(nome_user):
    sg.set_options(font=FONT_TEXT)
    
    lista_graficos = [
        "1. Médias de Espera por Triagem", "2. Volume de Consultas", "3. Evolução da Fila",
        "4. Taxa de Ocupação Real", "5. Stress Test: Taxa Chegada", 
        "6. Atendimentos por Especialidade", "7. Eficiência: Esp. vs Reservas",
        "8. Evolução das Desistências"
    ]
    
    sidebar_content = [
        [sg.Text(" PAINEL DE CONTROLO", font=('Arial', 10, 'bold'), text_color='#f1c40f', background_color='#34495e')],
        [sg.HSep()],
        [sg.Frame(" Parâmetros da Simulação ", [
            [sg.Text("Nº Médicos:", size=(12,1)), sg.Input(str(Base.NUM_MEDICOS), key='-NUM_MED-', size=(8,1), justification='center')],
            [sg.Text("Chegada/h:", size=(12,1)), sg.Input(str(int(Base.TAXA_CHEGADA * 60)), key='-TAXA-', size=(8,1), justification='center')],
            [sg.Text("Tempo (min):", size=(12,1)), sg.Input(str(Base.TEMPO_SIMULACAO), key='-TEMPO-', size=(8,1), justification='center')],
            [sg.Text("Distribuição:", size=(9,1)), sg.Combo(["Exponencial", "Normal", "Uniforme"], key='-DIST-', default_value="Exponencial", size=(10,1), readonly=True)],
            [sg.VPush(background_color='#34495e')],
            [sg.Button(" EXECUTAR SIMULAÇÃO", key='-RUN-', size=BTN_SIZE_M, button_color=('#ffffff', '#27ae60'), font=('Arial', 10, 'bold'), pad=((0,0),(15,5)))]
        ], pad=((0,0),(10,20)), expand_x=True, background_color='#34495e', title_color='white',element_justification="center")],
        
        [sg.Frame(" Análise Visual ", [
            [sg.Text("Selecione o Indicador:", font=('Arial', 8), background_color='#34495e', text_color='white')],
            [sg.Combo(lista_graficos, key='-COMBO_GRAF-', size=(23, 1), readonly=True, default_value=lista_graficos[0])],
            [sg.Button("Ver Gráfico", key='-SHOW_GRAF-', size=BTN_SIZE_M, disabled=True, button_color=('#ffffff', '#2980b9'))]
        ], pad=((0,0),(0,20)), expand_x=True, background_color='#34495e', title_color='white')],
        

        [sg.Frame(" Relatórios Detalhados ", [
            [sg.Push(), sg.Button(" Log Completo", key='-LOG-', size=(23,1), disabled=True, pad=(0, 5)), sg.Push()],
            [sg.Push(), sg.Button(" Procurar Doente", key='-SEARCH-', size=(23,1), disabled=True, pad=(0, 5)), sg.Push()],
            [sg.Push(), sg.Button(" Performance Médicos", key='-TIME-', size=(23,1), disabled=True, pad=(0, 5)), sg.Push()]
        ], pad=((0,0),(0,20)), expand_x=True, background_color='#34495e', title_color='white')],
        
        [sg.VPush(background_color='#34495e')],
        [sg.Button(" SAIR DO SISTEMA", key='-EXIT-', size=BTN_SIZE_M, button_color=('#ffffff', '#c0392b'))]
    ]

    main_content = [
        [sg.Text("GESTÃO HOSPITALAR", font=('Helvetica', 24, 'bold'), text_color='#ecf0f1'), 
         sg.Push(), 
         sg.Text(f"Olá, {nome_user}!", font=('Arial', 24), text_color='#bdc3c7')],
        [sg.HSep(pad=((0,0),(0,20)))],
        [sg.Text(" STATUS DA OPERAÇÃO:", font=('Arial', 10, 'bold'), text_color='#2ecc71')],
        [sg.Multiline("O sistema está em standby.\nConfigure os parâmetros à esquerda e inicie a simulação...", 
                      key='-STATUS_BOX-', size=(70, 25), font=FONT_MONO, 
                      background_color='#2c3e50', text_color='#ecf0f1', 
                      border_width=2, autoscroll=True, disabled=True, expand_x=True, expand_y=True)],
        [sg.Text("Progresso:", font=('Arial', 8)), 
         sg.ProgressBar(100, orientation='h', size=(50, 10), key='-PROG-', bar_color=('#2ecc71', '#34495e'), expand_x=True)]
    ]

    layout = [
        [sg.Column(sidebar_content, key='-SIDEBAR-', element_justification='c', expand_y=True, background_color='#34495e', pad=0),
         sg.Column(main_content, expand_y=True, expand_x=True, pad=(20,20))]
    ]
    
    window = sg.Window("Simulação Hospitalar", layout, size=(1100, 700), finalize=True, resizable=True)
    
    if window['-SIDEBAR-'].Widget:
        window['-SIDEBAR-'].Widget.config(bg='#34495e')
        
    return window

def janela_log_popup(dados_lista):
    sg.theme('Default1') 
    colunas = [" Tempo (min) ", " Evento ", " Doente ", " Médico ", " Triagem "]
    
    layout = [
        [sg.Text(" HISTÓRICO DE EVENTOS", font=FONT_TITLE, pad=(0,10))],
        [sg.Table(values=dados_lista, headings=colunas, 
                  auto_size_columns=False, col_widths=[12, 15, 20, 20, 10],
                  justification='left', num_rows=25, alternating_row_color='#f1f2f6',
                  key='-TABLE-', row_height=25)],
        [sg.Button("Fechar Janela", size=(15,1), pad=(0,10))]
    ]
    win = sg.Window("Log Detalhado", layout, modal=True, resizable=True)
    win.read()
    win.close()
    sg.theme('DarkTeal9') 

def janela_medicos_popup(dados_tabela):
    sg.theme('Default1')
    colunas = [" Nome do Médico ", " Especialidade ", " T. Trab. (min) ", " Ocupação % "]
    
    layout = [
        [sg.Text(" PERFORMANCE DA EQUIPA MÉDICA", font=FONT_TITLE, text_color='#27ae60', pad=(0,10))],
        [sg.Table(values=dados_tabela, headings=colunas,
                  auto_size_columns=False, col_widths=[25, 20, 15, 12],
                  justification='center', num_rows=15, alternating_row_color='#e8f6f3',
                  row_height=25)],
        [sg.Button("Fechar", size=(10,1), pad=(0,10))]
    ]
    win = sg.Window("Métricas da Equipa", layout, modal=True, resizable=True)
    win.read()
    win.close()
    sg.theme('DarkTeal9')

def popup_procurar_doente():
    layout = [
        [sg.Text("Nome do Doente a pesquisar:", font=('Arial', 10))],
        [sg.Input(key='-NOME_SEARCH-', size=(30,1), focus=True)],
        [sg.Button("Pesquisar", bind_return_key=True), sg.Button("Cancelar")]
    ]
    window = sg.Window("Pesquisa", layout, modal=True, finalize=True)
    event, values = window.read()
    window.close()
    
    nome = None
    if event == "Pesquisar":
        nome = values['-NOME_SEARCH-']
    return nome