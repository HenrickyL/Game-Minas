#backup avanços finais do dia 13-14/06
#avanços no quesito tentar organizar a função do 1ºclick
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
    title="Minas"
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
    def Red_img(n,img):
        A=(82.14895971050655, -3.000135777641224)
        y=A[0]+n*A[1]
        #
        #k=[60,45,30,25]
        l=round(y)
        re_size=[l,l]
        img = pg.transform.scale(img, re_size)
    Red_img(n,Img_bomb)
    Red_img(n,Img_exp)
    Red_img(n,Img_band_game)
    Red_img(n,Img_duv)

###########################        
class Grid: # crindo linhas verticais e horizontais de tamanho seguindo padrões.
    first_click=True
    first_roll=True
    pos_first=None
    Qflags=0
    G_cor=cor.white
    G_cor_f=cor.gray_e
    n=Default.n
    #salvar var 1 vez
    Sv=True
    #organizar Mv 1 vez
    Omv=True
    
    esp=2
    Wd=Default.Game_area
    Wx=int((Wd[0])/n)
    Wy=int((Wd[1])/n)
    B=pg.Surface([Wx-esp,Wy-esp])
    B.fill(G_cor)
    clock=pg.time.Clock()

    def Draw_back(self,BG,M_p):
        e=self.esp
        l,m=0,0
        for i in range(e,self.Wd[0],self.Wx):
            l+=1
            aux=[]
            for j in range(e,self.Wd[1],self.Wy):
                m+=1
                p=[i,j]
                self.B.fill(cor.white)
                BG.blit(self.B,p)
                #criar matriz de posições
                aux.append(p)
            if(self.Sv==True):
                M_p.append(aux)
        self.Sv=False
    def organizar_borda(self,Mv):
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
    def Ver_redor_click(self,Mn,Mv,pos_click):
        p=pos_click
        x=p[0]
        y=p[1]
        print(">",x,y,Mn[x][y])
        if(Mv[x][y]==0 and Mn[i][j]==0):#and x>=0 and y>=0):
            Mv[x][y]=1
            self.Ver_redor_click(Mn,Mv,[x-1,y])
            self.Ver_redor_click(Mn,Mv,[x,y-1])
            self.Ver_redor_click(Mn,Mv,[x+1,y])
            self.Ver_redor_click(Mn,Mv,[x,y+1])
             
            
    def Draw_front(self,BG,M_n,M_p,M_v):
        mouse=pg.mouse.get_pos()
        mouse_c=pg.mouse.get_pressed()
        
        self.B.fill(cor.gray_e)
        e=self.esp
        for i in range(1,len(M_v[0])-1):
            for j in range(1,len(M_v[1])-1):
                if(M_v[i][j]==0 and self.first_roll==False): # não rodar na primeira *
                    pos=M_p[i-1][j-1]#-1 pela matriz ser menor que a Mn
                    xi=pos[0]
                    xf=xi+self.Wx
                    yi=pos[1]
                    yf=yi+self.Wy
                    if(xi<=mouse[0]<=xf and yi<=mouse[1]<=yf):
                        self.B.fill([120,120,120])
                        self.clock.tick(100)
                        if(mouse_c[0]==1):
                            M_v[i][j]=1
                            if(self.first_click==True):
                                self.pos_first_click=[i,j]
                                self.first_click=False
                             #verificar ao redor
                            self.Ver_redor_click(M_n,M_v,[i,j])
                        
                    else:
                        self.B.fill(cor.gray_e)
                    BG.blit(self.B,M_p[i-1][j-1])
                else:
                    self.Draw_back(BG,M_p)# * rodarpara gerar Mp
                    self.first_roll=False
                    self.Draw_front(BG,M_n,M_p,M_v) #rodar para colocar os blocos escuros
###########################################################################
# Classe principal onde há as funções principais do jogo
class APP:#################################################################
    cor=colors()
    window=Default.window
    title=Default.title
    
    def __init__(self):
        self.n=Default.n
        self.BG = None
        self.run = True
        self.Tela= True
        self.NewMatrix=False
        self.calc=True
        
        self.Default_g=Default()
        
        self.grid_b=Grid()
        self.grid_b.n=self.n
        self.grid_f=Grid()
        self.grid_f.n=self.n
        
        self.Qb=round(self.n**2*0.15)#quantidade de bombas
        self.M_b=np.zeros([self.n+2,self.n+2])
        self.M_n=np.zeros([self.n+2,self.n+2])
        self.M_p=[]#lista de posições 
        self.M_v=np.zeros([self.n+2,self.n+2])#matriz de verificação
        self.print_matriz=1
        self.clock=pg.time.Clock()
    #Matriz########
    def bomba(self,pos_first_click):
        n=Default.n
        i=0
        V=[]
        p=pos_first_click
        while(i<self.Qb):
            x=randint(1,n)
            y=randint(1,n)
            if [x,y] not in V and [x,y]!=p:
                V.append([x,y])
                i+=1
        for j in V:
            self.M_b[j[0]][j[1]]=1     
    def Ver_redor(self,Mb,k,l):
        soma=0
        for i in range(-1,2):
            for j in range(-1,2):
                soma+=Mb[k+i][l+j]
        return soma

    def Num_redor(self):#M_bomb matriz de comparação
        
        aux=len(self.M_b[0])
        aux2=len(self.M_b[1])
        
        for i in range(1,aux-1):
            for j in range(1,aux2-1):
                if(self.M_b[i][j]==0):
                    self.M_n[i][j] = self.Ver_redor(self.M_b,i,j)
                else:
                    self.M_n[i][j] =-1
                    
        ###############       
    
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
                    self.clock.tick(20)
                    botao.fill([150,250,150])
                    self.clock.tick(150)
                self.n= N_game
                self.grid_b.n=self.n
                self.grid_f.n=self.n
                #reajustando as matrizes:
                self.M_b=np.zeros([self.n+2,self.n+2])
                self.M_n=np.zeros([self.n+2,self.n+2])
                self.M_p=[]#lista de posições 
                self.M_v=np.zeros([self.n+2,self.n+2])
                #ajustando M_v para bordas =1
                self.grid_f.organizar_borda(self.M_v)
                self.Tela=False
                #sleep(3)
                self.draw()
                
                
        else:
            botao.fill(cor.gray_e)
                
        self.BG.blit(botao,[xi,yi])
        f=pygame.font.SysFont('Arial',30)
        t=f.render(text, True, cor.green)
        B_pos=[x,y]
        self.BG.blit(t, B_pos)
    def Quit_game(self):
        self.BG.fill(cor.red_e)
        pg.display.update()
        sleep(0.5)
        pg.quit()
    def draw_num(self):
        N_cor=cor.black
        n=self.n #numero de linhas=colunas
        size_font=round(320/n)
        dist=(Default.Game_area[0]/n) # larg de cada celula
        f=pg.font.SysFont('Arial',size_font) #objeto fonte
        x0,y0=dist/3,dist/3 #posição inicial, centraliada na celula
        x,y=x0,y0
        for i in range(1,len(self.M_b[0])):
            aux=(Grid.Wx-Grid.esp)/3
            if(i!=1):x+=dist
            for j in range(1,len(self.M_b[0])):
                if(j!=1):y+=dist
                else: y=y0
                if(self.M_n[i][j]==-1):
                    self.BG.blit(Default.Img_bomb,[x-aux,y-aux*0.75])
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
    def Time(self,pos):
        #global segundos, minutos, hora
        font=pg.font.SysFont('Arial',25) 
        txt_time= "00:00:00"           #"%d:%d:%d"%(hora,minutos,segundos)
        cronometro=font.render(txt_time, True, cor.black)
        self.BG.blit(cronometro,pos)
        
    def draw_score(self):
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
        self.Time([W[0]+mid/2-Default.tam_c-3,100+Default.tam_c])
    def draw(self,):
        self.BG.fill(cor.gray)#pinta tudo
        self.draw_score()
        
        self.grid_f.Draw_front(self.BG,self.M_n, self.M_p,self.M_v)#desenha os blocos de cima [(BG,M_n,M_p,M_v):]
        if(self.grid_f.first_click==True and self.calc==True):
                    self.bomba(self.grid_f.pos_first_click)
                    self.Num_redor()
                    self.calc=False
        self.grid_b.Draw_back(self.BG,self.M_p) #desenha o de baixo
        self.draw_num() #desenha os numeros
        pg.display.update()#atualiza tela
    def main(self):
        hora,minutos,segundos=0,0,0
        pg.init()
        pg.font.init()
        self.BG=pg.display.set_mode(Default.window)
        pg.display.set_caption(Default.title)
        self.run=True
        #TRABALHANDO COM TEMPO
        TEMPO=threading.Thread(target=crono,args=())
        TEMPO.start()
        #
        
        self.settings()
        self.Quit_game()
        
        
    def settings(self):
        while(self.run):
            for event in pg.event.get():
                if event.type == QUIT:
                    self.run=False
                else:
                    if(self.Tela==True):
                        self.draw_tela_inicial()
                    else:
                        self.draw()
                    
                    

theapp=APP()
theapp.main()

