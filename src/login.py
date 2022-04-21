from contextlib import nullcontext
import PySimpleGUI as sg
from numpy import prod
import contract
import os
import traceback
from produttore import ProdWin
from trasformatore import TrasfWin
from consumatore import ConsWin

#Definisce la finestra che sarà utilizzata per effettuare il login
class LoginWin():

    #E' il costruttore della classe. Il parametro self si riferisce all'istanza dell'oggetto (come this in C++)
    def __init__(self):

        # Salva nella variabile path il percorso globale della cartella in cui si trova il file .py in esecuzione
        self.path = os.path.abspath(os.path.dirname(
            __file__))  

        # Cambio della cartella attuale nella cartella in cui si trova il file .py
        os.chdir(self.path)  

        # viene preso il file impronta.ico dalla cartella in cui si trovale il file .py in esecuzione
        self.impronta = os.path.join(self.path,
                                     'impronta.ico')  

        self.addr = contract.account
        self.acco = [self.addr[0] + ' (trasformatore)', self.addr[1] + ' (produttore)', self.addr[2] + ' (consumatore)']
        self.acct = [self.addr[0], self.addr[1], self.addr[2]]

        #Definiamo le colonne del layout
        file_list_column = [
            [
                sg.Text("Inserisci indirizzo di portafoglio:", background_color="#1d8c3b"),
                sg.Listbox(self.acco, size=(100, 3), key="PORTAFOGLIO", enable_events=True),

            ],
            [
                sg.Text("Inserisci password di portafoglio:", background_color="#1d8c3b"),
                sg.In(size=(58, 1), enable_events=True, key="PASSWORD", background_color="#8bd9a0", password_char='*'),
            ],
            [
                sg.Button("Entra", button_color="#013810", key="entra", bind_return_key=True)
            ],
        ]

        #Layout Completo
        layout = [
            [
                sg.Column(file_list_column, background_color="#1d8c3b"),
            ]
        ]

        #Creazione della finestra passandogli il titolo, il layout, il colore di sfondo e l'icona
        self.windowLogin = sg.Window("Accedi al FootPrint Calculator", layout, background_color="#1d8c3b",
                                     icon=self.impronta)
        # Toggle della finestra "Login" per disattivare/attivare dopo login/logout
        self.nexttoggle = True  
        self.WinTrasformatore = 0
        
        self.EventListener()

    #Funzione che rende attiva o disattiva la finestra del login
    def toggle_login(self):
        self.windowLogin['entra'].update(disabled=self.nexttoggle)
        self.windowLogin['PORTAFOGLIO'].update(disabled=self.nexttoggle)
        self.nexttoggle = not self.nexttoggle

    def EventListener(self):
        # Loop degli eventi
        while True:
            event, values = self.windowLogin.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            #Viene definito cosa succede se si clicca sul bottone "entra"
            if event == "entra":
                #si va a vedere se sono stati inseriti un indirizzo di portafoglio corretto ed una password corretta
                try:
                    #Ci si accerta che un'indirizzo di portafoglio sia stato selezionato
                    contract.current_user = self.acct[self.windowLogin.Element('PORTAFOGLIO').Widget.curselection()[0]]
                    print(contract.current_user)
                    self.toggle_login()
                    print(self.acct[self.windowLogin.Element('PORTAFOGLIO').Widget.curselection()[0]])
                    if self.acct[self.windowLogin.Element('PORTAFOGLIO').Widget.curselection()[0]] == contract.trasf and \
                            values['PASSWORD'] == 'trasformatore':
                        contract.w3.geth.personal.unlock_account(contract.account[0], 'trasformatore',1500)
                        self.ProdTrasf = TrasfWin(self.impronta, self)
                        self.ProdTrasf.ListenEvent()
                    elif self.acct[
                        self.windowLogin.Element('PORTAFOGLIO').Widget.curselection()[0]] == contract.prod and values[
                        'PASSWORD'] == 'produttore':
                        contract.w3.geth.personal.unlock_account(contract.account[1], 'produttore', 1500)
                        self.ProdWin = ProdWin(self.impronta, self)
                        self.ProdWin.ListenEvent()
                    elif self.acct[
                        self.windowLogin.Element('PORTAFOGLIO').Widget.curselection()[0]] == contract.consum and values[
                        'PASSWORD'] == 'consumatore':
                        contract.w3.geth.personal.unlock_account(contract.account[2], 'consumatore',1500)
                        self.ConsWin = ConsWin(self.impronta, self)
                        self.ConsWin.ListenEvent()
                    else:
                        sg.Popup('Non hai inserito un indirizzo o una password validi', keep_on_top=True,
                                 background_color="#1d8c3b", icon=self.impronta), self.toggle_login()

                #Se non è stato selezionato alcun account o se è scaduto il tempo della sessione, si notifica cosa è accaduto
                #e viene reso possibile all'utente riprovare ad accedere
                except:
                    self.windowLogin['entra'].update(disabled=False)
                    self.windowLogin['PORTAFOGLIO'].update(disabled=False)
                    if not self.windowLogin.Element('PORTAFOGLIO').Widget.curselection():
                        print("non hai selezionato alcun account")
                        sg.Popup('non hai selezionato alcun account', keep_on_top=True, background_color="#1d8c3b",
                                 icon=self.impronta)
                    else:
                        traceback.print_exc()
                        print("Tempo scaduto! La sessione è terminata")
                        sg.Popup('Tempo scaduto! La sessione è terminata, per favore accedi nuovamente', keep_on_top=True, background_color="#1d8c3b",
                                 icon=self.impronta)
                        appo = self.windowLogin.Element('PORTAFOGLIO').Widget.curselection()[0]
                        print(appo)
                        if appo == 0:
                            self.ProdTrasf.CloseWindow()
                        elif appo == 1:
                            self.ProdWin.CloseWindow()
                        else:
                            self.ConsWin.CloseWindow()