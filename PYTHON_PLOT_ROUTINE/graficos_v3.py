# -*- coding: utf-8 -*-
""" ********************************************
SCRIPT PARA PLOTAGEM DA CURVA DE CONVERGÊNCIA
DAS ANÁLISES EM AXISSIMETRIA
Versão: 2023.1
Situação : Teste (11/07/2020) 
******************************************** """ 

# Importar bibliotecas
import pandas as pd                   # importa o pacote para manmipular tabelas 
import matplotlib.pyplot as plt       # importa o módulo para plotagem
import numpy as np                    # importa o pacote para operar arrays
from matplotlib import rc             # importa a função com os parâmetros de configuração da plotagem
from scipy.interpolate import interp1d
#
# Parametros para plotagem
todos_passos = 1                # 1 - plota todos os passos
npts         = 500              # numero de pontos para o gráfico

# Definição de configurações de plotagem
plt.rc('font',**{'family':'Times New Roman','size' :16},)
plt.rcParams['axes.unicode_minus'] = False
plt.rc('text', usetex=True)
plt.rc('axes', labelsize=14)
plt.rc('xtick', labelsize=16) 
plt.rc('ytick', labelsize=16)
plt.rc('lines', lw=1.0,color='k')
plt.rc('axes',lw=0.75)
plt.rc('legend',fontsize=14)

# Lendo arquivo de parâmetros
parametros = pd.read_csv('parametros.txt',
                         skiprows=2, 
                         skipfooter = 1, 
                         engine='python').values

# Preenchendo algumas variáveis
for i,x in enumerate (parametros[:,1]):
    if x == 'NESC    ':
        # Numero de escavações
        NESC = int(float(parametros[i,2]))
    if x == 'UMAXIMOFINAL':
        # Convergência máxima
        umaxfinal = float(parametros[i,2])
    if x == 'L2      ':
        # Comprimento do trecho escavado
        L2 = float(parametros[i,2])   
    if x == 'RE      ':
        # Raio do túnel
        Re = float(parametros[i,2]) 
    if x == 'NANALISES':
        # Numero de escavações
        NANALISES = int(float(parametros[i,2]))  
    if x == 'SMAXIMOFINAL':
        # Numero de escavações
        smaximofinal = float(float(parametros[i,2]))          
    if x == 'SMINIMOFINAL':
        # Numero de escavações
        sminimofinal = float(float(parametros[i,2]))          
    if x == 'NESC1   ':
         # Numero de escavações
         NESC1 = int(float(parametros[i,2])) 
    if x == 'UMAXIMOFINAL1':
        # Convergência máxima
        umaxfinal1 = float(parametros[i,2])         
    if x == 'RE1     ':
        # Raio do túnel
        Re1 = float(parametros[i,2]) 
    if x == 'SMAXIMOFINAL1':
        # Numero de escavações
        smaximofinal1 = float(float(parametros[i,2]))          
    if x == 'SMINIMOFINAL1':
        # Numero de escavações
        sminimofinal1 = float(float(parametros[i,2]))  

def graficar(arquivo,titulo,eixox,eixoy,minimo,maximo,nesc,lface,raio,lfacestr,figura):
    
    # Lendo arquivo do perfil de convergencias       
    data = pd.read_csv(arquivo,
                   delim_whitespace= True).values

    # Definindo as dimensões do layout da figura
    plt.figure(figura,figsize = (9,5))

    # Calculando o número de passos
    nanalises = len(data[0,:])-1

    # Plotando as curvas
    for i in range(2,len(data[0,:])):
        #
        # Coletando dados
        x = data[:,1]
        y = data[:,i]
        xmax = data[nesc,1]
        #
        # Suavizando a curva
        interp_func = interp1d(x,y,kind=2)
        x_smooth = np.linspace(min(x),max(x),npts)
        y_smooth = interp_func(x_smooth)
        #
        # Invertendo o eixo x
        x_smooth = -(x_smooth - max(x_smooth))
        #
        # Plotando e identificandoa curva
        if i!= nesc+2:
            if todos_passos == 1:
                plt.plot(x_smooth,y_smooth,color ='gray',zorder = 1,alpha = (i+70)/(len(data[0,:])+70))
        elif i == nesc+2:
                plt.plot(x_smooth,y_smooth,'#1aff1a',lw = 3,zorder = 15,label = 'final excavation profile')
        if i == nanalises: 
            plt.plot(x_smooth,y_smooth,'b',lw = 3,zorder = 15,label = 'long-term profile')
        
    # Formatando os eixos
    plt.axvline(x=lface/raio,color = 'k', label = lfacestr, linestyle = '--')
    plt.ylim([minimo, maximo])
    plt.xlim([0, lface/raio*1.2])
    plt.ylabel(eixoy)
    plt.xlabel(eixox)
    plt.legend()
    plt.grid(True) 
    plt.title(titulo) 
    plt.autoscale(axis='y')
    
    # Formatando a legenda
    plt.legend(
        loc = 'center',
        shadow=True,
        framealpha = 0.8,
        ncol = 3,
        columnspacing = 0.5,
        bbox_to_anchor=(0.5, -0.2))
    
    # Salvando em arquivo    
    plt.savefig('profile'+ str(figura) + '.pdf')
    

arquivo = 'convergencias_90.txt'
titulo = 'Convergence Profiles'
eixox = r'$y/R_e$'  
eixoy = r'$U=-u(R_e,90^\circ)/R_{e}$ [\%]'
minimo = 0
maximo = umaxfinal*1.2
nesc = NESC-1
raio = Re
lface = L2
lfacestr = 'last excavation face'
figura = 1
graficar(arquivo,titulo,eixox,eixoy,minimo,maximo,nesc,lface,raio,lfacestr,figura)

arquivo = 'pressure_90.txt'
titulo = 'Pressure Profiles'
eixox = r'$y/R_e$'  
eixoy = r'$p(R_e,90^\circ)$ [MPa]'
minimo = sminimofinal
maximo = smaximofinal
nesc = NESC
raio = Re
lface = L2
lfacestr = 'last excavation face'
if smaximofinal < 0:
    maximo = smaximofinal*1/2
figura = 2
graficar(arquivo,titulo,eixox,eixoy,minimo,maximo,nesc,lface,raio,lfacestr,figura)

# arquivo = 'convergencias1_90.txt'
# titulo = 'Gallery Convergence Profiles'
# eixox = r'$x/R_{e_1}$'  
# eixoy = r'$U_1=-u_1(R_{e1},90^\circ)/R_{e1}$ [\%]'
# minimo = 0
# maximo = umaxfinal1*1.2
# nesc = NESC1
# raio = Re1
# lface = 16*Re/2
# lfacestr = 'center of longitudinal tunnel'
# figura = 3
# graficar(arquivo,titulo,eixox,eixoy,minimo,maximo,nesc,lface,raio,lfacestr,figura)

# arquivo = 'pressure1_90.txt'
# titulo = 'Gallery Pressure Profiles'
# eixox = r'$x/R_{e_1}$'  
# eixoy = r'$p_1(R_{e1},90^\circ)$ [MPa]'
# minimo = sminimofinal1*1.2
# maximo = smaximofinal1*1.2
# nesc = NESC1
# raio = Re1
# lface = 16*Re/2
# lfacestr = 'center of longitudinal tunnel'
# if smaximofinal1 < 0:
#     maximo = smaximofinal1*1/2
# figura = 4
# graficar(arquivo,titulo,eixox,eixoy,minimo,maximo,nesc,lface,raio,lfacestr,figura)