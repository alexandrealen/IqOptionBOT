from iqoptionapi.stable_api import IQ_Option
import PySimpleGUI as sg
from datetime import datetime
import time, threading, schedule

#
#Tela de login
#
class TelaLogin:
    def __init__(self):
        sg.theme("Reddit")
        layout = [
                  [sg.Text('Login'), sg.Input()],      
                  [sg.Text('Senha'), sg.Input(password_char = "*")],      
                  [sg.Submit("logar")]
                 ] 

        window = sg.Window("iqOption Bot").layout(layout)
        self.window = window
        self.event, self.values = window.Read()

        while self.values[0] == "" or self.values[1] == "":
            sg.theme("Reddit")
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
        sg.theme("Reddit")
        symbols = ["AUDCAD", "AUDCHF", "AUDJPY", "AUDJPY-OTC", "AUDNZD", "AUDUSD", "AUDUSD-OTC", "CADCHF", "CADJPY", "CHFJPY", "EURAUD", "EURAUD-OTC", "EURCAD", "EURGBP", "EURJPY", "EURJPY-OTC", "EURNZD", "EURNZD-OTC", "EURUSD", "EURUSD-OTC", "GBPAUD", "GBPCAD", "GBPCHF", "GBPJPY", "GBPNZD", "GBPUSD", "NZDUSD", "NZDUSD-OTC", "USDCAD", "USDCHF", "USDJPY", "USDJPY-OTC", "USDNOK"]
        tempo = ["1 min", "5 min", "15 min"]
        opt = ["call", "put"]
        layout = [
                  [sg.Text('Valor'), sg.Input("5", key = "value-input")],
                  [sg.Checkbox('Definir horário?', key = "hour", default=True), sg.Input("01:59:58", key = "hour-input")],
                  [sg.Checkbox('Conta Real', key = "account")],
                  [sg.OptionMenu(values = symbols, key = "symbol"), sg.OptionMenu(values = tempo, key = "time"), sg.OptionMenu(values = opt, key = "opt")],
                  [sg.Output(size = (60,6), echo_stdout_stderr = True)],
                  [sg.Button("Operar", visible=True, key="submit"), sg.Button("Resetar", visible=False, key="reset")]
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
def Buy(quantity, symbol, opt, expireTime, tela):
    check, id = api.buy(quantity, symbol, opt, expireTime)
    if check:
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": Lucro/preju: %.2f" % api.check_win_v3(id))
    else:
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": Operação falhou, verifique se inseriu os dados corretamente e se o simbolo o qual deseja apostar está aberto")

    tela.window.Element("reset").Update(visible = True)
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": A operação terminou, se deseja operar novamente, clique em resetar")
    


def operar(value, symbol , opt, expireTime, tela):  
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": Deu a hora menó, iniciando a operação")
    t2 = threading.Thread(target=Buy, args=(value, symbol , opt, expireTime, tela, ))
    t2.daemon = True
    t2.start()

def agendar(hour_input, value, symbol , opt, expireTime, tela):
    schedule.every().day.at(hour_input).do(operar, value, symbol , opt, expireTime, tela)
    while True: 
        schedule.run_pending()
        time.sleep(1)

def CreateAndManageLoginWindow():
    telaLogin = TelaLogin()
    if telaLogin.event == sg.WIN_CLOSED:
        telaLogin.window.close()
        exit()
    api = IQ_Option(str(telaLogin.values[0]), str(telaLogin.values[1]))
    #api = IQ_Option("alexandrealen03@gmail.com", "alexandrealen03@gmail.com")
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
        telaLogin.event, telaLogin.values = telaLogin.window.Read()
        api = IQ_Option(str(telaLogin.values[0]), str(telaLogin.values[1]))
        api.connect()
        telaLogin.window.close()

    return api

def CreateAndManageMainWindow(api):
    tela = Tela()
    first = False
    while True:
        if first == True:
            tela.event, tela.values = tela.window.Read()
        else:
            first = True

        if tela.event == sg.WIN_CLOSED:
            tela.window.close()
            exit()

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
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": Horário definido para " + hour_input)
            value = float(tela.values["value-input"])
            symbol = tela.values["symbol"]
            opt = tela.values["opt"]
            expireTime = tela.values["time"]
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": valor: R$:" + str(value))
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": ativo: " + str(symbol))
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": opção: " + str(opt))
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": duração: " + str(expireTime) + " min")
            t1 = threading.Thread(target=agendar, args=(hour_input, value, symbol , opt, expireTime, tela, ))

            #para poder fechar o programa mesmo que a thread não tenha terminado
            t1.daemon = True

            t1.start()
            tela.window.Element("submit").Update(disabled = True)
            while True:
                event, values = tela.window.Read()
                if event == sg.WIN_CLOSED:
                    exit()
                elif event == "reset":
                    tela.window.Element("submit").Update(disabled = False)
                    tela.window.Element("reset").Update(visible = False)
                    break
        else:
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": Iniciando operação agora")
            value = float(tela.values["value-input"])
            symbol = tela.values["symbol"]
            opt = tela.values["opt"]
            expireTime = tela.values["time"]
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": valor: R$:" + str(value))
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": ativo: " + str(symbol))
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": opção: " + str(opt))
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": duração: " + str(expireTime) + " min")
            t1 = threading.Thread(target=Buy, args=(value, symbol , opt, expireTime, tela, ))

            #para poder fechar o programa mesmo que a thread não tenha terminado
            t1.daemon = True
            
            t1.start()
            tela.window.Element("submit").Update(disabled = True)
            while True:
                event, values = tela.window.Read()
                if event == sg.WIN_CLOSED:
                    exit()
                elif event == "reset":
                    tela.window.Element("submit").Update(disabled = False)
                    tela.window.Element("reset").Update(visible = False)
                    break

#
#Começa instanciando a tela de login e fazendo as verificações
#
api = CreateAndManageLoginWindow()

CreateAndManageMainWindow(api)