from iqoptionapi.stable_api import IQ_Option
import PySimpleGUI as sg
from datetime import datetime
import time, threading, schedule

#
#Tela de login
#
class TelaLogin:
    def __init__(self):
        layout = [
                  [sg.Text('Login'), sg.Input()],      
                  [sg.Text('Senha'), sg.Input(password_char = "*")],      
                  [sg.Submit("logar")]
                 ] 

        window = sg.Window("iqOption Bot").layout(layout)
        self.window = window
        self.event, self.values = window.Read()

        while self.values[0] == "" or self.values[1] == "":
            layout = [
                      [sg.Text('COLOCA O LOGIN E A SENHA ANIMAL')],
                      [sg.Text('Login'), sg.Input()],      
                      [sg.Text('Senha'), sg.Input(password_char = "*")],      
                      [sg.Submit("logar")]
                     ]
            window = sg.Window("iqOption Bot").layout(layout)
            self.window = window
            self.event, self.values = window.Read()

#
#Tela principal
#
class Tela:
    def __init__(self):
        symbols = ["EURUSD", "EURJPY", "EURNZD", "EURAUD", "USDJPY", "AUDUSD", "AUDJPY", "NZDUSD", "EURUSD-OTC"]
        tempo = ["1 min", "5 min", "15 min"]
        opt = ["call", "put"]
        layout = [
                  [sg.Text('Valor'), sg.Input("5", key = "value-input")],
                  [sg.Checkbox('Definir horário?', key = "hour"), sg.Input("example: 01:23, 02:00, 14:30, 23:01", key = "hour-input")],
                  [sg.Checkbox('Conta Real', key = "account")],
                  [sg.OptionMenu(values = symbols, key = "symbol"), sg.OptionMenu(values = tempo, key = "time"), sg.OptionMenu(values = opt, key = "opt")],
                  [sg.Output(size = (60,5), echo_stdout_stderr = True)],
                  [sg.Button("Operar", visible=True, key="submit")]
                 ] 

        window = sg.Window("iqOption Bot").layout(layout)
        self.window = window
        self.event, self.values = window.Read()

#
#declarações de funções
#Buy = função que chama a api e executa a compra; 
#agendar = função que cria o schedule e fica em loop infinito tentando executar schedule (deve ser chamada por uma thread)
#operar = função chamada pelo schedule da agendar, que vai chamar a Buy em uma nova thread
#
def Buy(quantity, symbol, opt, expireTime):
    check, id = api.buy(quantity, symbol, opt, expireTime)
    if check:
        print("Lucro/preju: %.2f" % api.check_win_v3(id))
        return
    else:
        print("Operação falhou :(")
        return

def operar(value, symbol , opt, expireTime):  
    print("Deu a hora menó, iniciando a operação")
    threading.Thread(target=Buy, args=(value, symbol , opt, expireTime, )).start()

def agendar(hour_input, value, symbol , opt, expireTime):
    schedule.every().day.at(hour_input).do(operar, value, symbol , opt, expireTime)
    while True: 
        schedule.run_pending()
        time.sleep(1)

#
#Começa instanciando a tela de login e fazendo as verificações
#
telaLogin = TelaLogin()
#api = IQ_Option(str(telaLogin.values[0]), str(telaLogin.values[1]))
api = IQ_Option("alexandrealen03@gmail.com","alexandrealen03@gmail.com")
api.connect()
telaLogin.window.close()

while api.check_connect() == False:
    layout = [
        [sg.Text('Login falhou, verifique se colocou o email/senha corretos')],
        [sg.Text('Login'), sg.Input()],      
        [sg.Text('Senha'), sg.Input(password_char = "*")],      
        [sg.Submit("logar")]
    ]
    telaLogin.window = sg.Window("iqOption Bot").layout(layout)
    telaLogin.button, telaLogin.values = telaLogin.window.Read()
    api = IQ_Option(str(telaLogin.values[0]), str(telaLogin.values[1]))
    api.connect()
    telaLogin.window.close()

#
#Se tudo der certo no login a tela principal é instanciada 
#
tela = Tela()

if tela.values["account"]:
    conta = "REAL"
else:
    conta = "PRACTICE"
api.change_balance(conta)

if tela.values["time"] == "1 min":
    tela.values["time"] = 1
elif tela.values["time"] == "5 min":
    tela.values["time"] = 5
else:
    tela.values["time"] = 15  

#
#mecanismo principal, baseado na opção de agendar horário para operar ou não
#
if tela.values["hour"]:
    hour_input = str(tela.values["hour-input"])
    print("Horário definido para " + hour_input)
    value = float(tela.values["value-input"])
    symbol = tela.values["symbol"]
    opt = tela.values["opt"]
    expireTime = tela.values["time"]
    threading.Thread(target=agendar, args=(hour_input, value, symbol , opt, expireTime, )).start()
    tela.window.Element("submit").Update(disabled = True)
    while True:
        tela.window.Read()
    
