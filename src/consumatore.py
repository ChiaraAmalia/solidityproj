import PySimpleGUI as sg
import contract
import os
from web3 import exceptions, Web3

# in questa classe viene gestita la finestra relativa al consumatore

class ConsWin():

    #funzione utilizzata per inizializzare la finestra del consumatore con i relativi accessi alle funzionalità
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
        self.VediPWin = False
        self.vediLPWin  = False
        self.vediLPWin2 = False
        self.vediFPWin = False
        self.vediFPWin2 = False
        self.infoPWin1 = False
        self.acqPWin = False
        self.infoAPWin = False
        self.infoAPWin2 = False

    #funzione utilizzata per chiudere le relative finestre aperte quando scade la sessione di autenticazione
    def CloseWindow(self):
        if(getattr(self,'VediPWin')):
            self.VediPWin.close()

        if(getattr(self,'vediLPWin')):
            self.vediLPWin.close()
        if(getattr(self,'vediLPWin2')):
            self.vediLPWin2.close()

        if(getattr(self,'vediFPWin')):
            self.vediFPWin.close()
        if(getattr(self,'vediFPWin2')):
            self.vediFPWin2.close()

        if(getattr(self,'infoPWin')):
            self.infoPWin.close()
        if(getattr(self,'infoPWin1')):
            self.infoPWin1.close()
        
        if(getattr(self,'acqPWin')):
            self.acqPWin.close()

        if(getattr(self,'infoAPWin')):
            self.infoAPWin.close()
        if(getattr(self,'infoAPWin2')):
            self.infoAPWin2.close()

        self.window.close()

    #funzione utilizzata per vedere tutti i prodotti
    def VediP(self):
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
            self.VediPWin = sg.Window("Tutti Lotti Prodotti",laytot, modal=True,
                background_color="#1d8c3b", icon=self.icona_impronta)
            while True:
                event, values = self.VediPWin.read()
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
            self.VediPWin.close()
        except exceptions.SolidityError as error:
            sg.Popup(str(error).replace('execution reverted:','Si è cerificato il seguente errore:'),keep_on_top=True,background_color="#1d8c3b",icon=self.icona_impronta)           

    #funzione utilizzata per vedere tutti i lotti di un prodotto
    def vediLP(self):
        self.vediLPWin=sg.Window("Inserisci Nome Prodotto",[[sg.Text("Inserisci nome:    ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="NOMEP",background_color="#8bd9a0")],
                                                              [sg.Button("Vedi Lotti",button_color="#013810", key="LOTTI")]],modal=True,background_color="#1d8c3b",icon=self.icona_impronta)
        while True:
            event, values = self.vediLPWin.read()
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
                            self.vediLPWin2 = sg.Window("Tutti Lotti Prodotto",laytot, modal=True,background_color="#1d8c3b", icon=self.icona_impronta)
                            while True:
                                event, values = self.vediLPWin2.read()
                                if event == "Exit" or event == sg.WIN_CLOSED:
                                    break
                            self.vediLPWin2.close()
                        if(prod[0] == ""): #se il prodotto non viene trovato ma sono presenti altri lotti di altri prodotti
                            sg.Popup('Tale prodotto è inesistente',keep_on_top=True,background_color="#1d8c3b",icon=self.icona_impronta) 
                    if (prod == []): #se il prodotto non viene trovato e non sono presenti lotti
                        sg.Popup('Prodotto inesistente',keep_on_top=True,background_color="#1d8c3b",icon=self.icona_impronta)   
                except exceptions.SolidityError as error:
                    sg.Popup(str(error).replace('execution reverted:','Si è cerificato il seguente errore:'),keep_on_top=True,background_color="#1d8c3b",icon=self.icona_impronta)
        self.vediLPWin.close()

    #funzione per vedere il footprint totale di un prodotto finito
    def vediFP(self):
        self.vediFPWin=sg.Window("Inserisci Lotto Prodotto",[[sg.Text("Inserisci lotto:    ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="LOTTOP",background_color="#8bd9a0")],
                                                            [sg.Button("Vedi FootPrint",button_color="#013810", key="FP")]],modal=True,background_color="#1d8c3b",icon=self.icona_impronta)
        while True:
            event, values = self.vediFPWin.read()
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
                    self.vediFPWin2 = sg.Window("FootPrint Lotto Prodotto",laytot, modal=True,background_color="#1d8c3b", icon=self.icona_impronta)
                    while True:
                        event, values = self.vediFPWin2.read()
                        if event == "Exit" or event == sg.WIN_CLOSED:
                            break
                    self.vediFPWin2.close()
        self.vediFPWin.close()

    #funzione per vedere le informazioni associate a un relativo prodotto
    def infoP(self):
        self.infoPWin=sg.Window("Inserisci Lotto Prodotto",[
                    [sg.Text("Inserisci lotto:    ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="LOTTOP",background_color="#8bd9a0")],
                    [sg.Button("Vedi informazioni",button_color="#013810", key="INF")]],modal=True,background_color="#1d8c3b",icon=self.icona_impronta)
        while True:
            event, values = self.infoPWin.read()
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
                    self.infoPWin1 = sg.Window("Informazioni Prodotto",laytot, modal=True,background_color="#1d8c3b", icon=self.icona_impronta)
                    while True:
                        event, values = self.infoPWin1.read()
                        if event == "Exit" or event == sg.WIN_CLOSED:
                            break
                    self.infoPWin1.close()
        self.infoPWin.close()

    #funzione utilizzata per acquistare un prodotto
    def acqP(self):
        check = False
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
            self.acqPWin = sg.Window("Acquista Prodotto",laytot, modal=True,
                            background_color="#1d8c3b", icon=self.icona_impronta)
            while True:
                event, values = self.acqPWin.read()
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
                if not values['-IN-'].isdigit() or len(values['-IN-']) > 9:
                    self.acqPWin.Element('-Alert-').update("non è un numero")
                if values['-IN-']=="":
                    self.acqPWin.Element('-Alert-').update("")
                if values['-IN-'].isdigit() and len(values['-IN-']) <= 9:
                    self.acqPWin.Element('-Alert-').update("")
                if event == '-LIST-' and len(values['-LIST-']):
                    check = True
                    self.acqPWin.Element('-Nome-').update(contract.info_Prod_trasf(prod[self.acqPWin.Element('-LIST-').Widget.curselection()[0]])[2])
                    self.acqPWin.Element('-QuantDisp-').update(contract.info_Prod_trasf(prod[self.acqPWin.Element('-LIST-').Widget.curselection()[0]])[5])
                    self.acqPWin.Element('-FootPrint-').update(contract.info_Prod_trasf(prod[self.acqPWin.Element('-LIST-').Widget.curselection()[0]])[6])
                if event == "ACQUISTA" and values['-IN-'].isdigit() and len(values['-IN-']) <= 9 and check:
                    try:
                        contract.acquista_Prod(prod[self.acqPWin.Element('-LIST-').Widget.curselection()[0]],int(values['-IN-']))
                        sg.Popup('Acquisto Completato', keep_on_top=True, background_color="#1d8c3b",icon=self.icona_impronta)
                    except exceptions.SolidityError as error:
                        sg.Popup(str(error).replace('execution reverted:','Si è cerificato il seguente errore:'), keep_on_top=True, background_color="#1d8c3b",icon=self.icona_impronta)
            self.acqPWin.close()
    
    #funzione utilizzata per visualizzare le informazioni relative ad un prodotto acquistato
    def infoAP(self):
        self.infoAPWin=sg.Window("Inserisci Lotto Prodotto Acquistato",[
                [sg.Text("Inserisci lotto:    ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="LOTTOP",background_color="#8bd9a0")],
                [sg.Button("Vedi informazioni",button_color="#013810", key="INF")]],modal=True,background_color="#1d8c3b",icon=self.icona_impronta)
        while True:
            event, values = self.infoAPWin.read()
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
                    self.infoAPWin2 = sg.Window("Informazioni Prodotto Acquistato",laytot, modal=True,background_color="#1d8c3b", icon=self.icona_impronta)
                    while True:
                        event, values = self.infoAPWin2.read()
                        if event == "Exit" or event == sg.WIN_CLOSED:
                            break
                    self.infoAPWin2.close()
        self.infoAPWin.close()

    #questa funzione viene utilizzata per gestire l'apertura delle finestre richieste dal consumatore
    #quando l'utente chiude la finestra iniziale del consumatore, viene terminata la sessione e bloccato l'account
    def ListenEvent(self):
        while True:
            event, values = self.window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                self.LoginWin.toggle_login()
                break 
            if event == "vediP":
                self.VediP()
            if event == "vediLP":
                self.vediLP()
            if event == "vediFP":
                self.vediFP()
            if event == "infoP":
                self.infoP()
            if event == "acqP":
                self.acqP()
            if event == "infoAP":
                self.infoAP()
        contract.w3.geth.personal.lock_account(contract.account[3])
        self.window.close()
