from pickle import FALSE
import PySimpleGUI as sg
import contract
import os
from web3 import exceptions

path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
impronta = os.path.join(path,'impronta.ico') #viene preso il file impronta.ico dalla cartella in cui si trovale il file .py in esecuzione
nexttoggle = True #Toggle della finestra "Login" per disattivare/attivare dopo login/logout
file_list_column = [
    [
        sg.Text("Inserisci indirizzo di portafoglio:",background_color="#1d8c3b"),
        sg.In(size=(58, 1), enable_events=True, key="PORTAFOGLIO",background_color="#8bd9a0"),
    ],
    [
        sg.Button("Entra",button_color="#013810",key="entra",bind_return_key=True)
    ],
]
# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column,background_color="#1d8c3b"),
    ]
]
windowLogin = sg.Window("Accedi al FootPrint Calculator", layout,background_color="#1d8c3b",icon=impronta)


def window_trasformatore():
    file_list_column = [
        [
            sg.Text("Finestra per il trasformatore:", key="finestra_trasformatore", background_color="#1d8c3b"),
        ],
        [
            sg.Button("Vedi Tutte Materie Prime", button_color="#013810", key="tutteMP"),
            sg.Button("Vedi Lotti Materia Prima", button_color="#013810", key="lottiMP"),
            sg.Button("Vedi Informazioni Materia Prima", button_color="#013810", key="infoMP"),
            sg.Button("Acquista Materia Prima", button_color="#013810", key="acquista"),
            sg.Button("Dettagli Materia Prima Acquistata", button_color="#013810", key="dettagliMP"),
            sg.Button("Aggiungi Prodotto Finito", button_color="#013810", key="aggProd"),
        ],
    ]
    layout = [
        [
            sg.Column(file_list_column, background_color="#1d8c3b"),
        ]
    ]
    window = sg.Window("Trasformatore", layout, modal=True,background_color="#1d8c3b", icon =impronta)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            toggle_login()
            break
        if event == "tutteMP":
            try:
                mat_prim = contract.tutti_MP_lotti()
                file_list_column = [
                    [sg.Text('Lotti Materie Prime',background_color="#1d8c3b")],
                    [sg.Listbox(mat_prim, size=(20, 12), key='-LIST-', enable_events=True)]
                ]
                laytot = [
                    [
                        sg.Column(file_list_column, background_color="#1d8c3b")
                    ]
                ]
                win = sg.Window("Tutti Lotti Materie Prime",laytot, modal=True,
                    background_color="#1d8c3b", icon=impronta)
                while True:
                    event, values = win.read()
                    if event == "Exit" or event == sg.WIN_CLOSED:
                        break
                win.close()
            except exceptions.SolidityError as error:
                sg.Popup(str(error).replace('execution reverted:','Si è cerificato il seguente errore:'),keep_on_top=True,background_color="#1d8c3b",icon=impronta)
        if event == "lottiMP":
            win=sg.Window("Inserisci Nome Materia Prima",[[sg.Text("Inserisci nome:    ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="NOMEMP",background_color="#8bd9a0")],
                                                          [sg.Button("Vedi Lotti",button_color="#013810", key="LOTTI")]],modal=True,background_color="#1d8c3b",icon=impronta)
            while True:
                event, values = win.read()
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
                if event == "LOTTI" and not values['NOMEMP']=='':
                    mat_prim = contract.lotti_MP(values['NOMEMP'])
                    file_list_column = [
                        [sg.Text('Lotti Materia Prima',background_color="#1d8c3b")],
                        [sg.Listbox(mat_prim, size=(20, 12), key='-LIST-', enable_events=True)]
                    ]
                    laytot = [
                        [
                            sg.Column(file_list_column, background_color="#1d8c3b")
                        ]
                    ]
                    wind = sg.Window("Tutti Lotti Materia Prima",laytot, modal=True,background_color="#1d8c3b", icon=impronta)
                    while True:
                        event, values = wind.read()
                        if event == "Exit" or event == sg.WIN_CLOSED:
                            break
                    wind.close()
            win.close()
        if event == "infoMP":
            win=sg.Window("Inserisci Lotto Materia Prima",[[sg.Text("Inserisci lotto:    ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="LOTTOMP",background_color="#8bd9a0")],
                                                          [sg.Button("Vedi informazioni",button_color="#013810", key="INF")]],modal=True,background_color="#1d8c3b",icon=impronta)
            while True:
                event, values = win.read()
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
                if event == "INF" and not values['LOTTOMP']=='':
                    
                    file_list_column = [
                        [sg.Text('Caratteristiche:',background_color="#1d8c3b")],
                        [sg.Text('Nome:',background_color="#1d8c3b")],
                        [sg.Text(contract.info_MP_prod(values['LOTTOMP'])[2],background_color="#1d8c3b",key='-Nome-')],
                        [sg.Text('IndirizzoProduttore:', background_color="#1d8c3b")],
                        [sg.Text(contract.info_MP_prod(values['LOTTOMP'])[3], background_color="#1d8c3b", key='-IndirizzoProduttore-')],
                        [sg.Text('Quantità disponibile:', background_color="#1d8c3b")],
                        [sg.Text(contract.info_MP_prod(values['LOTTOMP'])[4], background_color="#1d8c3b", key='-Quantita-')],
                        [sg.Text('FootPrint:', background_color="#1d8c3b")],
                        [sg.Text(contract.info_MP_prod(values['LOTTOMP'])[5], background_color="#1d8c3b", key='-FootPrint-')]
                    ]
                
                    laytot = [
                        [
                            sg.Column(file_list_column, background_color="#1d8c3b")
                        ]
                    ]
                    wind = sg.Window("Informazioni Materia Prima",laytot, modal=True,background_color="#1d8c3b", icon=impronta)
                    while True:
                        event, values = wind.read()
                        if event == "Exit" or event == sg.WIN_CLOSED:
                            break
                    wind.close()
            win.close()
        if event == "acquista":
            mat_prim = contract.tutti_MP_lotti()

            col_sin=[[sg.Text('Seleziona una materia prima',background_color="#1d8c3b")],
                [sg.Listbox(mat_prim, size=(20, 12), key='-LIST-', enable_events=True)],
                [sg.Text('Quantità:', background_color="#1d8c3b"),sg.In(size=(10, 1), enable_events=True,background_color="#8bd9a0",key='-IN-')],
                [sg.Text('',background_color="#1d8c3b",key='-Alert-')]]
            col_des=[[sg.Text('Caratteristiche:',background_color="#1d8c3b")],
                     [sg.Text('Nome:',background_color="#1d8c3b")],
                     [sg.Text('',background_color="#1d8c3b",key='-Nome-')],
                     [sg.Text('FootPrint:', background_color="#1d8c3b")],
                     [sg.Text('', background_color="#1d8c3b", key='-FootPrint-')],
                [sg.Button("Acquista", button_color="#013810", key='ACQUISTA')]]
            laytot=[[sg.Column(col_sin, element_justification='c',background_color="#1d8c3b"),sg.VSeperator(),sg.Column(col_des, element_justification='c',background_color="#1d8c3b")]]
            win = sg.Window("Acquista Materia Prima",laytot, modal=True,
                            background_color="#1d8c3b", icon=impronta)
            while True:
                event, values = win.read()
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
                if not values['-IN-'].isdigit():
                    win.Element('-Alert-').update("non è un numero")

                if values['-IN-']=="":
                    win.Element('-Alert-').update("")

                if values['-IN-'].isdigit():
                    win.Element('-Alert-').update("")

                if event == '-LIST-' and len(values['-LIST-']):
                    win.Element('-Nome-').update(contract.info_MP_prod(mat_prim[win.Element('-LIST-').Widget.curselection()[0]])[2])
                    win.Element('-FootPrint-').update(contract.info_MP_prod(mat_prim[win.Element('-LIST-').Widget.curselection()[0]])[5])
    
                if event == "ACQUISTA" and values['-IN-'].isdigit():
                    try:
                        contract.acquista_MP(mat_prim[win.Element('-LIST-').Widget.curselection()[0]],int(values['-IN-']))
                        sg.Popup('Acquisto Completato', keep_on_top=True, background_color="#1d8c3b",icon=impronta)
                    except exceptions.SolidityError as error:
                        sg.Popup(str(error).replace('execution reverted:','Si è cerificato il seguente errore:'), keep_on_top=True, background_color="#1d8c3b",icon=impronta)
            win.close()
        if event == "dettagliMP":
            win=sg.Window("Inserisci Lotto Materia Prima Acquistata",[[sg.Text("Inserisci lotto:    ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="LOTTOMP",background_color="#8bd9a0")],
                                                           [sg.Button("Vedi informazioni",button_color="#013810", key="INF")]],modal=True,background_color="#1d8c3b",icon=impronta)
            while True:
                event, values = win.read()
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
                if event == "INF" and not values['LOTTOMP']=='':
                    
                    file_list_column = [
                        [sg.Text('Caratteristiche:',background_color="#1d8c3b")],
                        [sg.Text('Nome:',background_color="#1d8c3b")],
                        [sg.Text(contract.info_MP_acq(values['LOTTOMP'])[2],background_color="#1d8c3b",key='-Nome-')],
                        [sg.Text('Quantità disponibile:', background_color="#1d8c3b")],
                        [sg.Text(contract.info_MP_acq(values['LOTTOMP'])[4], background_color="#1d8c3b", key='-Quantita-')],
                        [sg.Text('FootPrint:', background_color="#1d8c3b")],
                        [sg.Text(contract.info_MP_acq(values['LOTTOMP'])[5], background_color="#1d8c3b", key='-FootPrint-')]
                    ]
                
                    laytot = [
                        [
                            sg.Column(file_list_column, background_color="#1d8c3b")
                        ]
                    ]
                    wind = sg.Window("Informazioni Materia Prima Acquistata",laytot, modal=True,background_color="#1d8c3b", icon=impronta)
                    while True:
                        event, values = wind.read()
                        if event == "Exit" or event == sg.WIN_CLOSED:
                            break
                    wind.close()
            win.close()
    window.close()

def window_produttore():
    file_list_column = [
        [
            sg.Text("Finestra per il produttore:", key="finestra_produttore", background_color="#1d8c3b"),
        ],
        [
            sg.Button("Inserisci Materia Prima", button_color="#013810", key="addMP"),
        ],
    ]
    layout = [
        [
            sg.Column(file_list_column, background_color="#1d8c3b"),
        ]
    ]
    window = sg.Window("Produttore", layout,background_color="#1d8c3b", icon = impronta)
    choice = None
    while True:
        event, values = window.read()
        
        if event == "Exit" or event == sg.WIN_CLOSED:
            toggle_login()
            break
        if event == "addMP":
            win=sg.Window("Aggiungi Materia Prima",[
                [sg.Text("Inserisci nome:    ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="NOMEMP",background_color="#8bd9a0")],
                [sg.Text("Inserisci quantità: ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="QUANTMP", background_color="#8bd9a0")],
                [sg.Text("Inserisci footprint: ",background_color="#1d8c3b"), sg.In(size=(30, 1), enable_events=True, key="FPMP", background_color="#8bd9a0")],
                [sg.Button("inserisci",button_color="#013810", key="INSERISCI")]],modal=True,background_color="#1d8c3b",icon=impronta)
            while True:
                event, values = win.read()
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
                if event == "INSERISCI" and not values['NOMEMP']=='' and values['QUANTMP'].isdigit() and values['FPMP'].isdigit():
                    contract.inserisci_MP(values['NOMEMP'],int(values['QUANTMP']),int(values['FPMP']))
                    win.Element('NOMEMP').update('')
                    win.Element('QUANTMP').update('')
                    win.Element('FPMP').update('')
                    sg.Popup('Materia Inserita Correttamente', keep_on_top=True,background_color="#1d8c3b",icon = impronta)
            win.close()
    window.close()

def window_consumatore():
    file_list_column = [
        [
            sg.Text("Finestra per il consumatore:", key="finestra_consumatore", background_color="#1d8c3b"),
        ],
        [
            sg.Button("Vedi footprint Prodotto", button_color="#013810", key="vediFP")
        ],
    ]
    layout = [
        [
            sg.Column(file_list_column, background_color="#1d8c3b"),
        ]
    ]
    window = sg.Window("Consumatore", layout, modal=True,background_color="#1d8c3b",icon= impronta)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            toggle_login()
            break

    window.close()


def toggle_login():
    global nexttoggle
    windowLogin['entra'].update(disabled=nexttoggle)
    windowLogin['PORTAFOGLIO'].update(disabled=nexttoggle)
    nexttoggle = not nexttoggle

if __name__ == '__main__':

    # Run the Event Loop
    while True:
        event, values = windowLogin.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "entra":
            contract.current_user = values['PORTAFOGLIO']
            toggle_login()
            if values['PORTAFOGLIO'] == contract.trasf:
                window_trasformatore()
            elif values['PORTAFOGLIO'] == contract.prod:
                window_produttore()
            elif values['PORTAFOGLIO'] == contract.consum:
                window_consumatore()
            else: sg.Popup('Non hai inserito un indirizzo valido', keep_on_top=True,background_color="#1d8c3b",icon = impronta), toggle_login()
            
        print(values['PORTAFOGLIO'])
        # Folder name was filled in, make a list of files in the folder


    windowLogin.close()
