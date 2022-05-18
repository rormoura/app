from tkinter import *
import os, sys #necessária para as funções de write e read
from ioctl_cmds import *
from fcntl import ioctl
import threading
import time


fd = os.open("/dev/mydev", os.O_RDWR)
remaining = 10

valor = [0,0,0,0]
i = 0
try1 = 0

array_switches = [0,0,0,0]
j=0


def chorou_bb(num):
    tela = Tk()
    tela.geometry('1920x1080')
    tela.title('GATE: O RESGATE')
    tela['bg']='#5d8a82'
    tela.attributes('-fullscreen',True)
    f = ("Times bold", 14)

    #função que abre a janela em caso de derrota
    ioctl(fd, WR_L_DISPLAY)#carinha de choro nos displays da esquerda
    data = 0x2e3f3f3a
    os.write(fd, data.to_bytes(4, 'little'))
    ioctl(fd, WR_R_DISPLAY)#carinha de choro nos displays da direita
    os.write(fd, data.to_bytes(4, 'little'))
    ioctl(fd, WR_RED_LEDS)#ligando os leds vermelhos
    data = 0xFFFFFFFF
    os.write(fd, data.to_bytes(4, 'little'))
    ioctl(fd, WR_GREEN_LEDS)#apagando os leds verdes
    data = 0x00000000
    os.write(fd, data.to_bytes(4, 'little'))
    os.close(fd)

    if(num == 0):
        textinho = "O alarme tocou e os bandidos encurralarram vc e sua equipe :(\nF to respect"
    elif(num == 1):
        textinho = "Seus passos fizeram muito barulho e os bandidos encurralarram vc e sua equipe :(\nF to respect"
    elif(num == 2):
        textinho = "Foi identificado que o sistema estava sendo invadido e os bandidos encurralarram vc e sua equipe :(\nF to respect"
    else:
        textinho = "KABOOM? Yes Rico, KABOOM!\nF to respect"


    def Voltar():
        tela.destroy()
        criar_menu()

    Label(
        tela,
        text=textinho,
        padx=20,
        pady=20,
        bg='red',
        font=f
    ).pack(expand = TRUE, fill=BOTH)

    Button(
        tela, 
        text="F", 
        font=f,
        command= Voltar
        ).pack(fill=X, side=BOTTOM)


    tela.mainloop()

def criar_garagem():
    tela = Tk()
    tela.geometry('1920x1080')
    tela.title('GATE: O RESGATE')
    tela['bg']='#5d8a82'
    tela.attributes('-fullscreen',True)
    f = ("Times bold", 14)

    def bomb():
        os.close(fd)
        criar_bomb()

    def vigilancia():
            global array_switches
            if(array_switches[0] == b'\x0c' and array_switches[1] == b'\x08' and array_switches[2] == b'\x0f' and array_switches[3] == b'\x02'): #resposta: C8F2
                ioctl(fd, WR_RED_LEDS) #se acertou, os leds vermelhos são apagados e os verdes acesos
                data = 0x0
                os.write(fd, data.to_bytes(4, 'little'))
                ioctl(fd, WR_GREEN_LEDS)
                data = 0xFFFFFFFF
                os.write(fd, data.to_bytes(4, 'little'))
                tela.destroy()
                criar_bomb()
            else:
                ioctl(fd, WR_RED_LEDS) #se errou, os leds vermelhos são acesos e os verdes apagados
                data = 0xFFFFFFFF
                os.write(fd, data.to_bytes(4, 'little'))
                ioctl(fd, WR_GREEN_LEDS)
                data = 0x0
                os.write(fd, data.to_bytes(4, 'little'))
                tela.destroy()
                chorou_bb(2)

    def click2():
        global array_switches
        global j

        ioctl(fd, RD_SWITCHES) #setando para ler os switches
        array_switches[j] = os.read(fd, 1) #lendo um byte dos switches
        j+=1

    bg = PhotoImage(file = "../Imagens/garagem.png")
    canvas = Canvas(tela)
    canvas.pack(fill="both", expand=True)
    canvas.create_image( (1920/2), (1080/2), image = bg, anchor = "center")

    #TERCEIRO DESAFIO
    #Consiste em hackear o sistema de vigilância da garagem mandando cinco algarismos pelos switches, os quais correspondem ao endereço 
    #que é a soma dos endereços que apareçem nos displays da esquerda (origem) e da direita (offset). Endereço de origem, mostrado em hexa: 0456.
    #Offset, mostrado em hexa: 8392. Resultado: 04560 + 08392 = C8F2. Então, pelos switches, o usuário deve mandar os seguintes
    #algarismos (em decimal) na seguinte ordem: 12 -> 8 -> 15 -> 2. O usuário só tem uma chance, caso contrário perde. Para enviar cada um dos
    #algarismos, envie no terminal a letra 'a'.

    Label(
        canvas,
        text="""Seu terceiro desafio é hackear o sistema de vigilância da garagem mandando quatro algarismos pelos switches, os quais correspondem ao endereço
                que é a soma dos endereços que apareçem nos displays da esquerda (origem) e da direita (offset).
                Vc só tem uma chance!!\nMande um algarismo por vez e nessa ordem: mais significativos -> menos significativos.
                Para mandar através dos switches é preciso clicar em "Enter" para cada valor. Depois, clicar em "Confirma".\nLembrando que os switches enviam um número em binário!
                Quando chegar no próximo desafio, pode fechar essa tela.""",
        padx=20,
        pady=20,
        bg='#ffbf00',
        font=f
    ).pack(side=TOP, fill=X)
    botao = Button(canvas, text="Confirma", command=vigilancia, bg='dark blue', fg='white', font="Arial 10 bold", activebackground='red', activeforeground='white', height=2, width=4)
    botao.pack(fill=X, side=BOTTOM)

    botao = Button(canvas, text="Enter", command=click2, bg='dark blue', fg='white', font="Arial 10 bold", activebackground='red', activeforeground='white', height=2, width=4)
    botao.pack(fill=X, side=BOTTOM)

    ioctl(fd, WR_L_DISPLAY)#origem
    data = 0x40191202 
    os.write(fd, data.to_bytes(4, 'little'))
    ioctl(fd, WR_R_DISPLAY)#offset
    data = 0x00301024
    os.write(fd, data.to_bytes(4, 'little'))

    tela.mainloop()

def criar_bomb():
    tela = Tk()
    tela.geometry('1920x1080')
    tela.title('GATE: O RESGATE')
    tela.attributes('-fullscreen',True)
    f = ("Times bold", 34)
    bg = PhotoImage(file='../Imagens/bomb.png')

    canvas = Canvas(tela)
    canvas.pack(fill="both", expand=True)
    canvas.create_image( (1920/2), (1080/2), image = bg, anchor = "center")

    def Desarmar():
        texto = cx_txt.get()
        tela.destroy()
        if(texto == "7355608"):
            criar_sobre()
        else:
            chorou_bb(3)

    label = Label(
        canvas,
        padx=20,
        pady=20,
        bg='#ffbf00',
        font=f
    )
    label.pack(side=TOP)

    Label(
        canvas,
        text="Nesse momento vc se lembra do pai dos FPS: 7355608",
        padx=20,
        pady=20,
        bg='#ffbf00',
        font=f
    ).pack(side=TOP, fill=X)

    cx_txt = Entry(tela, width = 20)
    cx_txt.pack(fill=X, side=BOTTOM, pady = 10)

    bt = Button(
        canvas, 
        text="Desarmar", 
        font=f,
        command=Desarmar,
    )
    bt.pack(fill=X, side=BOTTOM)

    

    def clock():
        global remaining
    
        while remaining>=0:
            mins, secs = divmod(remaining, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            remaining -= 1
            label.config(text=timeformat)
            tela.update()
            time.sleep(1) 

        tela.destroy()
        
    global remaining

    t1 = threading.Thread(target=clock)
    t1.start()

    button1_canvas = canvas.create_window(100, 10, anchor = "nw")
    

    tela.mainloop()
    chorou_bb(3)



def criar_cozinha():
    tela = Tk()
    tela.geometry('1920x1080')
    tela.title('GATE: O RESGATE')
    tela['bg']='#5d8a82'
    tela.attributes('-fullscreen',True)
    f = ("Times bold", 14)
    bg = PhotoImage(file='../Imagens/cozinha.png')

    canvas = Canvas(tela)
    canvas.pack(fill="both", expand=True)
    canvas.create_image( (1920/2), (1080/2), image = bg, anchor = "center")

    def Voltar():
        tela.destroy()
        criar_sala()

    Label(
        canvas,
        text="Parece que o refém não está nesse lugar",
        padx=20,
        pady=20,
        bg='#ffbf00',
        font=f
    ).pack(side=TOP, fill=X)

    Button(
        canvas, 
        text="Voltar", 
        font=f,
        command=Voltar
        ).pack(fill=X, side=BOTTOM)


    tela.mainloop()

def criar_quarto():
    tela = Tk()
    tela.geometry('1920x1080')
    tela.title('GATE: O RESGATE')
    tela['bg']='#5d8a82'
    tela.attributes('-fullscreen',True)
    f = ("Times bold", 14)
    bg = PhotoImage(file='../Imagens/quarto.png')

    canvas = Canvas(tela)
    canvas.pack(fill="both", expand=True)
    canvas.create_image( (1920/2), (1080/2), image = bg, anchor = "center")

    def Voltar():
        tela.destroy()
        criar_sala()

    Label(
        canvas,
        text="Ninguém por aqui...",
        padx=20,
        pady=20,
        bg='#ffbf00',
        font=f
    ).pack(side=TOP, fill=X)

    Button(
        canvas, 
        text="Voltar", 
        font=f,
        command=Voltar
        ).pack(fill=X, side=BOTTOM)


    tela.mainloop()

def criar_sala():
    tela = Tk()
    tela.geometry('1920x1080')
    tela.title('GATE: O RESGATE')
    tela['bg']='#5d8a82'
    tela.attributes('-fullscreen',True)
    f = ("Times bold", 14)
    bg = PhotoImage(file='../Imagens/sala.png')

    canvas = Canvas(tela)
    canvas.pack(fill="both", expand=True)
    canvas.create_image( (1920/2), (1080/2), image = bg, anchor = "center")

    def Voltar():
        tela.destroy()
        criar_menu()

    def quarto():
        tela.destroy()
        criar_quarto()

    def cozinha():
        tela.destroy()
        criar_cozinha()

    def garagem():
        tela.destroy()
        criar_garagem()

    Label(
        canvas,
        text="Seu segundo desafio é encontrar o local onde o refém está!!Escolha logo! O tempo está passando!!!\nVc só tem duas chances antes que os capangas ouçam seus passos!!!",
        padx=20,
        pady=20,
        bg='#ffbf00',
        font=f
    ).pack(side=TOP, fill=X)

    Button(
        canvas, 
        text="Voltar", 
        font=f,
        command=Voltar
        ).pack(fill=X, side=BOTTOM)

    Button(
        canvas, 
        text="Garagem", 
        font=f,
        command=garagem
        ).pack(fill=X, side=BOTTOM)

    Button(
        canvas, 
        text="Quarto", 
        font=f,
        command=quarto
        ).pack(fill=X, side=BOTTOM)

    Button(
        canvas, 
        text="Cozinha", 
        font=f,
        command=cozinha
        ).pack(fill=X, side=BOTTOM)

    tela.mainloop()

def criar_porta():
    tela = Tk()
    tela.geometry('1920x1080')
    tela.title('GATE: O RESGATE')
    tela['bg']='#5d8a82'
    tela.attributes('-fullscreen',True)
    f = ("Times bold", 14)

    fd = os.open("/dev/mydev", os.O_RDWR)

    def Voltar():
        os.close(fd)
        tela.destroy()

    def sala():
        os.close(fd)
        tela.destroy()
        criar_sala()

    def Sair():
        tela.detroy()
        criar_menu()

    def senha():#O PRIMEIRO DESAFIO
        global try1
        global valor
        #Essa função sãos os loops que leem os push buttons 

        if(valor[0] == b'\x01' and valor[1] == b'\x00' and valor[2] == b'\x02' and valor[3] == b'\x04'): #resposta: 1024 bytes
            ioctl(fd, WR_RED_LEDS) #se acertou, os leds vermelhos são apagados e os verdes acesos
            data = 0x0
            os.write(fd, data.to_bytes(4, 'little'))
            ioctl(fd, WR_GREEN_LEDS)
            data = 0xFFFFFFFF
            os.write(fd, data.to_bytes(4, 'little'))
            sala()
        else:
            try1+=1
            if try1==2:
                tela.destroy()
                chorou_bb(0)
            ioctl(fd, WR_RED_LEDS) #se errou, os leds vermelhos são acesos e os verdes apagados
            data = 0xFFFFFFFF
            os.write(fd, data.to_bytes(4, 'little'))
            ioctl(fd, WR_GREEN_LEDS)
            data = 0x0
            os.write(fd, data.to_bytes(4, 'little'))
            print("SÓ MAIS UMA CHANCE!")


    def click():
        global i
        global valor

        ioctl(fd, RD_PBUTTONS) #setando para ler os push buttons
        valor[i] = os.read(fd, 1) #lendo um byte dos push buttons
        i=i+1

    img = PhotoImage(file='../Imagens/porta.png')

    canvas = Canvas(tela)
    canvas.pack(fill="both", expand=True)
    canvas.create_image( (1920/2), (1080/2), image = img, anchor = "center")

    Label(
        canvas,
        text= """Seu primeiro desafio é acertar a senha da fechadura!!
                Vc terá que informar quatro algarismos através dos push buttons\nUm de cada vez! Forneca um algarismo (segurando!) e clique em "Enter".
                Se vc acertar o algarismo, os leds verdes ficam ligados, caso contrário, os vermelhos.
                Vc tem somente duas tentativas antes do alarme tocar!!
                Dica para a senha: Quantidade de bytes reservados para a IVT. Informe os algarismos nessa ordem: milhar->centena->dezena->unidade.
                Após, aperte "Confirma" para prosseguir.""",
        padx=20,
        pady=20,
        bg='#ffbf00',
        font=f
    ).pack(side=TOP, fill=X)
    
    botao = Button(canvas, text="Confirma", command=senha, bg='dark blue', fg='white', font="Arial 10 bold", activebackground='red', activeforeground='white', height=2, width=4)
    botao.pack(fill=X, side=BOTTOM)

    botao = Button(canvas, text="Enter", command=click, bg='dark blue', fg='white', font="Arial 10 bold", activebackground='red', activeforeground='white', height=2, width=4)
    botao.pack(fill=X, side=BOTTOM)

    tela.mainloop()

def criar_sobre():
    tela = Tk()
    tela.geometry('1920x1080')
    tela.title('GATE: O RESGATE')
    tela['bg']='#5d8a82'
    tela.attributes('-fullscreen',True)
    f = ("Times bold", 14)

    def Voltar2():
        tela.destroy()
        criar_menu()

    Label(
        tela,
        text="Obrigado por jogar!\nDesenvolvido por atss, lnb, mvfs, rrm2, vgc3\n",
        padx=20,
        pady=20,
        bg='#ffbf00',
        font=f
    ).pack(expand=True, fill=BOTH)

    Button(
        tela, 
        text="Voltar", 
        font=f,
        command=Voltar2
        ).pack(fill=X, expand=TRUE, side=LEFT)
    tela.mainloop()

def criar_menu():
    tela = Tk()
    tela.geometry('1920x1080')
    tela.title('GATE: O RESGATE')
    tela['bg']='#5d8a82'
    tela.attributes('-fullscreen',True)
    f = ("Times bold", 14)
    bg = PhotoImage(file='../Imagens/Gate.png')

    def Jogar():
        tela.destroy()
        criar_porta()

    def Sobre():
        tela.destroy()
        criar_sobre()
    
    def Sair():
        exit(0)

    canvas = Canvas(tela)
    canvas.pack(fill="both", expand=True)
    canvas.create_image( (1920/2), (1080/2), image = bg, anchor = "center")

    Button(
        canvas, 
        text="Sair", 
        font=f,
        command=Sair
        ).pack(fill=X, side=BOTTOM)

    Button(
        canvas, 
        text="Sobre", 
        font=f,
        command=Sobre
        ).pack(fill=X, side=BOTTOM)

    Button(
        canvas, 
        text="Jogar", 
        font=f,
        command=Jogar
        ).pack(fill=X, side=BOTTOM)

    global valor, i, ry1, array_switches, j
    valor = [0,0,0,0]
    i = 0
    try1 = 0

    array_switches = [0,0,0,0]
    j=0

    ioctl(fd, WR_RED_LEDS) #se acertou, os leds vermelhos são apagados e os verdes acesos
    data = 0x0002aaaa
    os.write(fd, data.to_bytes(4, 'little'))
    ioctl(fd, WR_GREEN_LEDS)
    data = 0x00000155
    os.write(fd, data.to_bytes(4, 'little'))
    ioctl(fd, WR_L_DISPLAY) #se acertou, os leds vermelhos são apagados e os verdes acesos
    data = 0x3F3F3F3F
    os.write(fd, data.to_bytes(4, 'little'))
    ioctl(fd, WR_R_DISPLAY)
    data = 0x3F3F3F3F
    os.write(fd, data.to_bytes(4, 'little'))

    tela.mainloop()

criar_menu()