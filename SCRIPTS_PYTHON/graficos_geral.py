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
from scipy.signal import savgol_filter
#
#
def graficar(arquivo,                   # nome do arquivo de leitura
             titulo,                    # titulo do gráfico
             eixox,eixoy,               # nome dos eixos x e y
             xmin,xmax,                 # intervalo eixo x
             ymin,ymax,                 # intervalo eixo y
             ncoluna,                   # numero da coluna (dados em y)
             lblcoluna,                 # legenda da coluna
             cor,tamanho,ordem,alpha,   # formatacao
             invertx,                   # inverter eixo x
             suavizar,filterx1,filterx2,wl,poly, # parametros do filtro de suavização
             figura):
    
    # Lendo arquivo de dados      
    data = pd.read_csv(arquivo,delim_whitespace= True).values

    # Definindo as dimensões do layout da figura
    plt.figure(figura,figsize = (9,5))

    # Eixo x
    x0          = 80*1/3
    if invertx == True:
        x = -(data[:,1]-max(data[:,1]))
    elif invertx == False:
        x =  data[:,1]
    #x = data[:,1]

    # dados do eixo y
    y = data[:,ncoluna]
    #y = savgol_filter(data[:,ncoluna],20,10)
    
    if suavizar == True:
        for i in range(1,3):
            y[filterx1:filterx2] = savgol_filter(data[filterx1:filterx2,ncoluna],wl,poly, mode = 'interp')
        
    # Plotando os dados
    plt.plot(x,y,color = cor,zorder = ordem, lw = tamanho, alpha = alpha, label = lblcoluna)

    # Formatando os eixos
    #plt.axvline(x0,color = 'k', label = lblx0, linestyle = '--')
    plt.ylim([ymin, ymax])
    plt.xlim([xmin, xmax])
    plt.ylabel(eixoy)
    plt.xlabel(eixox)
    plt.legend()
    plt.grid(True) 
    plt.title(titulo, fontsize = 16) 
    #plt.autoscale(axis='y')
    
    # Formatando a legenda
    plt.legend(
        loc = 'center',
        shadow=False,
        framealpha = 0.8,
        ncol = 4,
        columnspacing = 0.5,
        bbox_to_anchor=(0.5, -0.2))
    
    # Salvando em arquivo    
    plt.savefig('profile'+ str(figura) + '.pdf')

# Formatação do gráfico
titulo      = 'Convergence Profiles'
eixox       = r'$y/R_e$'  
eixoy       = r'$U=-u(R_e,\theta = 90^\circ)/R_{e}$ [\%]'
ymin        = 0
ymax        = 1.5
xmin        = 5
xmax        = 35
invertx     = True
suavizar    = True

# parametros para o filtro de suavização
filterx1    = 35
filterx2    = 90
wl          = 30
poly        = 10


figura      = 1
arquivo     = 'EP_CRE_CG_D1_4RE_3D.txt'
ncoluna     = 81
lblcoluna   = 'EP_CRE - $d_1 = 4R_e$'
cor         = 'b'
tamanho     = 3
ordem       = 1
alpha       = 1
graficar(arquivo,titulo,eixox,eixoy,
         xmin,xmax,ymin,ymax,
         ncoluna,lblcoluna,
         cor,tamanho,ordem,alpha,
         invertx,
         suavizar,filterx1,filterx2,wl,poly,
         figura)

figura      = 1
arquivo     = 'EPVP_CRVE_CG_D1_4RE_3D.txt'
ncoluna     = 111
lblcoluna   = 'EPVP_CRVE - $d_1 = 4R_e$'
cor         = 'pink'
tamanho     = 3
ordem       = 1
alpha       = 1
graficar(arquivo,titulo,eixox,eixoy,
         xmin,xmax,ymin,ymax,
         ncoluna,lblcoluna,
         cor,tamanho,ordem,alpha,
         invertx,
         suavizar,filterx1,filterx2,wl,poly,
         figura)

figura      = 1
arquivo     = 'EP_CRE_CG_D1_8RE_3D.txt'
ncoluna     = 90
lblcoluna   = 'EP_CRE - $d_1 = 8R_e$'
cor         = 'g'
tamanho     = 3
ordem       = 1
alpha       = 1
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,
          invertx,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

figura      = 1
arquivo     = 'EP_CRE_CG_D1_16RE_3D.txt'
ncoluna     = 107
lblcoluna   = 'EP_CRE - $d_1 = 16R_e$'
cor         = 'r'
tamanho     = 3
ordem       = 1
alpha       = 1
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,
          invertx,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

figura      = 1
arquivo     = 'EP-CRE-SG-D1-INF-AXI.txt'
ncoluna     = 79
lblcoluna   = 'EP_CRE - AXI'
cor         = 'gray'
tamanho     = 3
ordem       = 1
alpha       = 1
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,
          invertx,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

# Colocar uma linha vertical
x0          = 80*1/3
lblx0       = 'Face'
plt.axvline(x0,color = 'k', label = lblx0, linestyle = '--')


#GALERIA


# Formatação do gráfico
titulo      = 'Gallery Convergence Profiles'
eixox       = r'$y/R_{e1}$'  
eixoy       = r'$U{1}=-u{1}(R_{e1},\theta = 90^\circ)/R_{e1}$ [%]'
ymin        = 0.75
ymax        = 1.9
xmin        = 0
xmax        = 12
invertx     = False

# parametros para o filtro de suavização
filterx1    = 0
filterx2    = 80
wl          = 20
poly        = 6


figura      = 2
arquivo     = 'EPVP_CRVE_CG_D1_16RE_3D_GALERIA.txt'
ncoluna     = 79
lblcoluna   = 'EPVP_CRVE - $d_1 = 16R_e$'
cor         = 'r'
tamanho     = 3
ordem       = 1
alpha       = 1
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,
          invertx,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

figura      = 2
arquivo     = 'EPVP_CRVE_CG_D1_8RE_3D_GALERIA.txt'
ncoluna     = 79
lblcoluna   = 'EPVP_CRVE - $d_1 = 8R_e$'
cor         = 'green'
tamanho     = 3
ordem       = 1
alpha       = 1
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,
          invertx,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

# parametros para o filtro de suavização
filterx1    = 0
filterx2    = 80
wl          = 10
poly        = 6

figura      = 2
arquivo     = 'EPVP_CRVE_CG_D1_4RE_3D_GALERIA.txt'
ncoluna     = 79
lblcoluna   = 'EPVP_CRVE - $d_1 = 4R_e$'
cor         = 'b'
tamanho     = 3
ordem       = 1
alpha       = 1
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,
          invertx,
          suavizar,filterx1,filterx2,wl,poly,
          figura)