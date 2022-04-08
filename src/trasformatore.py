import PySimpleGUI as sg
import contract
import os
from web3 import exceptions, Web3

class TrasfWin():
    def __init__(self,icona_impronta,LoginWin):
        self.LoginWin = LoginWin
        self.icona = icona_impronta
        file_list_column = [
            [
                sg.Text("Finestra per il trasformatore:", key="finestra_trasformatore", background_color="#1d8c3b"),
            ],
            [
                sg.Button("Vedi Tutte le Materie Prime", button_color="#013810", key="tutteMP"),
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
        self.window = sg.Window("Trasformatore", layout, modal=True,background_color="#1d8c3b", icon =self.icona)
        choice = None

    def tutteMP(self):
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
            self.TutteMPWin = sg.Window("Tutti Lotti Materie Prime",laytot, modal=True,
                background_color="#1d8c3b", icon=self.icona)
            while True:
                event, values = self.TutteMPWin.read()
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
            self.TutteMPWin.close()
        except exceptions.SolidityError as error:
            sg.Popup(str(error).replace('execution reverted:','Si è cerificato il seguente errore:'),keep_on_top=True,background_color="#1d8c3b",icon=self.icona)

    def lottiMP(self):
        self.LottiMPwin=sg.Window("Inserisci Nome Materia Prima",[[sg.Text("Inserisci nome:    ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="NOMEMP",background_color="#8bd9a0")],
                                                              [sg.Button("Vedi Lotti",button_color="#013810", key="LOTTI")]],modal=True,background_color="#1d8c3b",icon=self.icona)
        while True:
            event, values = self.LottiMPwin.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            if event == "LOTTI" and values['NOMEMP']=='':
                sg.Popup("Non hai inserito una materia prima",keep_on_top=True,background_color="#1d8c3b",icon=self.icona)
            if event == "LOTTI" and not values['NOMEMP']=='':
                try:
                    mat_prim = contract.lotti_MP(values['NOMEMP'])
                    if (mat_prim != []):
                        if(mat_prim[0] != ""):
                            file_list_column = [
                                [sg.Text('Lotti Materia Prima',background_color="#1d8c3b")],
                                [sg.Listbox(mat_prim, size=(20, 12), key='-LIST-', enable_events=True)]
                                ]
                            laytot = [
                                [
                                    sg.Column(file_list_column, background_color="#1d8c3b")
                                ]
                                ]
                            wind = sg.Window("Tutti Lotti Materia Prima",laytot, modal=True,background_color="#1d8c3b", icon=self.icona)
                            while True:
                                event, values = wind.read()
                                if event == "Exit" or event == sg.WIN_CLOSED:
                                    break
                            wind.close()
                        if(mat_prim[0] == ""):
                            sg.Popup('Tale materia prima è inesistente',keep_on_top=True,background_color="#1d8c3b",icon=self.icona) 
                    if (mat_prim == []):
                        sg.Popup('Materia prima inesistente',keep_on_top=True,background_color="#1d8c3b",icon=self.icona)   
                except exceptions.SolidityError as error:
                    sg.Popup(str(error).replace('execution reverted:','Si è cerificato il seguente errore:'),keep_on_top=True,background_color="#1d8c3b",icon=self.icona)
        self.LottiMPwin.close()

    def infoMP(self):
        self.infoMPWin=sg.Window("Inserisci Lotto Materia Prima",[[sg.Text("Inserisci lotto:    ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="LOTTOMP",background_color="#8bd9a0")],
                                                              [sg.Button("Vedi informazioni",button_color="#013810", key="INF")]],modal=True,background_color="#1d8c3b",icon=self.icona)
        while True:
            event, values = self.infoMPWin.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            if event == "INF" and values['LOTTOMP']=='':
                sg.Popup("Non hai inserito un lotto",keep_on_top=True,background_color="#1d8c3b",icon=self.icona)
            if event == "INF" and not values['LOTTOMP']=='':
                try:
                    contract.info_MP_prod(values['LOTTOMP'])
                except exceptions.SolidityError as error:
                    sg.Popup(str(error).replace('execution reverted:','Si è cerificato il seguente errore:'),keep_on_top=True,background_color="#1d8c3b",icon=self.icona)
                else:
                    file_list_column = [
                        [sg.Text('Caratteristiche:',background_color="#1d8c3b")],
                        [sg.Text('Nome:',background_color="#1d8c3b")],
                        [sg.Text(contract.info_MP_prod(values['LOTTOMP'])[2],background_color="#1d8c3b",key='-Nome-')],
                        [sg.Text('Indirizzo Produttore:', background_color="#1d8c3b")],
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
                    wind = sg.Window("Informazioni Materia Prima",laytot, modal=True,background_color="#1d8c3b", icon=self.icona)
                    while True:
                        event, values = wind.read()
                        if event == "Exit" or event == sg.WIN_CLOSED:
                            break
                    wind.close()
        self.infoMPWin.close()
    
    def Acquista(self):
        try:
            mat_prim = contract.tutti_MP_lotti()
        except exceptions.SolidityError as error:
            sg.Popup(str(error).replace('execution reverted:','Si è cerificato il seguente errore:'),keep_on_top=True,background_color="#1d8c3b",icon=self.icona)
        else:
            col_sin=[[sg.Text('Seleziona una materia prima',background_color="#1d8c3b")],
                [sg.Listbox(mat_prim, size=(20, 12), key='-LIST-', enable_events=True)],
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
            self.AcquistaWin = sg.Window("Acquista Materia Prima",laytot, modal=True,
                            background_color="#1d8c3b", icon=self.icona)
            while True:
                event, values = self.AcquistaWin.read()
                if event == "Exit" or event == sg.WIN_CLOSED:
                    break
                if not values['-IN-'].isdigit():
                    self.AcquistaWin.Element('-Alert-').update("non è un numero")
                if values['-IN-']=="":
                    self.AcquistaWin.Element('-Alert-').update("")
                if values['-IN-'].isdigit():
                    self.AcquistaWin.Element('-Alert-').update("")
                if event == '-LIST-' and len(values['-LIST-']):
                    self.AcquistaWin.Element('-Nome-').update(contract.info_MP_prod(mat_prim[self.AcquistaWin.Element('-LIST-').Widget.curselection()[0]])[2])
                    self.AcquistaWin.Element('-QuantDisp-').update(contract.info_MP_prod(mat_prim[self.AcquistaWin.Element('-LIST-').Widget.curselection()[0]])[4])
                    self.AcquistaWin.Element('-FootPrint-').update(contract.info_MP_prod(mat_prim[self.AcquistaWin.Element('-LIST-').Widget.curselection()[0]])[5])
                if event == "ACQUISTA" and values['-IN-'].isdigit():
                    try:
                        contract.acquista_MP(mat_prim[self.AcquistaWin.Element('-LIST-').Widget.curselection()[0]],int(values['-IN-']))
                        sg.Popup('Acquisto Completato', keep_on_top=True, background_color="#1d8c3b",icon=self.icona)
                    except exceptions.SolidityError as error:
                        sg.Popup(str(error).replace('execution reverted:','Si è cerificato il seguente errore:'), keep_on_top=True, background_color="#1d8c3b",icon=self.icona)
            self.AcquistaWin.close()

    def DettagliMP(self):
        self.DettagliMPWin=sg.Window("Inserisci Lotto Materia Prima Acquistata",[
                    [sg.Text("Inserisci lotto:    ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="LOTTOMP",background_color="#8bd9a0")],
                    [sg.Button("Vedi informazioni",button_color="#013810", key="INF")]],modal=True,background_color="#1d8c3b",icon=self.icona)
        while True:
            event, values = self.DettagliMPWin.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            if event == "INF" and values['LOTTOMP']=='':
                sg.Popup("Non hai inserito un lotto",keep_on_top=True,background_color="#1d8c3b",icon=self.icona)
            if event == "INF" and not values['LOTTOMP']=='':
                try:
                    contract.info_MP_acq(values['LOTTOMP'])
                except exceptions.SolidityError as error:
                        sg.Popup(str(error).replace('execution reverted:','Si è cerificato il seguente errore:'), keep_on_top=True, background_color="#1d8c3b",icon=self.icona)
                else:
                    file_list_column = [
                        [sg.Text('Caratteristiche:',background_color="#1d8c3b")],
                        [sg.Text('Lotto:',background_color="#1d8c3b")],
                        [sg.Text(contract.info_MP_acq(values['LOTTOMP'])[1],background_color="#1d8c3b",key='-Nome-')],
                        [sg.Text('Quantità disponibile:', background_color="#1d8c3b")],
                        [sg.Text(contract.info_MP_acq(values['LOTTOMP'])[2], background_color="#1d8c3b", key='-Quantita-')],
                    ]
                    laytot = [
                        [
                            sg.Column(file_list_column, background_color="#1d8c3b")
                        ]
                    ]
                    wind = sg.Window("Informazioni Materia Prima Acquistata",laytot, modal=True,background_color="#1d8c3b", icon=self.icona)
                    while True:
                        event, values = wind.read()
                        if event == "Exit" or event == sg.WIN_CLOSED:
                            break
                    wind.close()
        self.DettagliMPWin.close()

    def AggProd(self):
        file_list_column = [
                    [sg.Text("Nome Prodotto:    ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="NOME",background_color="#8bd9a0")],
                    [sg.Text("Lotti Materie Prime:    ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="LOTTIMP",background_color="#8bd9a0")],
                    [sg.Text("Quantità Materie Prime Utilizzate:    ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="QMP",background_color="#8bd9a0")],
                    [sg.Text("Quantità Prodotto:    ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="QP",background_color="#8bd9a0")],
                    [sg.Text("FootPrint Prodotto :    ",background_color="#1d8c3b"),sg.In(size=(30, 1), enable_events=True, key="FOOTP",background_color="#8bd9a0")],
                    [sg.Button("Inserisci Prodotto",button_color="#013810", key="INS")]
                ]
        laytot = [
                    [
                    sg.Column(file_list_column, background_color="#1d8c3b")
                    ]
                ]
        self.AggProdWin=sg.Window("Inserisci Nuovo Prodotto",laytot,modal=True,background_color="#1d8c3b",icon=self.icona)

        while True:
            event, values = self.AggProdWin.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            if event == "INS":
                try:                        
                    array_lotti = values['LOTTIMP']
                    array_lotti = array_lotti.split(",")
                    array_quant = values['QMP']
                    array_quant = array_quant.split(",")
                    len_lotti = len(array_lotti)
                    len_quant = len(array_quant)
                    if (len_lotti < len_quant): 
                        sg.Popup('ad ogni lotto deve essere associata una sola quantità', keep_on_top=True, background_color="#1d8c3b",icon=self.icona)
                    if (len_quant < len_lotti): 
                        sg.Popup('ad ogni quantità deve essere associato un solo lotto', keep_on_top=True, background_color="#1d8c3b",icon=self.icona)
                    if (len_lotti == len_quant):
                    
                        res = all(ele.isdigit() for ele in array_quant)
                        if res:
                            for i in range(0,len(array_quant)):
                                    array_quant[i] = int(array_quant[i])            
                            contract.inserisci_Prod(values['NOME'],array_lotti,array_quant,int(values['QP']),int(values['FOOTP']))
                            sg.Popup('Inserimento Prodotto Completato', keep_on_top=True, background_color="#1d8c3b",icon=self.icona)
                            self.AggProdWin.Element('NOME').update('')
                            self.AggProdWin.Element('LOTTIMP').update('')
                            self.AggProdWin.Element('QMP').update('')
                            self.AggProdWin.Element('QP').update('')
                            self.AggProdWin.Element('FOOTP').update('')
                        if not res:
                            sg.Popup('Non hai inserito delle quantità valide per le materie prime utilizzate', keep_on_top=True, background_color="#1d8c3b",icon=self.icona)
                except exceptions.SolidityError as error:
                    sg.Popup(str(error).replace('execution reverted:','Si è cerificato il seguente errore:'), keep_on_top=True, background_color="#1d8c3b",icon=self.icona)
        self.AggProdWin.close()

    def ListenEvent(self):
        while True:
            event, values = self.window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                self.LoginWin.toggle_login()
                break
            if event == "tutteMP":
                self.tutteMP()
            if event == "lottiMP":
                self.lottiMP()
            if event == "infoMP":
                self.infoMP()
            if event == "acquista":
                self.Acquista()
            if event == "dettagliMP":
                self.DettagliMP()
            if event == "aggProd":
               self.AggProd()
        contract.w3.geth.personal.lock_account(contract.account[0])
        self.window.close()

    def CloseWindow(self):
        if(getattr(self,'TutteMPWin')):
            self.TutteMPWin.close()
        if(getattr(self,'LottiMPwin')):
            self.LottiMPwin.close()
        if(getattr(self,'infoMPWin')):
            self.infoMPWin.close()
        if(getattr(self,'AcquistaWin')):
            self.AcquistaWin.close()
        if(getattr(self,'DettagliMPWin')):
            self.DettagliMPWin.close()
        if(getattr(self,'AggProdWin')):
            self.AggProdWin.close()
        self.window.close()