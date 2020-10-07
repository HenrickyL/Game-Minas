#Biblioteca feita por Henricky de Lima monteiro
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv
from scipy import linalg
import numpy.matlib
from random import *


def MinQuad2(X,Y): #funcao que da os valores de A,B e C da funcao y=A+Bx+Cx^2
	A=len(X)
	B=sum(X)
	C=sum(X**2)
	D=sum(X)
	E=sum(X**2)
	F=sum(X**3)
	G=sum(X**2)
	H=sum(X**3)
	I=sum(X**4)

	x=sum(Y)
	y=sum(X*Y)
	z=sum((X**2)*Y)

	VarC= (((z-(G*x)/A))-((H-(G*B)/A)*(y-(D*x)/A)/(E-D*B/A)))/((F-G*C/A)-((H-G*B/A)*(F-D*C/A)/(E-(D*B)/A)))

	VarB= ((y-D*x/A)/(E-D*B/A))-(VarC)*(F-D*C/A)/(E-D*C/A) 

	VarA=((x/A)-(B/A*VarB))-((C/A)*(VarC))
	return VarA,VarB,VarC
##############################################33

#Metodos quadrados e plotagem de grafico
def graficL(x,y,eixox,eixoy,titulo,L): #inserir os vetores com valores de x e y
                                #Tem que usar essas bibliotecas
    #import numpy as np
    #import matplotlib.pyplot as plt
    #from numpy.linalg import inv
    #from scipy import linalg
    #import numpy.matlib
    
    Y1=y
    X1=x
    #matriz                                                                #
    MX1=np.matlib.zeros((len(x),2))#Linhas x colunas
    z=np.matlib.zeros((len(y),1))#y transposto para que fique na vertical, pos o padrao e horizontal(vetor python)
    for i in range(0,len(x)):
        for j in range(0,1):
            MX1[i,0]=1             #primeira colona so de 1
            MX1[i,1]=X1[i]         #segunda coluna os valores de X1
            z[i,0]=Y1[i]
    #                                                                      #
    At1=MX1.transpose()#A Transposto(At)
    AtA1=At1.dot(MX1)#At.A
    AtY1=At1.dot(z)#At.b  
    C1=linalg.solve(AtA1,AtY1)#resolucao do sistema  de equacoes
    #
    print(C1)
    x1=np.linspace(np.min(X1),np.max(X1),500,endpoint="true")#valores genericos de x  
    y1=C1[0]+C1[1]*x1 #<------ Muda-se a aqui a funcao
    plt.plot(x1,y1)
    #
    R1=np.corrcoef(X1,Y1)*100#gera matriz com valor R^2(procurar o valor positivo)
    tR1=str(round(R1[0,1],2))#transformando em string - com o valor da  matriz
    textR1=r"$R$="+tR1+"%" #criando um texto
    #
    plt.plot(X1,Y1,linestyle=":", color='green',marker="o",label=L)#plotando grafico
    plt.text(np.max(X1)-0.2*np.max(X1),np.max(Y1),textR1)#posicao do r^2
    #
    plt.title(titulo, fontsize=20)#Titulo do grafico
    plt.ylabel(eixoy, fontsize=15)#Unidade eixo x
    plt.xlabel(eixox, fontsize=15)#Unidade eixo y
    #
    print("y=A+Bx")
    print("coeficiente angulas(B): ",str(C1[1]))
    print("A:",str(C1[0]))
    print ('R=', R1[0,1])
    plt.legend(loc='lower right', prop={'size':12})
###############################################################
def grafic(x,y,DotBolean,LineE,LineT,Label,LineBolean): #inserir os vetores com valores de (x , y,True, 'o:','-','massa',True,'lower right')
                                #Tem que usar essas bibliotecas
    #import numpy as np
    #import matplotlib.pyplot as plt
    #from numpy.linalg import inv
    #from scipy import linalg
    #import numpy.matlib
    
    Y1=y
    X1=x
    #matriz                                                                #
    MX1=np.matlib.zeros((len(x),2))#Linhas x colunas
    z=np.matlib.zeros((len(y),1))#y transposto para que fique na vertical, pos o padrao e horizontal(vetor python)
    for i in range(0,len(x)):
        for j in range(0,1):
            MX1[i,0]=1             #primeira colona so de 1
            MX1[i,1]=X1[i]         #segunda coluna os valores de X1
            z[i,0]=Y1[i]
    #                                                                      #
    At1=MX1.transpose()#A Transposto(At)
    AtA1=At1.dot(MX1)#At.A
    AtY1=At1.dot(z)#At.b  
    C1=linalg.solve(AtA1,AtY1)#resolucao do sistema  de equacoes
    #
    k1=float(C1[0])
    k2=float(C1[1])
    if (DotBolean==True) :
        print('Com pontos')
        plt.plot(X1,Y1,LineE,label=Label)#plotando grafico

    if (LineBolean==True) :
	    print('Com linha')
	    x1=np.linspace(np.min(X1),np.max(X1),500,endpoint="true")#valores genericos de x  
	    y1=C1[0]+C1[1]*x1 #<------ Muda-se a aqui a funcao
	    plt.plot(x1,y1,LineT,label='y=({:3.2})+({:3.2})x \n({:1})'.format(k1,k2,Label))
	    #
    R2(X1,Y1)#r^2 
    #
    print("y=A+Bx")
    print("coeficiente angulas(B): ",str(C1[1]))
    print("A:",str(C1[0]))
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0,prop={'size':12})#legenda ao lado do grafico

###############################################################
def Errgrafic(x,y,dx,dy,LinhaGen,cor,Ponto,L): #inserir os vetores com valores de x e y
                                #Tem que usar essas bibliotecas
    #import numpy as np
    #import matplotlib.pyplot as plt
    #from numpy.linalg import inv
    #from scipy import linalg
    #import numpy.matlib
    #from random import *

    
    Y1=y
    X1=x
    #matriz                                                                #
    MX1=np.matlib.zeros((len(x),2))#Linhas x colunas
    z=np.matlib.zeros((len(y),1))#y transposto para que fique na vertical, pos o padrao e horizontal(vetor python)
    for i in range(0,len(x)):
        for j in range(0,1):
            MX1[i,0]=1             #primeira colona so de 1
            MX1[i,1]=X1[i]         #segunda coluna os valores de X1
            z[i,0]=Y1[i]
    #                                                                      #
    At1=MX1.transpose()#A Transposto(At)
    AtA1=At1.dot(MX1)#At.A
    AtY1=At1.dot(z)#At.b  
    C1=linalg.solve(AtA1,AtY1)#resolucao do sistema  de equacoes
    #
    print(C1)
    k1=float(C1[0])
    k2=float(C1[1])
    #print(k1,k2)
    x1=np.linspace(np.min(X1),np.max(X1),500,endpoint="true")#valores genericos de x   	
    y1=C1[0]+C1[1]*x1 #<------ Muda-se a aqui a funcao
    plt.plot(x1,y1,LinhaGen,label='y=({:3.2})+({:3.2})x'.format(k1,k2))
    #
    R1=np.corrcoef(X1,Y1)*100#gera matriz com valor R^2(procurar o valor positivo)
    tR1=str(round(R1[0,1],2))#transformando em string - com o valor da  matriz
    textR1=r"$R$="+tR1+"%" #criando um texto
    #
    print(')))))',R1)
    plt.errorbar(X1,Y1,xerr=dx,yerr=dy,linestyle=':', color=cor,marker=Ponto,label=L)#plotando grafico
    plt.text(np.max(X1)-0.2*np.max(X1),np.max(Y1),textR1)#posicao do r^2
    #
    #
    #print("y=A+Bx")
    #print("coeficiente angulas(B): ",str(C1[1]))
    #print("A:",str(C1[0]))
    #print ('R=', R1[0,1])
    plt.legend(loc='lower right', prop={'size':12})
###########################################################3
def incM(dq,q,dr,r,s):#multiplication
	ds=s*np.sqrt((dq/q)**2+(dr/r)**2)
	return ds
############################################################
def incP(x,n,dx,q): #potencia q=x^n
	dq=n*q*(dx/x)
	return dq	
def incMed(ds):#media
	dmed=np.sqrt(sum(ds**2))/len(ds)
	return dmed
###########################################
def R2(X1,Y1): #gerar R - coeficiente de confiabilidade
    R1=np.corrcoef(X1,Y1)*100#gera matriz com valor R^2(procurar o valor positivo)
    tR1=str(round(R1[0,1],2))#transformando em string - com o valor da  matriz
    textR1=r'$R=$'+ tR1+'%' #criando um texto
    #Posicoes aleatorias para o r2
    Q=randrange(90,110,5)/100
    plt.text(0.9*max(X1),Q*np.max(Y1),textR1)#posicao do r^2

