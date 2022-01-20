from calendar import month
from cgitb import text
from distutils import command
from posixpath import split
from tkinter import *
from tkinter import ttk
from tkinter import font
from turtle import left
from typing import Counter
from PIL import ImageTk,Image
from datetime import date
from compras import compras
from pynubank import Nubank, MockHttpClient
import matplotlib.pyplot as pyplot
import collections

# cpf = "aqui voce bota seu cpf"
# senha = "aqui voce bota a sua senha"

# nu = Nubank()
# uuid, qr_code = nu.get_qr_code()
# qr_code.print_ascii(invert=True)
# input('Após escanear o QRCode pressione enter para continuar')
# nu.authenticate_with_qr_code(cpf, senha, uuid)

nu = Nubank(MockHttpClient())
nu.authenticate_with_cert("qualquer-cpf", "qualquer-senha", "caminho/do_certificado.p12")

card_statements = nu.get_card_statements()
# account_statements = nu.get_account_statements()
totalSpent = 0


#Informações hardCoded apenas para ilustração
invoiceStr = "470,21"
goal = 600

# TransferOutEvent Transferência enviada
# TransferInEvent Transferência recebida
# BillPaymentEvent Pagamento da fatura
# BarcodePaymentEvent Pagamento efetuado
################################################

time = date.today()
timeStr = time.strftime("%d/%m/%Y")

splash_screen = Tk()
splash_screen.geometry("+500+250")
splash_screen.overrideredirect(True) #Desabilita o título da janela
splash_screen.wm_attributes("-transparentcolor", 'green')

img = ImageTk.PhotoImage(Image.open("money.ico"))
label = Label(image=img, bg="green")
label.grid()

months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

def mainWindow():
    splash_screen.destroy()
    menu = Tk()
    menu.title("Gerenciador de Finanças")
    menu.geometry("500x600+450+250")
    menu.iconbitmap("money.ico")

    nb = ttk.Notebook(menu)
    nb.place(x=0, y=0, width=500, height=600)

    dateTime = Label(nb, text=timeStr)
    dateTime.pack(side=TOP, anchor=NE)

    aba1 = Frame(nb, bg="lime green")
    nb.add(aba1, text="Menu Principal")
    aba2 = Frame(nb, bg="lime green")
    nb.add(aba2, text="Resumo do Cartão")
    aba3 = Frame(nb, bg="lime green")
    nb.add(aba3, text="Resumo da NuConta")

    file = open("dados.txt", "a+")
    patrimonio = 0
    linha = ""

    # for operation in account_statements:
    #     operation["amount"] = str(float(operation["amount"])/100.0)

    #     if str(operation['__typename']) == 'TransferInEvent':
    #         patrimonio += float(operation["amount"])
    #         linha = operation['title'] + ";" + str(operation['detail']) + ";"  + str(operation['postDate']) + ";"  + str(operation['detail']).replace('R$','').replace(' ','') + '\n'

    #     elif str(operation['__typename']) == 'TransferOutEvent':
    #         patrimonio -= float(operation["amount"])
    #         linha = operation['title'] + ";" + str(operation['detail']) + ";"  + str(operation['postDate']) + ";"  + str(operation['detail']).replace('R$','').replace(' ','') + '\n'

    #     elif str(operation['__typename']) == 'BarcodePaymentEvent':
    #         patrimonio -= float(operation["amount"])
    #         linha = operation['title'] + ";" + str(operation['detail']) + ";"  + str(operation['postDate']) + ";"  + str(operation['detail']).replace('R$','').replace(' ','') + '\n'

    #     elif str(operation['__typename']) == 'PixTransferOutEvent':
    #         patrimonio -= float(operation["amount"])
    #         linha = operation['title'] + ";" + str(operation['detail']) + ";"  + str(operation['postDate']) + ";"  + str(operation['detail']).replace('R$','').replace(' ','') + '\n'

    #     elif str(operation['__typename']) == 'PixTransferInEvent':
    #         patrimonio += float(operation["amount"])
    #         linha = operation['title'] + ";" + str(operation['detail']) + ";"  + str(operation['postDate']) + ";"  + str(operation['detail']).replace('R$','').replace(' ','') + '\n'

            
    #     elif str(operation['__typename']) == 'BillPaymentEvent':
    #         patrimonio -= float(operation["amount"])
    #         linha = operation['title'] + ";" + str(operation['detail']) + ";"  + str(operation['postDate']) + ";"  + str(operation['detail']).replace('R$','').replace(' ','') + '\n'

    #     file.writelines(linha)
    #     patrimonio += float(operation["amount"])

    patrimonio = float("{:.2f}".format(patrimonio))
    patrimony = Label(aba3, text="Patrimonio atual = R$ " + str(patrimonio),
     bd=2, font=25, bg="pale green",
     borderwidth=2, relief="flat", width=40)
    patrimony.pack(anchor="center", pady=20)

    def updateMonth(currentMonth):
        monthlyExpenses["text"] = currentMonth + ": Gastos Mensais"

    monthlyExpenses = Label(aba2, text="Gastos Mensais",
     bd=2, font=25, bg="pale green",
     borderwidth=2, relief="flat", width=40)
    monthlyExpenses.pack(anchor="center", pady=20)


    def updateTreeView(totalSpent):
        totalSpent = 0
        tv.delete(*tv.get_children())
        month = mySpin.get()
        updateMonth(month)
        
        for compra in card_statements:
            if month != months[int(compra["time"].split("-")[1])-1]:
                continue

            values = [compra["amount"]/100.0, compra["description"], compra["time"].split("T")[0]]
            tv.insert("", "end", values=values)
            totalSpent += float(compra["amount"]/100)

        totalSpent = float("{:.2f}".format(totalSpent))
        totalSpentLabel["text"] = "Os gastos desse mês totalizam \nR$ " + str(totalSpent)

        if goal - totalSpent <=0:
            invoice["text"] = "Em " + month + ", seus gastos superaram o planejamento mensal em\nR$ " + str("{:.2f}".format(abs(goal - totalSpent)))
        else:
            invoice["text"] = "Em " + month + ", você economizou\nR$ " + str("{:.2f}".format(abs(goal - totalSpent)))


    def value_changed():
        updateTreeView(totalSpent)

    monthSelect = Label(aba2, text="Selecione o mês", width=50, relief="flat", bg="pale green")
    monthSelect.pack( padx=10)

    mySpin = Spinbox(aba2, values=months, width=50, relief="groove", command=value_changed)
    mySpin.pack( padx=5)
    
    tv = ttk.Treeview(aba2, columns=("Valor", "Estabelecimento", "Data"), show="headings")
    tv.column("Valor",  width=80)
    tv.column("Estabelecimento", width=200)
    tv.column("Data", width=80)
    tv.heading("Valor", text="VALOR")
    tv.heading("Estabelecimento", text="ESTABELECIMENTO")
    tv.heading("Data",text="DATA")
    tv.pack(pady=5)
    

    totalSpentLabel = Label(aba2, text="Os gastos desse mês totalizam \nR$ " + str(totalSpent), bd=2, font=25, bg="pale green",
     borderwidth=2, relief="flat", width=40)
    totalSpentLabel.pack(pady=15)

    invoice = Label(aba2, text="Planejamento mensal", bd=2, font=25, bg="pale green",
     borderwidth=2, relief="flat", width=40)
    invoice.pack(pady=15)

    def generateStatistics():
        titles = []
        reducedTitles = []
        titleLabels = []

        currentMonth = mySpin.get()

        for compra in card_statements:
            if currentMonth == months[int(compra["time"].split("-")[1])-1]:
                titles.append(compra["title"])

        counter=collections.Counter(titles)

        for title in counter:
            reducedTitles.append(counter[title])
            titleLabels.append(title)

        pyplot.axis("equal")
        pyplot.pie(reducedTitles, labels=titleLabels, autopct='%1.1f%%')
        pyplot.legend(titleLabels, loc=3)
        pyplot.title("Resumo dos gastos no mês de " + currentMonth)
        pyplot.show()


    statisticsButton = Button(aba2, text="Gerar estatísticas do mês", width=50, relief="groove", command=generateStatistics)
    statisticsButton.pack()


splash_screen.after(2000, mainWindow)
mainloop()