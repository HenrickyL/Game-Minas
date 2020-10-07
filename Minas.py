#IMPORTANDO BIBLIOTECAS

import pygame as pg # biblioteca de jogos
from pygame.locals import *
import pygame.font #trabalhar com fontes
from time import sleep #pausar o sistema
from random import randint #gerar numeros aleatórios
import numpy as np #trabalhar com vetores e matemática em geral
import sys
import threading

#uso de thred para criar um cronometromensagem
#*problema: thred não se encerra com o fim do jogo, e uma dificuladade em usar as variáveis no contador.

global segundos, minutos, hora, time_Stop#, Thr_quit

#Thr_quit=False
segundos, minutos, hora= 0,0,0
time_Stop=False

def crono(): #thread serve para execução simultânea
        global segundos, minutos, hora,time_Stop#, Thr_quit
        segundos = int(segundos)
        minutos= int(minutos)
        hora= int(hora)

        if time_Stop==True:
            return
        elif hora == 1 and minutos==30:
            hora=0
            minutos=0
            segundos=0
            return 
        elif minutos== 60:
            minutos=0
            hora+=1
            return crono()

        elif segundos == 60:
            segundos = 0
            minutos+=1
            return crono()
        else:
            segundos+=1
            sleep(1)
            if(segundos%60==0):
                print("*")
            return crono()

#CLASSES

class colors: #Criada para não precisar escrever as tuplas RGB.
    def __init__(self):
        self.black=(0,0,0)
        self.white=(255,255,255)
        self.gray_e=(80, 80, 80) #cinza escuro
        self.gray=(180, 180, 180)#cinza claro
        self.red=(255,0,0)
        self.green=(0,255,0)
        self.blue=(0,0,255)
        self.red_e=(120, 0, 0)
        self.green_e=(0, 120, 0)
cor= colors()
cor.white
class Default: #Criada para deixar valores padrões.
    window=[800,600]
    #N=[8,12,16,20]#grid_game_divisões
    n=8
    aux=window[0]-window[1] #delta x: área de score |x x x|s|
    Game_area=[window[0]-aux,window[1]]
    title="Minas @HenrickyL"
    Img_bomb = pg.image.load("bomb.png")
    
    Img_exp = pg.image.load("expl.png")
    Img_band_game = pg.image.load("Band.png")
    Img_duv = pg.image.load("Duvid.png")
    Img_clock = pg.image.load("time.png")
    tam_c = 30
    re_size_c=[tam_c,tam_c]
    Img_clock= pg.transform.scale(Img_clock, re_size_c)
    Img_band = pg.image.load("Band.png")
    Img_band= pg.transform.scale(Img_band, re_size_c)
    def Red_img(self,img): #redimensionar imagem
        A=(82.14895971050655, -3.000135777641224) #parametros da função que redimensiona
        n=self.n
        y=A[0]+n*A[1]
        #
        #k=[60,45,30,25]
        l=round(y)
        re_size=[l,l]
        return pg.transform.scale(img, re_size)
    #redimensionado
    def IMG_redimensionada(self):
        self.Img_bomb=self.Red_img(self.Img_bomb)
        self.Img_exp=self.Red_img(self.Img_exp)
        self.Img_band_game=self.Red_img(self.Img_band_game)
        self.Img_duv=self.Red_img(self.Img_duv)

###########################        
class Grid: # crindo blocos que são organizamos em "grid"
    default=Default()
    first_click=True #se ocorreu o 1º click
    pos_first=None #salvar a posição do primeiro click
    G_cor=cor.white 
    G_cor_f=cor.gray_e
    default.n = n = None
    Qflags=0 #quantidade de bandeiras colocadas
    Qb=None
    #salvar var 1 vez
    Sv=True #se deve salvar a alteração na matriz de verificação M_v
    #organizar Mv 1 unica vez
    Omv=True
    Wd=default.Game_area
    Wx=None
    Wy=None
    Game_over = False
    esp=2 #espaçamento entre blocos

    clock=pg.time.Clock()
    def Bloco(self):
        esp=self.esp
        self.default.n = self.n
        self.default.IMG_redimensionada()
        self.Qb=round(self.n**2*0.15)
        # "i" para diferenciar
        self.Wx=Wxi=int((self.Wd[0])/self.n)
        self.Wy=Wyi=int((self.Wd[1])/self.n)
        B=pg.Surface([Wxi-esp,Wyi-esp])
        return Wxi,Wyi,B
        
    def Draw_back(self,BG,M_p,Mn): #função que faz o grid de tras branco e cria a matriz das posições M_p dos blocos
        e=self.esp
        Wx,Wy,B=self.Bloco()
        l,m=0,0
        for i in range(e,self.Wd[0],Wx):
            l+=1
            aux=[]
            for j in range(e,self.Wd[1],Wy):
                m+=1
                p=[i,j]
                B.fill(cor.white)
                BG.blit(B,p)
                #criar matriz de posições
                aux.append(p)
            if(self.Sv==True):
                M_p.append(aux)
        self.Sv=False
    def organizar_borda(self,Mv): #organizar a matriz M_v com as bordas 0->1
        if(self.Omv==True):
            m=len(Mv[1])
            n=len(Mv[0])
            for i in range(0,n):
                Mv[i][0]=1
                Mv[i][n-1]=1
                for j in range(0,m):
                    Mv[0][j]=1
                    Mv[m-1][j]=1
            self.Omv=False
    def Ver_redor_click(self,Mn,Mv,pos_click): #verificar redor do click; recursao parapreencher M_v dependendo de M_n
        p=pos_click
        x=p[0] #determina x, e x determina a coluna (i)
        y=p[1] #determina y, e y indica a linha (j)
        if Mv[x][y]==1 or x==0 or y==0 or x>=len(Mn)-1 or y>=len(Mn)-1:
            return
        Mv[x][y] = 1
        #não ter verificado e ser zero bombas ao redor
        if(Mn[x][y]==0):#and x>=0 and y>=0):
            #olhar os arredores não verificados
            self.Ver_redor_click(Mn,Mv,[x-1,y])
            self.Ver_redor_click(Mn,Mv,[x,y-1])
            self.Ver_redor_click(Mn,Mv,[x+1,y])
            self.Ver_redor_click(Mn,Mv,[x,y+1])
             
            
    def Draw_front(self,BG,M_n,M_p,M_v): #desenhar os blocos da frente, que podem existir ou não, dependendo o M_v
        mouse=pg.mouse.get_pos()
        mouse_c=pg.mouse.get_pressed()
        Wx,Wy,B=self.Bloco()
        for i in range(1,len(M_v[0])-1):
            for j in range(1,len(M_v[1])-1):
                if(M_v[i][j]!=1 and self.Game_over!=True):
                    pos=M_p[i-1][j-1]#-1 pela matriz ser menor que a Mn
                    xi=pos[0] #determina a coluna
                    xf=xi+self.Wx
                    yi=pos[1] #determina a linha
                    yf=yi+self.Wy
                    if(xi<=mouse[0]<=xf and yi<=mouse[1]<=yf):
                        B.fill([120,120,120])
                        if(mouse_c[0]==1):                         
                            if(self.first_click==True):
                                self.pos_first_click=[j,i] #se clicar [i=1,j=8] ficava como [x=8,y=1]/na matriz segue essa posição
                                self.first_click=False
    
                            else:
                                if(M_v[i][j]==2):
                                    self.Qflags-=1
                                #verificar ao redor
                                self.Ver_redor_click(M_n,M_v,[i,j])
                        elif(mouse_c[2]==1): #bandeiras
                            if(M_v[i][j]!=2 and self.Qflags<self.Qb): 
                                M_v[i][j]=2
                                self.Qflags+=1
                            elif(M_v[i][j]==2 and self.Qflags<self.Qb):
                                sleep(0.1)
                                M_v[i][j]=0
                                self.Qflags-=1
                            B.fill(cor.red)                         
                    else:
                        B.fill(cor.gray_e)
                    #printando bloco e verificando se precisa colocar bandeira
    
                    if(M_v[i][j]==2 and self.Qflags<=self.Qb):
                        BG.blit(B,M_p[i-1][j-1])
                        BG.blit(self.default.Img_band_game,M_p[i-1][j-1])
                    else:
                        BG.blit(B,M_p[i-1][j-1])
###########################################################################
# Classe principal onde há as funções principais do jogo
class APP:#################################################################
    cor=colors()
    window=Default.window
    title=Default.title
    TEMPO=threading.Thread(target=crono)
    
    def __init__(self):
        self.Padrao=Default()
        
        self.n = self.Padrao.n
        self.BG = None #valores iniciais para serem alterados
        self.run = True
        self.Tela= True
        self.Rodar=False
        self.first_time = True #primeira rodada
        self.cont_ft=0 #contador das primeira rodadas
        self.NewMatrix=False
        self.calc=True
        self.game_over=False
        self.reset_time=False
        self.win = False
        self.time_start=False #printar cronometro
        #****
        self.Key_master=True
        
        #objetos
        self.grid_b=Grid() 
        self.grid_b.n=self.n
        self.grid_f=Grid()
        self.grid_f.n=self.n
        
        self.Qb=None#round(self.n**2*0.15)#quantidade de bombas
        self.M_b=np.zeros([self.n+2,self.n+2])
        self.M_n=np.zeros([self.n+2,self.n+2])
        self.M_p=[]#lista de posições 
        self.M_v=np.zeros([self.n+2,self.n+2])#matriz de verificação
        self.print_matriz=1
        self.clock=pg.time.Clock()
    #Matriz########
    def bomba(self,pos_first_click): #gera bombas aleatoriamente em um local != do click
        n=self.n
        self.Qb=round(n**2*0.15)
        V=[] #salvar posições da bomba
        R=[] #salvar redor do click
        l=pos_first_click[1]
        m=pos_first_click[0]
        #salva os arredores do click
        for i in range(-1,2): #salvar redor do click
            for j in range(-1,2):
                R.append([l+i,m+j])
                
        i=0
        while(i<self.Qb):
            x=randint(1,n)
            y=randint(1,n)
            #novos locais e não pode estar no redor do click
            if ([x,y] not in V) and ([x,y] not in R):
                V.append([x,y]) #posições da bomba
                i+=1
        for j in V: #posições onde vão colocar as bombas
            self.M_b[j[0]][j[1]]=1     
    def Ver_redor(self,Mb,k,l):
        soma=0
        for i in range(-1,2):
            for j in range(-1,2):
                soma+=Mb[k+i][l+j]
        return soma

    def Num_redor(self):#M_bomb matriz de comparação; verificar a quantidade de bombas ao redor de M_n[i][j]
        
        aux=len(self.M_b[0])
        aux2=len(self.M_b[1])
        
        for i in range(1,aux-1):
            for j in range(1,aux2-1):
                if(self.M_b[i][j]==0):
                    self.M_n[i][j] = self.Ver_redor(self.M_b,i,j)
                else:
                    self.M_n[i][j] =-1
                    
        ###############       
    def Reset_param(self,N):
        #ATUALIZANDO PADRÕES
        self.n= N
        self.Qb=round(N**2*0.15)
        self.Padrao.n=N
        self.grid_b.n=N
        self.grid_f.n=N
        self.Padrao.IMG_redimensionada()
        self.M_b=np.zeros([N+2,N+2])
        self.M_n=np.zeros([N+2,N+2])
        self.M_v=np.zeros([N+2,N+2])
        self.grid_f.organizar_borda(self.M_v)
        
    def Button(self,text='Button',pos=2): #com base no que vai printar na tela inicial 
        if(pos==2):#x: um terço menos metade do tamanho da string +/- (para centralizar)
            x=Default.window[0]/3-(Default.window[0]/3)/8 
            y=Default.window[1]/3
            N_game=8
        elif(pos==3):
            x=Default.window[0]/3-(Default.window[0]/3)/8
            y=Default.window[1]*2/3
            N_game=12
        elif(pos==4):
            x=Default.window[0]*2/3-(Default.window[0]/3)/8
            y=Default.window[1]/3
            N_game=16
        else:
            x=Default.window[0]*2/3-(Default.window[0]/3)/8
            y=Default.window[1]*2/3
            N_game=20
        Tam=[150,150]
        mouse=pg.mouse.get_pos()
        mouse_click=pg.mouse.get_pressed()
        botao=pg.Surface(Tam)
        xi=x-75*2/3+10
        xf=xi+Tam[0]
        yi=y-70
        yf=yi+Tam[1]
        
        if(xi<=mouse[0]<=xf and yi<=mouse[1]<=yf):
            botao.fill(cor.gray)
            if(mouse_click[0]==1):
                for i in range(0,5):
                    botao.fill(cor.gray_e)
                    self.clock.tick(150)
                    botao.fill([150,250,150])
                    self.clock.tick(150)
                #garantir a mudança do nº de linhaxcoluna
                self.Reset_param(N_game)
                self.Tela=False
                sleep(0.1)
                
        else:
            botao.fill(cor.gray_e)
                
        self.BG.blit(botao,[xi,yi])
        f=pygame.font.SysFont('Arial',30)
        t=f.render(text, True, cor.green)
        B_pos=[x,y]
        self.BG.blit(t, B_pos)
    def Quit_game(self):
        global time_Stop
        self.BG.fill(cor.red_e)
        pg.display.update()
        #self.TEMPO
        #self.TEMPO._stop()
        time_Stop=True
        self.TEMPO.join()
        sleep(0.5)
        pg.quit()
    def draw_num(self): #função importante
        global time_Stop
        N_cor=cor.black
        n=self.n #numero de linhas=colunas
        size_font=round(320/n)
        dist=(Default.Game_area[0]/n) # larg de cada celula
        f=pg.font.SysFont('Arial',size_font) #objeto fonte
        x0,y0=dist/3,dist/3 #posição inicial, centraliada na celula
        x,y=x0,y0
        for i in range(1,len(self.M_b[0])):
            aux=(self.grid_b.Wx-Grid.esp)*0.3 
            if(i!=1):x+=dist
            for j in range(1,len(self.M_b[0])):
                if(j!=1):y+=dist
                else: y=y0
                #se verificou bomba, ou seja, foi clicado, muda imagem
                if(self.M_n[i][j]==-1): 
                    if(self.M_v[i][j]==1): #ter bomba e for verificado é game over
                        self.BG.blit(self.Padrao.Img_exp,[x-aux,y-aux*0.75])
                        self.game_over=True
                        self.time_start=False
                        self.reset_time==True 
                        time_Stop = True
                        self.grid_f.Game_over = True
                        for Ki in range(1,len(self.M_b[0])):
                            for Kj in range(1,len(self.M_b[1])):
                                if(self.M_n[Ki][Kj]==-1):
                                    if(Ki!=i and Kj!=j):
                                        self.BG.blit(self.Padrao.Img_bomb,self.M_p[Ki-1][Kj-1])
                    else:
                        self.BG.blit(self.Padrao.Img_bomb,[x-aux,y-aux*0.75])
                    t=f.render('', True, self.cor.red)#str(int(self.M_n[i][j]))
                else:
                    if(self.M_n[i][j]==0): text_cell =''
                    else: text_cell=str(int(self.M_n[i][j]))
                    
                    t=f.render(text_cell, True, N_cor)
                self.BG.blit(t,[x,y])
                
            
        
    def draw_tela_inicial(self):
        self.BG.fill(cor.white)
        for i in range(2,6):
            if(i*4<10):
                label="%2d  x %2d"%(4*i,4*i)
            else:
                label="%2d x %2d"%(4*i,4*i)
            self.Button(label,i)
        pg.display.update()
    def Time(self,pos,ligado=False):
        global segundos, minutos, hora,time_Stop
        
        if(self.reset_time==True):
            hora,minutos,segundos=0,0,0
            time_Stop=False
            self.reset_time=False
        #global segundos, minutos, hora
        font=pg.font.SysFont('Arial',25)
        if(ligado==False):
            txt_time="00:00:00"
        else:    
            txt_time="%2.d:%2.d:%2.d"%(hora,minutos,segundos)#"00:00:00"
        cronometro=font.render(txt_time, True, cor.black)
        self.BG.blit(cronometro,pos)
        #pg.display.update()
    def Mensagem(self, title="title", mensagem="messenger",func=0):
        global time_Stop
        tamX= Default.Game_area[0]*0.4
        tamY=Default.Game_area[1]*0.2
        M=pg.Surface([tamX,tamY])
        B=pg.Surface([tamX*0.3,tamY*0.2])
        mouse=pg.mouse.get_pos()
        mouse_c=pg.mouse.get_pressed()
        x=Default.Game_area[0]/2-tamX/2
        y=Default.Game_area[1]/2-tamY/2
        bx,by=Default.Game_area[0]/2-tamX*0.3/2,Default.Game_area[0]/2+tamY*0.2/2
        
        xi=bx
        xf=xi+tamX*0.3
        yi=by
        yf=yi+tamY*0.2
        M.fill(cor.gray)
        #interação com botão
        if(xi<=mouse[0]<=xf and yi*1.1<=mouse[1]<=yf*1.1):
            B.fill(cor.gray)
            if(mouse_c[0]==1):
                time_Stop=True
                self.TEMPO.join()
                app_game= APP()
                sleep(0.5) 
                #main(self,RESET_FASE=False,reset_dificuldade=False,N=None)
                app_game.main(True,False,self.n)
        else:
            B.fill(cor.gray_e)
        self.BG.blit(M,[x,y])
        self.BG.blit(B,[bx,by*1.1])
        t=pg.font.SysFont('Arial',25)
        t2=pg.font.SysFont('Arial',20)
        Mes_txt=t.render(mensagem, True, cor.black)
        B_txt=t2.render("ok", True, cor.black)
        txt_scoring="Seu tempo:  %d:%d:%.2d"%(hora,minutos, segundos)
        Score_txt=t2.render(txt_scoring, True, cor.black)
        
        self.BG.blit(B_txt,[bx+tamX*0.3/3,by*1.11]) #posicionar ele *problema
        if(func==0):
            self.BG.blit(Mes_txt,[x+tamX*0.3,y+tamY*0.3*0.85])
        elif(func==1):
            self.BG.blit(Mes_txt,[x+tamX*0.2,y+tamY*0.3*0.85])
            self.BG.blit(Score_txt,[x+tamX*0.2,y+tamY*0.45])
    def Button_score(self,txt="Button",y=350, funcao=0):
        
        tamX=(Default.window[0]-Default.Game_area[0])*0.8
        tamY=30
        #posição
        
        x=Default.Game_area[0]+tamX*0.1/0.8
        #y
        #mouse interação
        mouse=pg.mouse.get_pos()
        mouse_click=pg.mouse.get_pressed()
        Bt=pg.Surface([tamX,tamY])
        xi=x
        xf=xi+tamX
        yi=y
        yf=yi+tamY
        if(xi<=mouse[0]<=xf and yi<=mouse[1]<=yf):
            Bt.fill([140,140,140])
            if(mouse_click[0]==1):
                self.Tela=True
                Bt.fill([170,200,170])
                self.reset_time=True
                if(funcao==0):
                    app_game= APP()
                    app_game.main(False,True)
                elif(funcao==1):
                    app_game= APP()
                    app_game.main(True,False,self.n)
                self.run=False
                self.Quit_game()
        else:
            Bt.fill([170,170,170])
        self.BG.blit(Bt,[x,y])
        f=pg.font.SysFont('Arial',25)
        Bt_txt=f.render(txt, True, cor.black)
        self.BG.blit(Bt_txt,[Default.Game_area[0]+tamX/3,y+5])
    def draw_score(self):
        self.Button_score("Recomeçar",350,1)
        self.Button_score("Dificuldade",400)
        
        
        W=Default.Game_area
        mid=Default.window[0]-Default.Game_area[0]
        #imagens/objetos
        time = Default.Img_clock
        flag=Default.Img_band
        f=pg.font.SysFont('Arial',25)
        N_flag=self.grid_f.Qflags
        text="%d /%d"%(N_flag,self.Qb)
        flag_score=f.render(text, True, cor.black)
        #printando
        self.BG.blit(flag_score,[W[0]+mid/2-Default.tam_c*2/3,25+Default.tam_c])
        self.BG.blit(flag,[W[0]+mid/2-Default.tam_c/2,25])
        self.BG.blit(time,[W[0]+mid/2-Default.tam_c/2,100])
        if(self.time_start==True):
            self.Time([W[0]+mid/2-Default.tam_c-3,100+Default.tam_c],True)
        else:
            self.Time([W[0]+mid/2-Default.tam_c-3,100+Default.tam_c],True)
        #tiMe ficava aqui *
        
    def Ver_win(self):
        soma=0
        for i in range(1,len(self.M_v)-1):
            for j in range(1,len(self.M_v)-1):
                if(self.M_v[i][j]==1):
                    soma+=1
        if(soma==self.n**2-self.Qb):
            self.win=True
    def draw(self):
        #primeira rodada
        if(self.first_time==True):
            self.cont_ft+=1
            if(self.cont_ft>10):
                self.first_time==False
        
        global time_Stop
        self.clock.tick(50)
        self.BG.fill(cor.gray)#pinta tudo
        self.draw_score()
        if(self.first_time==True):
            self.cont_ft+=1
            if(self.cont_ft>5):
                self.first_time=False
        else:
            self.grid_b.Draw_back(self.BG,self.M_p,self.M_n) #desenha o de baixov
            self.draw_num() #desenha os numeros
            self.grid_f.Draw_front(self.BG,self.M_n, self.M_p,self.M_v)#desenha os blocos de cima [(BG,M_n,M_p,M_v):]
        if(self.grid_f.first_click==False and self.calc==True):
                    self.bomba(self.grid_f.pos_first_click)
                    self.Num_redor()
                    self.grid_f.Draw_front(self.BG,self.M_n, self.M_p,self.M_v)
                    self.calc=False
                    if(self.Rodar==True):
                        self.TEMPO.start()
                        self.Rodar=False
                    self.reset_time=True
                    time_Stop=False
                    self.time_start==True
        #################verificar se ganhou##############
        self.Ver_win()
        ##################################################
        if(self.game_over==True):
            self.Mensagem("titulo","GAME OVER")
        elif(self.win==True):
            time_Stop=True
            self.Mensagem("titulo","CONGRATULATIONS",1)
            #print("game over")
        pg.display.update()#atualiza tela
        if(self.grid_f.first_click==False and self.Key_master==True):
            self.Key_master=False
            #printar a cola
            print(self.M_n[1:-1,1:-1].transpose(),">",len(self.M_n),self.Qb)
        
    def main(self,RESET_FASE=False,reset_dificuldade=False,N=None): #True,False,self.n)
        global segundos, minutos, hora, time_Stop#, Thr_quit
        #self.TEMPO.re start()
        segundos, minutos, hora= 0,0,0
        time_Stop=False
        if(RESET_FASE==False and reset_dificuldade==False):
            self.Rodar=True
            time_Stop=True
            self.reset_time=True
        elif(N==None):
            self.Tela=True
            time_Stop=True
            self.reset_time=True

        else:
            self.Rodar==False
        if(RESET_FASE==True and N!=None):
            self.Reset_param(N)
            self.Tela=False
        hora,minutos,segundos=0,0,0
        pg.init()
        pg.font.init()
        self.BG=pg.display.set_mode(Default.window)
        pg.display.set_caption(Default.title)
        self.run=True        
        self.settings()
        self.Quit_game()
        
    def settings(self):
        while(self.run):
            if(self.Tela==False):
                self.draw()
                self.clock.tick(100)
            for event in pg.event.get():
                if event.type == QUIT:
                    self.run=False

                else:
                    if(self.Tela==True):
                        self.draw_tela_inicial()
                    
theapp=APP()
theapp.main()


