import PySimpleGUI as sg
import contract
import os
from web3 import exceptions, Web3

class ProdWin():

    def __init__(self,icona_impronta,LoginWin):
        self.impronta=icona_impronta
        self.LoginWin = LoginWin
        self.file_list_column = [
            [
                sg.Text("Finestra per il produttore:", key="finestra_produttore", background_color="#1d8c3b"),
            ],
            [
                sg.Button("Inserisci Materia Prima", button_color="#013810", key="addMP"),
            ],
        ]
        layout = [
            [
                sg.Column(self.file_list_column, background_color="#1d8c3b"),
            ]
        ]
        self.window = sg.Window("Produttore", layout,background_color="#1d8c3b", icon = icona_impronta)
        choice = None
        self.EventListener()

    
    def EventListener(self):
        while True:
            event, values = self.window.read()

            if event == "Exit" or event == sg.WIN_CLOSED:
                self.LoginWin.toggle_login()
                break
            if event == "addMP":
                win=sg.Window("Aggiungi Materia Prima",[
                    [sg.Text("Inserisci nome:    ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="NOMEMP",background_color="#8bd9a0")],
                    [sg.Text("Inserisci quantità: ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="QUANTMP", background_color="#8bd9a0")],
                    [sg.Text('',background_color="#1d8c3b",key='-Alert-')],
                    [sg.Text("Inserisci footprint: ",background_color="#1d8c3b"), sg.In(size=(30, 1), enable_events=True, key="FPMP", background_color="#8bd9a0")],
                    [sg.Text('',background_color="#1d8c3b",key='-Alert_1-')],
                    [sg.Button("inserisci",button_color="#013810", key="INSERISCI")]],modal=True,background_color="#1d8c3b",icon=self.impronta)
                while True:
                    event, values = win.read()
                    if event == "Exit" or event == sg.WIN_CLOSED:
                        break
                    if not values['QUANTMP'].isdigit():
                            win.Element('-Alert-').update("non è un numero")

                    if values['QUANTMP']=="":
                            win.Element('-Alert-').update("")

                    if values['QUANTMP'].isdigit():
                            win.Element('-Alert-').update("")

                    if not values['FPMP'].isdigit():
                            win.Element('-Alert_1-').update("non è un numero")

                    if values['FPMP']=="":
                            win.Element('-Alert_1-').update("")

                    if values['FPMP'].isdigit():
                            win.Element('-Alert_1-').update("")
                    if event == "INSERISCI" and not values['NOMEMP']=='' and values['QUANTMP'].isdigit() and values['FPMP'].isdigit():
                        try:
                            contract.inserisci_MP(values['NOMEMP'],int(values['QUANTMP']),int(values['FPMP']))
                        except exceptions.SolidityError as error:
                            sg.Popup(str(error).replace('execution reverted:','Si è cerificato il seguente errore:'),keep_on_top=True,background_color="#1d8c3b",icon=self.impronta)
                        else:
                            sg.Popup('Materia Inserita Correttamente', keep_on_top=True, background_color="#1d8c3b",icon=self.impronta)
                        win.Element('NOMEMP').update('')
                        win.Element('QUANTMP').update('')
                        win.Element('FPMP').update('')
                        #win.close()
                win.close()
        contract.w3.geth.personal.lock_account(contract.account[1])
        self.window.close()