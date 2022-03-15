import PySimpleGUI as sg
import contract
import os


path = os.path.abspath(os.path.dirname(__file__)) #Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
os.chdir(path)  # Cambio della cartella attuale nella cartella in cui si trova il file .py
impronta = os.path.join(path,'impronta.ico') #viene preso il file impronta.ico dalla cartella in cui si trovale il file .py in esecuzione

def window_trasformatore():
    file_list_column = [
        [
            sg.Text("Finestra per il trasformatore:", key="finestra_trasformatore", background_color="#1d8c3b"),
        ],
        [
            sg.Button("Acquista Materia Prima", button_color="#013810", key="acquista"),
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
            break
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
                [sg.Button("Acquista", button_color="#013810", key="ACQUISTA")]]
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

            while True:
                event, values = win.read()
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
                if event == "ACQUISTA" and values['-IN-'].isdigit():
                    contract.acquista_MP(mat_prim[win.Element('-LIST-').Widget.curselection()[0]],int(values['-IN-']))
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
            break

    window.close()

if __name__ == '__main__':
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

    window = sg.Window("Accedi al FootPrint Calculator", layout,background_color="#1d8c3b",icon=impronta)

    # Run the Event Loop
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "entra" and values['PORTAFOGLIO'] == '0xcA843569e3427144cEad5e4d5999a3D0cCF92B8e':
            window_trasformatore()
        if event == "entra" and values['PORTAFOGLIO'] == '0xed9d02e382b34818e88B88a309c7fe71E65f419d':
            window_produttore()
        if event == "entra" and values['PORTAFOGLIO'] == '0x0fBDc686b912d7722dc86510934589E0AAf3b55A':
            window_consumatore()
        # Folder name was filled in, make a list of files in the folder


    window.close()
