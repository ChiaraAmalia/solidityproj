import PySimpleGUI as sg
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
    window = sg.Window("Produttore", layout, modal=True,background_color="#1d8c3b", icon = impronta)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

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
            sg.Button("Entra",button_color="#013810",key="entra")
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
            window.close()
            window_trasformatore()
        if event == "entra" and values['PORTAFOGLIO'] == '0xed9d02e382b34818e88B88a309c7fe71E65f419d':
            window.close()
            window_produttore()
        if event == "entra" and values['PORTAFOGLIO'] == '0x0fBDc686b912d7722dc86510934589E0AAf3b55A':
            window.close()
            window_consumatore()
        # Folder name was filled in, make a list of files in the folder


    window.close()
