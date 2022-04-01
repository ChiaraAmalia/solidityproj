import PySimpleGUI as sg
import contract
import os
from web3 import exceptions, Web3

class ConsWin():

    def __init__(self,icona_impronta,LoginWin):
        self.icona_impronta = icona_impronta
        self.LoginWin = LoginWin
        file_list_column = [
            [
                sg.Text("Finestra per il consumatore:", key="finestra_consumatore", background_color="#1d8c3b"),
            ],
            [
                sg.Button("Vedi tutti i Prodotti", button_color="#013810", key="vediP"),
                sg.Button("Vedi Lotti Prodotto", button_color="#013810", key="vediLP"),
                sg.Button("Vedi FootPrint Lotto Prodotto", button_color="#013810", key="vediFP"),
                sg.Button("Vedi Informazioni Prodotto", button_color="#013810", key="infoP"),
                sg.Button("Acquista Prodotto", button_color="#013810", key="acqP"),
                sg.Button("Vedi informazioni Prodotto acquistato", button_color="#013810", key="infoAP")
            ],
        ]
        layout = [
            [
                sg.Column(file_list_column, background_color="#1d8c3b"),
            ]
        ]
        self.window = sg.Window("Consumatore", layout, modal=True,background_color="#1d8c3b",icon= self.icona_impronta)
        self.choice = None
        self.EventListening()

    def EventListening(self):
        while True:
            event, values = self.window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                self.LoginWin.toggle_login()
                break 
            if event == "vediP":
                try:
                    mat_prim = contract.tutti_Prod_lotti()
                    file_list_column = [
                        [sg.Text('Lotti Prodotti',background_color="#1d8c3b")],
                        [sg.Listbox(mat_prim, size=(20, 12), key='-LIST-', enable_events=True)]
                    ]
                    laytot = [
                        [
                            sg.Column(file_list_column, background_color="#1d8c3b")
                        ]
                    ]
                    win = sg.Window("Tutti Lotti Prodotti",laytot, modal=True,
                        background_color="#1d8c3b", icon=self.icona_impronta)
                    while True:
                        event, values = win.read()
                        if event == "Exit" or event == sg.WIN_CLOSED:
                            break
                    win.close()
                except exceptions.SolidityError as error:
                    sg.Popup(str(error).replace('execution reverted:','Si è cerificato il seguente errore:'),keep_on_top=True,background_color="#1d8c3b",icon=self.icona_impronta)           
            if event == "vediLP":
                win=sg.Window("Inserisci Nome Prodotto",[[sg.Text("Inserisci nome:    ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="NOMEP",background_color="#8bd9a0")],
                                                              [sg.Button("Vedi Lotti",button_color="#013810", key="LOTTI")]],modal=True,background_color="#1d8c3b",icon=self.icona_impronta)
                while True:
                    event, values = win.read()
                    if event == "Exit" or event == sg.WIN_CLOSED:
                        break

                    if event == "LOTTI" and values['NOMEP']=='':
                        sg.Popup("Non hai inserito un prodotto",keep_on_top=True,background_color="#1d8c3b",icon=self.icona_impronta)

                    if event == "LOTTI" and not values['NOMEP']=='':
                        try:
                            prod = contract.lotti_Prod(values['NOMEP'])
                            if (prod != []):
                                if(prod[0] != ""):
                                    file_list_column = [
                                        [sg.Text('Lotti Prodotto',background_color="#1d8c3b")],
                                        [sg.Listbox(prod, size=(20, 12), key='-LIST-', enable_events=True)]
                                        ]
                                    laytot = [
                                        [
                                            sg.Column(file_list_column, background_color="#1d8c3b")
                                        ]
                                        ]
                                    wind = sg.Window("Tutti Lotti Prodotto",laytot, modal=True,background_color="#1d8c3b", icon=self.icona_impronta)
                                    while True:
                                        event, values = wind.read()
                                        if event == "Exit" or event == sg.WIN_CLOSED:
                                            break
                                    wind.close()
                                if(prod[0] == ""):
                                    sg.Popup('Tale prodotto è inesistente',keep_on_top=True,background_color="#1d8c3b",icon=self.icona_impronta) 
                            if (prod == []):
                                sg.Popup('Prodotto inesistente',keep_on_top=True,background_color="#1d8c3b",icon=self.icona_impronta)   
                        except exceptions.SolidityError as error:
                            sg.Popup(str(error).replace('execution reverted:','Si è cerificato il seguente errore:'),keep_on_top=True,background_color="#1d8c3b",icon=self.icona_impronta)
                win.close()
            if event == "vediFP":
                win=sg.Window("Inserisci Lotto Prodotto",[[sg.Text("Inserisci lotto:    ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="LOTTOP",background_color="#8bd9a0")],
                                                            [sg.Button("Vedi FootPrint",button_color="#013810", key="FP")]],modal=True,background_color="#1d8c3b",icon=self.icona_impronta)
                while True:
                    event, values = win.read()
                    if event == "Exit" or event == sg.WIN_CLOSED:
                        break
                    if event == "FP" and values['LOTTOP']=='':
                        sg.Popup("Non hai inserito un lotto",keep_on_top=True,background_color="#1d8c3b",icon=self.icona_impronta)
                    if event == "FP" and not values['LOTTOP']=='':
                        try:
                            contract.footprint_Prod(values['LOTTOP'])
                        except exceptions.SolidityError as error:
                            sg.Popup(str(error).replace('execution reverted:','Si è cerificato il seguente errore:'),keep_on_top=True,background_color="#1d8c3b",icon=self.icona_impronta)
                        else:
                            file_list_column = [
                                [sg.Text(contract.footprint_Prod(values['LOTTOP']),background_color="#1d8c3b",key='FootPrint')],
                            ]

                            laytot = [
                                [
                                    sg.Column(file_list_column, background_color="#1d8c3b")
                                ]
                            ]
                            wind = sg.Window("FootPrint Lotto Prodotto",laytot, modal=True,background_color="#1d8c3b", icon=self.icona_impronta)
                            while True:
                                event, values = wind.read()
                                if event == "Exit" or event == sg.WIN_CLOSED:
                                    break
                            wind.close()
                win.close()
            if event == "infoP":
                win=sg.Window("Inserisci Lotto Prodotto",[
                    [sg.Text("Inserisci lotto:    ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="LOTTOP",background_color="#8bd9a0")],
                    [sg.Button("Vedi informazioni",button_color="#013810", key="INF")]],modal=True,background_color="#1d8c3b",icon=self.icona_impronta)
                while True:
                    event, values = win.read()
                    if event == "Exit" or event == sg.WIN_CLOSED:
                        break
                    if event == "INF" and values['LOTTOP']=='':
                        sg.Popup("Non hai inserito un lotto",keep_on_top=True,background_color="#1d8c3b",icon=self.icona_impronta)
                    if event == "INF" and not values['LOTTOP']=='':
                        try:
                            contract.info_Prod_trasf(values['LOTTOP'])
                        except exceptions.SolidityError as error:
                                sg.Popup(str(error).replace('execution reverted:','Si è cerificato il seguente errore:'), keep_on_top=True, background_color="#1d8c3b",icon=self.icona_impronta)
                        else:
                            file_list_column = [
                                [sg.Text('Caratteristiche:',background_color="#1d8c3b")],
                                [sg.Text('Nome:',background_color="#1d8c3b")],
                                [sg.Text(contract.info_Prod_trasf(values['LOTTOP'])[2],background_color="#1d8c3b",key='-Nome-')],
                                [sg.Text('Indirizzo Trasformatore:', background_color="#1d8c3b")],
                                [sg.Text(contract.info_Prod_trasf(values['LOTTOP'])[3], background_color="#1d8c3b", key='-IndirizzoTrasformatore-')],
                                [sg.Text('Quantità disponibile:', background_color="#1d8c3b")],
                                [sg.Text(contract.info_Prod_trasf(values['LOTTOP'])[5], background_color="#1d8c3b", key='-Quantita-')],
                                [sg.Text('FootPrint:', background_color="#1d8c3b")],
                                [sg.Text(contract.info_Prod_trasf(values['LOTTOP'])[6], background_color="#1d8c3b", key='-FootPrint-')]
                            ]

                            laytot = [
                                [
                                    sg.Column(file_list_column, background_color="#1d8c3b")
                                ]
                            ]
                            wind = sg.Window("Informazioni Prodotto",laytot, modal=True,background_color="#1d8c3b", icon=self.icona_impronta)
                            while True:
                                event, values = wind.read()
                                if event == "Exit" or event == sg.WIN_CLOSED:
                                    break
                            wind.close()
                win.close()
            if event == "acqP":
                try:
                    prod = contract.tutti_Prod_lotti()
                except exceptions.SolidityError as error:
                    sg.Popup(str(error).replace('execution reverted:','Si è cerificato il seguente errore:'),keep_on_top=True,background_color="#1d8c3b",icon=self.icona_impronta)
                else:
                    col_sin=[[sg.Text('Seleziona un prodotto',background_color="#1d8c3b")],
                        [sg.Listbox(prod, size=(20, 12), key='-LIST-', enable_events=True)],
                        [sg.Text('Quantità:', background_color="#1d8c3b"),sg.In(size=(10, 1), enable_events=True,background_color="#8bd9a0",key='-IN-')],
                        [sg.Text('',background_color="#1d8c3b",key='-Alert-')]]
                    col_des=[[sg.Text('Caratteristiche:',background_color="#1d8c3b")],
                            [sg.Text('Nome:',background_color="#1d8c3b")],
                            [sg.Text('',background_color="#1d8c3b",key='-Nome-')],
                            [sg.Text('Quantità disponibile:',background_color="#1d8c3b")],
                            [sg.Text('',background_color="#1d8c3b",key='-QuantDisp-')],
                            [sg.Text('FootPrint:', background_color="#1d8c3b")],
                            [sg.Text('', background_color="#1d8c3b", key='-FootPrint-')],
                        [sg.Button("Acquista", button_color="#013810", key='ACQUISTA')]]
                    laytot=[
                            [sg.Column(col_sin, element_justification='c',background_color="#1d8c3b"),sg.VSeperator(),sg.Column(col_des, element_justification='c',background_color="#1d8c3b")]
                        ]
                    win = sg.Window("Acquista Prodotto",laytot, modal=True,
                                    background_color="#1d8c3b", icon=self.icona_impronta)
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
                            win.Element('-Nome-').update(contract.info_Prod_trasf(prod[win.Element('-LIST-').Widget.curselection()[0]])[2])
                            win.Element('-QuantDisp-').update(contract.info_Prod_trasf(prod[win.Element('-LIST-').Widget.curselection()[0]])[5])
                            win.Element('-FootPrint-').update(contract.info_Prod_trasf(prod[win.Element('-LIST-').Widget.curselection()[0]])[6])

                        if event == "ACQUISTA" and values['-IN-'].isdigit():
                            try:
                                contract.acquista_Prod(prod[win.Element('-LIST-').Widget.curselection()[0]],int(values['-IN-']))
                                sg.Popup('Acquisto Completato', keep_on_top=True, background_color="#1d8c3b",icon=self.icona_impronta)
                            except exceptions.SolidityError as error:
                                sg.Popup(str(error).replace('execution reverted:','Si è cerificato il seguente errore:'), keep_on_top=True, background_color="#1d8c3b",icon=self.icona_impronta)
                    win.close()
            if event == "infoAP":
                win=sg.Window("Inserisci Lotto Prodotto Acquistato",[
                [sg.Text("Inserisci lotto:    ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="LOTTOP",background_color="#8bd9a0")],
                [sg.Button("Vedi informazioni",button_color="#013810", key="INF")]],modal=True,background_color="#1d8c3b",icon=self.icona_impronta)
                while True:
                    event, values = win.read()
                    if event == "Exit" or event == sg.WIN_CLOSED:
                        break
                    if event == "INF" and values['LOTTOP']=='':
                        sg.Popup("Non hai inserito un lotto",keep_on_top=True,background_color="#1d8c3b",icon=self.icona_impronta)
                    if event == "INF" and not values['LOTTOP']=='':
                        try:
                            contract.info_Prod_acq(values['LOTTOP'])
                        except exceptions.SolidityError as error:
                                sg.Popup(str(error).replace('execution reverted:','Si è cerificato il seguente errore:'), keep_on_top=True, background_color="#1d8c3b",icon=self.icona_impronta)
                        else:
                            file_list_column = [
                                [sg.Text('Caratteristiche:',background_color="#1d8c3b")],
                                [sg.Text('Lotto:',background_color="#1d8c3b")],
                                [sg.Text(contract.info_Prod_acq(values['LOTTOP'])[1],background_color="#1d8c3b",key='-Nome-')],
                                [sg.Text('Quantità disponibile:', background_color="#1d8c3b")],
                                [sg.Text(contract.info_Prod_acq(values['LOTTOP'])[2], background_color="#1d8c3b", key='-Quantita-')],
                            ]

                            laytot = [
                                [
                                    sg.Column(file_list_column, background_color="#1d8c3b")
                                ]
                            ]
                            wind = sg.Window("Informazioni Prodotto Acquistato",laytot, modal=True,background_color="#1d8c3b", icon=self.icona_impronta)
                            while True:
                                event, values = wind.read()
                                if event == "Exit" or event == sg.WIN_CLOSED:
                                    break
                            wind.close()
                win.close()                   
        self.window.close()
