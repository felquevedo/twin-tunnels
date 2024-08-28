# -*- coding: utf-8 -*-
""" ********************************************
SCRIPT PARA PLOTAGEM DA CURVA DE CONVERGÊNCIA
DAS ANÁLISES EM AXISSIMETRIA
Versão: 2023.1
Situação : Teste (11/07/2020) 
******************************************** """ 

#%% 1. IMPORTAR BIBLIOTECAS

import pandas as pd                    # importa o pacote para manmipular tabelas 
import matplotlib.pyplot as plt        # importa o módulo para plotagem
from scipy.signal import savgol_filter # importa filtro
import locale                          # importa módulo para definir a localização usada no ponto decimal
from matplotlib.ticker import StrMethodFormatter # importa módulo para formatar eixo
import numpy as np

#%% 2. FUNÇÃO GRAFICAR
def graficar_secao_deformada(arquivox, arquivoy,                # nome do arquivo de leitura
                             titulo,                            # titulo do gráfico
                             xmin,xmax,                         # intervalo eixo x
                             ymin,ymax,                         # intervalo eixo y
                             ncoluna,                           # numero da coluna (dados em y)
                             lblcoluna,                         # legenda da coluna
                             cor,tamanho,ordem,alpha,estilo,    # formatacao
                             figura):

    # Lendo arquivo de dados      
    datax = pd.read_csv(arquivox,delim_whitespace= True,header=None).values
    datay = pd.read_csv(arquivoy,delim_whitespace= True,header=None).values
    
    # Definindo as dimensões do layout da figura
    fig = plt.figure(figura,figsize = (6,6))
    
    # Retirando eixos
    plt.axis('off')
    plt.ylim([ymin, ymax])
    plt.xlim([xmin, xmax])
    
    # Coletando os dados da indeformada
    x =  datax[:,1]
    y =  datax[:,2]
    y_espelhado = [-yi for yi in y]
    
    # Plotando indeformada
    if apenasdeformada == False:
        plt.plot(x, y, color=cor, lw = tamanho, label = 'indeformada')
        plt.plot(x,y_espelhado, color='k', lw = tamanho)
    
    # Plotando nó a 90 graus
    plt.plot(x[16], y[16], marker='o', markersize=5, color='k')
        
    
    # Coletando os dados da deformada
    ux = datax[:,ncoluna]
    uy = datay[:,ncoluna]
    
    # Escalando a deformada
    x = x+ux*escala
    y = y+uy*escala
    y_espelhado = [-yi for yi in y]
    
    # Plotando a deformada
    plt.plot(x, y,   color = cor,
                     zorder = ordem, 
                     linestyle=estilo, 
                     lw = tamanho, 
                     alpha = alpha, 
                     label = lblcoluna)
    
    plt.plot(x,y_espelhado,   color = cor,
                     zorder = ordem, 
                     linestyle=estilo, 
                     lw = tamanho, 
                     alpha = alpha)

    # Plotando nó a 90 graus
    plt.plot(x[16], y[16], marker='o', markersize=5, color=cor)
  
    
    # Plotando linha
    plt.axhline(y=0, color='k', alpha = 0.5, lw = 1)
    plt.axvline(x=0, color='k', alpha = 0.5, lw = 1)
    
    # Formatando a legenda
    plt.legend(
        loc = 1,
        shadow=False,
        framealpha = 0,
        ncol = 1,
        bbox_to_anchor=(0.5, 0),
        columnspacing = 0.5,
        fontsize="11")
    
    # adicionando título
    plt.title(titulo, fontsize = 16, fontweight="bold")

    # Salvando em arquivo    
    plt.savefig(str(titulo) + '.pdf', 
                dpi = fig.dpi, 
                bbox_inches='tight', 
                pad_inches=0.2)

dicncolunalongterm = {

    'E_CRE_SG_D1_INF_AXI': 99,
    'E_CRE_CG_D1_16RE_3D': 127,
    'E_CRE_CG_D1_8RE_3D': 110,
    'E_CRE_CG_D1_4RE_3D': 101,
    
    'EP_SR_SG_D1_INF_AXI': 99,
    'EP_SR_SG_D1_16RE_3D': 99,
    'EP_SR_SG_D1_8RE_3D': 99,
    'EP_SR_SG_D1_4RE_3D': 99,
    
    'EP_SR_CG_D1_16RE_3D': 127,
    'EP_SR_CG_D1_8RE_3D': 110,
    'EP_SR_CG_D1_4RE_3D': 101,
 
    'EP_CRE_SG_D1_INF_AXI': 99,
    'EP_CRE_CG_D1_16RE_3D': 127,
    'EP_CRE_CG_D1_8RE_3D': 110,
    'EP_CRE_CG_D1_4RE_3D': 101,
    
    'EP_CRE_SG_D1_16RE_3D': 99,
    'EP_CRE_SG_D1_8RE_3D': 99,
    'EP_CRE_SG_D1_4RE_3D': 99,

    'VP_CRE_SG_D1_INF_AXI': 129,
    'VP_CRE_CG_D1_16RE_3D': 157,
    'VP_CRE_CG_D1_8RE_3D': 140,
    'VP_CRE_CG_D1_4RE_3D': 131, 
    
    'VP_CRE_SG_D1_16RE_3D': 129,
    'VP_CRE_SG_D1_8RE_3D': 129,
    'VP_CRE_SG_D1_4RE_3D': 129, 

    'EPVP_CRE_SG_D1_INF_AXI': 129,
    'EPVP_CRE_CG_D1_16RE_3D': 157,
    'EPVP_CRE_CG_D1_8RE_3D': 140,
    'EPVP_CRE_CG_D1_4RE_3D': 131,
    
    'EPVP_CRE_SG_D1_16RE_3D': 129,
    'EPVP_CRE_SG_D1_8RE_3D': 129,
    'EPVP_CRE_SG_D1_4RE_3D': 129,
    
    'EPVP_CRVE_SG_D1_INF_AXI': 129,
    'EPVP_CRVE_CG_D1_16RE_3D': 157,
    'EPVP_CRVE_CG_D1_8RE_3D': 140,
    'EPVP_CRVE_CG_D1_4RE_3D': 131,
    
    'EPVP_CRVE_SG_D1_16RE_3D': 129,
    'EPVP_CRVE_SG_D1_8RE_3D': 129,
    'EPVP_CRVE_SG_D1_4RE_3D': 129,
       
    }

dicncolunafinalexcavation = {

    'VP_CRE_SG_D1_INF_AXI': 99,
    'VP_CRE_CG_D1_16RE_3D': 127,
    'VP_CRE_CG_D1_8RE_3D': 110,
    'VP_CRE_CG_D1_4RE_3D': 101,
    
    'VP_CRE_SG_D1_16RE_3D': 99,
    'VP_CRE_SG_D1_8RE_3D': 99,
    'VP_CRE_SG_D1_4RE_3D': 99,

    'EPVP_CRE_SG_D1_INF_AXI': 99,
    'EPVP_CRE_CG_D1_16RE_3D': 127,
    'EPVP_CRE_CG_D1_8RE_3D': 110,
    'EPVP_CRE_CG_D1_4RE_3D': 101,
    
    'EPVP_CRE_SG_D1_16RE_3D': 99,
    'EPVP_CRE_SG_D1_8RE_3D': 99,
    'EPVP_CRE_SG_D1_4RE_3D': 99,
    
    'EPVP_CRVE_SG_D1_INF_AXI': 99,
    'EPVP_CRVE_CG_D1_16RE_3D': 127,
    'EPVP_CRVE_CG_D1_8RE_3D': 110,
    'EPVP_CRVE_CG_D1_4RE_3D': 101,
    
    'EPVP_CRVE_SG_D1_16RE_3D': 99,
    'EPVP_CRVE_SG_D1_8RE_3D': 99,
    'EPVP_CRVE_SG_D1_4RE_3D': 99,
       
    }

figura = 1



#%% DEFORMATION OF SECTION EP_CRE_CG_D1_16RE_3D
modelo      = 'EP_CRE_CG_D1_16RE_3D'
figura      = figura+1
arquivox    = modelo + '\convergencias_x.txt'
arquivoy    = modelo + '\convergencias_y.txt'
titulo      = modelo
escala      = 50
xmin        = -1.1
xmax        = 1.1
ymin        = -1.1
ymax        = 1.1
tamanho     = 2
ordem       = 1
alpha       = 1

lblcoluna           = 'D1_4Re'
ncoluna             = dicncolunalongterm[modelo] +1
cor                 = "k"
estilo              = "dashed"
apenasdeformada     = False
graficar_secao_deformada(arquivox, arquivoy,                
                             titulo,                            
                             xmin,xmax,                        
                             ymin,ymax,                         
                             ncoluna,                           
                             lblcoluna,                         
                             cor,tamanho,ordem,alpha,estilo,    
                             figura)

modelo      = 'EP_CRE_CG_D1_8RE_3D'
figura      = figura
arquivox    = modelo + '\convergencias_x.txt'
arquivoy    = modelo + '\convergencias_y.txt'

lblcoluna           = 'D1_8Re'
ncoluna             = dicncolunalongterm[modelo] +1
cor                 = "g"
estilo              = "dashed"
apenasdeformada     = True
graficar_secao_deformada(arquivox, arquivoy,                
                             titulo,                            
                             xmin,xmax,                        
                             ymin,ymax,                         
                             ncoluna,                           
                             lblcoluna,                         
                             cor,tamanho,ordem,alpha,estilo,    
                             figura)

modelo      = 'EP_CRE_CG_D1_4RE_3D'
figura      = figura
arquivox    = modelo + '\convergencias_x.txt'
arquivoy    = modelo + '\convergencias_y.txt'

lblcoluna           = 'D1_4Re'
ncoluna             = dicncolunalongterm[modelo] +1
cor                 = "r"
estilo              = "dashed"
apenasdeformada     = True
graficar_secao_deformada(arquivox, arquivoy,                
                             titulo,                            
                             xmin,xmax,                        
                             ymin,ymax,                         
                             ncoluna,                           
                             lblcoluna,                         
                             cor,tamanho,ordem,alpha,estilo,    
                             figura)


#%% DEFORMATION OF SECTION VP_CRE_CG_D1_16RE_3D
modelo      = 'VP_CRE_CG_D1_16RE_3D'
figura      = figura+1
arquivox    = modelo + '\convergencias_x.txt'
arquivoy    = modelo + '\convergencias_y.txt'
titulo      = modelo
escala      = 50
xmin        = -1.1
xmax        = 1.1
ymin        = -1.1
ymax        = 1.1
tamanho     = 2
ordem       = 1
alpha       = 1

lblcoluna           = 'CP'
ncoluna             = dicncolunafinalexcavation[modelo] +1
cor                 = "k"
estilo              = "-."
apenasdeformada     = False
graficar_secao_deformada(arquivox, arquivoy,                
                             titulo,                            
                             xmin,xmax,                        
                             ymin,ymax,                         
                             ncoluna,                           
                             lblcoluna,                         
                             cor,tamanho,ordem,alpha,estilo,    
                             figura)

lblcoluna           = 'LP'
ncoluna             = dicncolunalongterm[modelo]+1
cor                 = "r"
estilo              = "dashed"
apenasdeformada     = True
graficar_secao_deformada(arquivox, arquivoy,                
                             titulo,                            
                             xmin,xmax,                        
                             ymin,ymax,                         
                             ncoluna,                           
                             lblcoluna,                         
                             cor,tamanho,ordem,alpha,estilo,    
                             figura)


raio = 1-(0.719/100)*escala
num_pontos = 100
theta = np.linspace(0,2*np.pi,num_pontos)
x = raio*np.cos(theta)
y = raio*np.sin(theta)
plt.plot(x,y)

plt.savefig(str(titulo) + '.pdf')

#%% DEFORMATION OF SECTION VP_CRE_CG_D1_8RE_3D
modelo      = 'VP_CRE_CG_D1_8RE_3D'
figura      = figura+1
arquivox    = modelo + '\convergencias_x.txt'
arquivoy    = modelo + '\convergencias_y.txt'
titulo      = modelo
escala      = 50
xmin        = -1.1
xmax        = 1.1
ymin        = -1.1
ymax        = 1.1
tamanho     = 2
ordem       = 1
alpha       = 1

lblcoluna           = 'CP'
ncoluna             = dicncolunafinalexcavation[modelo] +1
cor                 = "k"
estilo              = "-."
apenasdeformada     = False
graficar_secao_deformada(arquivox, arquivoy,                
                             titulo,                            
                             xmin,xmax,                        
                             ymin,ymax,                         
                             ncoluna,                           
                             lblcoluna,                         
                             cor,tamanho,ordem,alpha,estilo,    
                             figura)

lblcoluna           = 'LP'
ncoluna             = dicncolunalongterm[modelo]+1
cor                 = "r"
estilo              = "dashed"
apenasdeformada     = True
graficar_secao_deformada(arquivox, arquivoy,                
                             titulo,                            
                             xmin,xmax,                        
                             ymin,ymax,                         
                             ncoluna,                           
                             lblcoluna,                         
                             cor,tamanho,ordem,alpha,estilo,    
                             figura)



#%% DEFORMATION OF SECTION VP_CRE_CG_D1_4RE_3D
modelo      = 'VP_CRE_CG_D1_4RE_3D'
figura      = figura+1
arquivox    = modelo + '\convergencias_x.txt'
arquivoy    = modelo + '\convergencias_y.txt'
titulo      = modelo
escala      = 50
xmin        = -1.1
xmax        = 1.1
ymin        = -1.1
ymax        = 1.1
tamanho     = 2
ordem       = 1
alpha       = 1

lblcoluna           = 'CP'
ncoluna             = dicncolunafinalexcavation[modelo] +1
cor                 = "k"
estilo              = "dashed"
apenasdeformada     = False
graficar_secao_deformada(arquivox, arquivoy,                
                             titulo,                            
                             xmin,xmax,                        
                             ymin,ymax,                         
                             ncoluna,                           
                             lblcoluna,                         
                             cor,tamanho,ordem,alpha,estilo,    
                             figura)

lblcoluna           = 'LP'
ncoluna             = dicncolunalongterm[modelo]+1
cor                 = "r"
estilo              = "dashed"
apenasdeformada     = True
graficar_secao_deformada(arquivox, arquivoy,                
                             titulo,                            
                             xmin,xmax,                        
                             ymin,ymax,                         
                             ncoluna,                           
                             lblcoluna,                         
                             cor,tamanho,ordem,alpha,estilo,    
                             figura)



raio = 1-(0.719/100)*escala
num_pontos = 100
theta = np.linspace(0,2*np.pi,num_pontos)
x = raio*np.cos(theta)
y = raio*np.sin(theta)
plt.plot(x,y, label = 'Tunel isolado - CP', color = 'g')

raio = 1-(0.7849/100)*escala
num_pontos = 100
theta = np.linspace(0,2*np.pi,num_pontos)
x = raio*np.cos(theta)
y = raio*np.sin(theta)
plt.plot(x,y, label = 'Tunel isolado - LP', color = 'orange')
plt.legend()

plt.savefig(str(titulo) + '.pdf')

#%% DEFORMATION OF SECTION EPVP_CRE_CG_D1_16RE_3D
modelo      = 'EPVP_CRE_CG_D1_16RE_3D'
figura      = figura+1
arquivox    = modelo + '\convergencias_x.txt'
arquivoy    = modelo + '\convergencias_y.txt'
titulo      = modelo
escala      = 50
xmin        = -1.1
xmax        = 1.1
ymin        = -1.1
ymax        = 1.1
tamanho     = 2
ordem       = 1
alpha       = 1

lblcoluna           = 'CP'
ncoluna             = dicncolunafinalexcavation[modelo] +1
cor                 = "k"
estilo              = "-."
apenasdeformada     = False
graficar_secao_deformada(arquivox, arquivoy,                
                             titulo,                            
                             xmin,xmax,                        
                             ymin,ymax,                         
                             ncoluna,                           
                             lblcoluna,                         
                             cor,tamanho,ordem,alpha,estilo,    
                             figura)

lblcoluna           = 'LP'
ncoluna             = dicncolunalongterm[modelo]+1
cor                 = "r"
estilo              = "dashed"
apenasdeformada     = True
graficar_secao_deformada(arquivox, arquivoy,                
                             titulo,                            
                             xmin,xmax,                        
                             ymin,ymax,                         
                             ncoluna,                           
                             lblcoluna,                         
                             cor,tamanho,ordem,alpha,estilo,    
                             figura)


#%% DEFORMATION OF SECTION EPVP_CRE_CG_D1_8RE_3D
modelo      = 'EPVP_CRE_CG_D1_8RE_3D'
figura      = figura+1
arquivox    = modelo + '\convergencias_x.txt'
arquivoy    = modelo + '\convergencias_y.txt'
titulo      = modelo
escala      = 50
xmin        = -1.1
xmax        = 1.1
ymin        = -1.1
ymax        = 1.1
tamanho     = 2
ordem       = 1
alpha       = 1

lblcoluna           = 'CP'
ncoluna             = dicncolunafinalexcavation[modelo] +1
cor                 = "k"
estilo              = "-."
apenasdeformada     = False
graficar_secao_deformada(arquivox, arquivoy,                
                             titulo,                            
                             xmin,xmax,                        
                             ymin,ymax,                         
                             ncoluna,                           
                             lblcoluna,                         
                             cor,tamanho,ordem,alpha,estilo,    
                             figura)

lblcoluna           = 'LP'
ncoluna             = dicncolunalongterm[modelo]+1
cor                 = "r"
estilo              = "dashed"
apenasdeformada     = True
graficar_secao_deformada(arquivox, arquivoy,                
                             titulo,                            
                             xmin,xmax,                        
                             ymin,ymax,                         
                             ncoluna,                           
                             lblcoluna,                         
                             cor,tamanho,ordem,alpha,estilo,    
                             figura)



#%% DEFORMATION OF SECTION EPVP_CRE_CG_D1_4RE_3D
modelo      = 'EPVP_CRE_CG_D1_4RE_3D'
figura      = figura+1
arquivox    = modelo + '\convergencias_x.txt'
arquivoy    = modelo + '\convergencias_y.txt'
titulo      = modelo
escala      = 50
xmin        = -1.1
xmax        = 1.1
ymin        = -1.1
ymax        = 1.1
tamanho     = 2
ordem       = 1
alpha       = 1

lblcoluna           = 'CP'
ncoluna             = dicncolunafinalexcavation[modelo] +1
cor                 = "k"
estilo              = "-."
apenasdeformada     = False
graficar_secao_deformada(arquivox, arquivoy,                
                             titulo,                            
                             xmin,xmax,                        
                             ymin,ymax,                         
                             ncoluna,                           
                             lblcoluna,                         
                             cor,tamanho,ordem,alpha,estilo,    
                             figura)

lblcoluna           = 'LP'
ncoluna             = dicncolunalongterm[modelo]+1
cor                 = "r"
estilo              = "dashed"
apenasdeformada     = True
graficar_secao_deformada(arquivox, arquivoy,                
                             titulo,                            
                             xmin,xmax,                        
                             ymin,ymax,                         
                             ncoluna,                           
                             lblcoluna,                         
                             cor,tamanho,ordem,alpha,estilo,    
                             figura)

raio = 1-(0.9204/100)*escala
num_pontos = 100
theta = np.linspace(0,2*np.pi,num_pontos)
x = raio*np.cos(theta)
y = raio*np.sin(theta)
plt.plot(x,y, label = 'Tunel isolado - CP', color = 'g')

raio = 1-(0.9735/100)*escala
num_pontos = 100
theta = np.linspace(0,2*np.pi,num_pontos)
x = raio*np.cos(theta)
y = raio*np.sin(theta)
plt.plot(x,y, label = 'Tunel isolado - LP', color = 'orange')
plt.legend()

plt.savefig(str(titulo) + '.pdf')

#%% DEFORMATION OF SECTION EPVP_CRVE_CG_D1_16RE_3D
modelo      = 'EPVP_CRVE_CG_D1_16RE_3D'
figura      = figura+1
arquivox    = modelo + '\convergencias_x.txt'
arquivoy    = modelo + '\convergencias_y.txt'
titulo      = modelo
escala      = 50
xmin        = -1.1
xmax        = 1.1
ymin        = -1.1
ymax        = 1.1
tamanho     = 2
ordem       = 1
alpha       = 1

lblcoluna           = 'CP'
ncoluna             = dicncolunafinalexcavation[modelo] +1
cor                 = "k"
estilo              = "-."
apenasdeformada     = False
graficar_secao_deformada(arquivox, arquivoy,                
                             titulo,                            
                             xmin,xmax,                        
                             ymin,ymax,                         
                             ncoluna,                           
                             lblcoluna,                         
                             cor,tamanho,ordem,alpha,estilo,    
                             figura)

lblcoluna           = 'LP'
ncoluna             = dicncolunalongterm[modelo]+1
cor                 = "r"
estilo              = "dashed"
apenasdeformada     = True
graficar_secao_deformada(arquivox, arquivoy,                
                             titulo,                            
                             xmin,xmax,                        
                             ymin,ymax,                         
                             ncoluna,                           
                             lblcoluna,                         
                             cor,tamanho,ordem,alpha,estilo,    
                             figura)

#%% DEFORMATION OF SECTION EPVP_CRVE_CG_D1_4RE_3D
modelo      = 'EPVP_CRVE_CG_D1_4RE_3D'
figura      = figura+1
arquivox    = modelo + '\convergencias_x.txt'
arquivoy    = modelo + '\convergencias_y.txt'
titulo      = modelo
escala      = 50
xmin        = -1.1
xmax        = 1.1
ymin        = -1.1
ymax        = 1.1
tamanho     = 2
ordem       = 1
alpha       = 1

lblcoluna           = 'CP'
ncoluna             = dicncolunafinalexcavation[modelo] +1
cor                 = "k"
estilo              = "-."
apenasdeformada     = False
graficar_secao_deformada(arquivox, arquivoy,                
                             titulo,                            
                             xmin,xmax,                        
                             ymin,ymax,                         
                             ncoluna,                           
                             lblcoluna,                         
                             cor,tamanho,ordem,alpha,estilo,    
                             figura)

lblcoluna           = 'LP'
ncoluna             = dicncolunalongterm[modelo]+1
cor                 = "r"
estilo              = "dashed"
apenasdeformada     = True
graficar_secao_deformada(arquivox, arquivoy,                
                             titulo,                            
                             xmin,xmax,                        
                             ymin,ymax,                         
                             ncoluna,                           
                             lblcoluna,                         
                             cor,tamanho,ordem,alpha,estilo,    
                             figura)


raio = 1-(0.9696/100)*escala
num_pontos = 100
theta = np.linspace(0,2*np.pi,num_pontos)
x = raio*np.cos(theta)
y = raio*np.sin(theta)
plt.plot(x,y, label = 'Tunel isolado - CP', color = 'g')

raio = 1-(1.1907/100)*escala
num_pontos = 100
theta = np.linspace(0,2*np.pi,num_pontos)
x = raio*np.cos(theta)
y = raio*np.sin(theta)
plt.plot(x,y, label = 'Tunel isolado - LP', color = 'orange')
plt.legend()

plt.savefig(str(titulo) + '.pdf')