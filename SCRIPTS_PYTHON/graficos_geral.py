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
             cor,tamanho,ordem,alpha,estilo,   # formatacao
             invertx,                   # inverter eixo x
             inserirx0,x0,              # adicionar linha pontilhada vertical
             suavizar,filterx1,filterx2,wl,poly, # parametros do filtro de suavização
             figura):
    
    # Lendo arquivo de dados      
    data = pd.read_csv(arquivo,delim_whitespace= True).values

    # Definindo as dimensões do layout da figura
    plt.figure(figura,figsize = (9,5))

    # Eixo x
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
    plt.plot(x,y,color = cor,
             zorder = ordem, 
             linestyle=estilo, 
             lw = tamanho, 
             alpha = alpha, 
             label = lblcoluna)

    # Formatando os eixos
    #plt.axvline(x0,color = 'k', label = lblx0, linestyle = '--')
    plt.ylim([ymin, ymax])
    plt.xlim([xmin, xmax])
    plt.ylabel(eixoy)
    plt.xlabel(eixox)
    plt.legend()
    
    # Formatando grades
    plt.rcParams['axes.axisbelow'] = True 
    plt.grid(True,which = 'major')
    plt.grid(True,which = 'minor', alpha = 0.3)
    plt.minorticks_on()
    
    # Inserir linha vertical em x0
    if inserirx0 == True:
        plt.axvline(x0,color = 'k', linestyle = '--')
    
    # adicionando título
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
    plt.savefig(str(titulo) + '.pdf')


""" ********************************************
CONVERGENCE PROFILES - MODEL EP_CRE
******************************************** """ 

# Formatação do gráfico
figura      = 1
titulo      = 'Convergence Profiles - EP_CRE'
eixox       = r'$y/R_e$'  
eixoy       = r'$U=-u(R_e,\theta = 90^\circ)/R_{e}$ [\%]'
ymin        = 0
ymax        = 1.5
xmin        = 5
xmax        = 35
invertx     = True
inserirx0   = True
x0          = 80*1/3
suavizar    = True

# parametros para o filtro de suavização
filterx1    = 35
filterx2    = 90
wl          = 30
poly        = 10


arquivo     = 'EP-CRE-SG-D1-INF-AXI\convergencias.txt'
ncoluna     = 79
lblcoluna   = '$d_1 = \infty$ and without gallery'
cor         = 'b'
tamanho     = 1.5
ordem       = 4
alpha       = 1
estilo      = 'dashed'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EP_CRE_CG_D1_16RE_3D\convergencias_90.txt'
ncoluna     = 107
lblcoluna   = '$d_1 = 16R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.3
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EP_CRE_CG_D1_8RE_3D\convergencias_90.txt'
ncoluna     = 90
lblcoluna   = ' $d_1 = 8R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 2
alpha       = 0.6
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EP_CRE_CG_D1_4RE_3D\convergencias_90.txt'
ncoluna     = 81
lblcoluna   = '$d_1 = 4R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 1
alpha       = 1
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

""" ********************************************
CONVERGENCE PROFILES - LONG-TERM - MODEL VP_CRE
******************************************** """ 

# Formatação do gráfico
figura      = 2
titulo      = 'Convergence Profiles - Long-term - VP_CRE'
eixox       = r'$y/R_e$'  
eixoy       = r'$U=-u(R_e,\theta = 90^\circ)/R_{e}$ [\%]'
ymin        = 0
ymax        = 1.5
xmin        = 5
xmax        = 35
invertx     = True
inserirx0   = True
x0          = 80*1/3
suavizar    = True

# parametros para o filtro de suavização
filterx1    = 35
filterx2    = 90
wl          = 30
poly        = 10

arquivo     = 'VP_CRE_SG_D1_INF_AXI\convergencias.txt'
ncoluna     = 109
lblcoluna   = '$d_1 = \infty$ without gallery'
cor         = 'b'
tamanho     = 1.5
ordem       = 4
alpha       = 1
estilo      = 'dashed'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'VP_CRE_CG_D1_4RE_3D\convergencias_90.txt'
ncoluna     = 111
lblcoluna   = '$d_1 = 4R_e$'
cor         = 'r'
tamanho     = 1.5
ordem       = 4
alpha       = 1
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'VP_CRE_CG_D1_8RE_3D\convergencias_90.txt'
ncoluna     = 120
lblcoluna   = '$d_1 = 8R_e$'
cor         = 'r'
tamanho     = 1.5
ordem       = 4
alpha       = 0.6
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

""" ********************************************
CONVERGENCE PROFILES - FINAL EXCAVATION - MODEL VP_CRE
******************************************** """ 

# Formatação do gráfico
figura      = 3
titulo      = 'Convergence Profiles - Final excavation - VP_CRE'
eixox       = r'$y/R_e$'  
eixoy       = r'$U=-u(R_e,\theta = 90^\circ)/R_{e}$ [\%]'
ymin        = 0
ymax        = 1.5
xmin        = 5
xmax        = 35
invertx     = True
inserirx0   = True
x0          = 80*1/3
suavizar    = True

# parametros para o filtro de suavização
filterx1    = 35
filterx2    = 90
wl          = 30
poly        = 10

arquivo     = 'VP_CRE_SG_D1_INF_AXI\convergencias.txt'
ncoluna     = 79
lblcoluna   = '$d_1 = \infty$ without gallery'
cor         = 'b'
tamanho     = 1.5
ordem       = 4
alpha       = 1
estilo      = 'dashed'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'VP_CRE_CG_D1_4RE_3D\convergencias_90.txt'
ncoluna     = 81
lblcoluna   = '$d_1 = 4R_e$'
cor         = 'r'
tamanho     = 1.5
ordem       = 4
alpha       = 1
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'VP_CRE_CG_D1_8RE_3D\convergencias_90.txt'
ncoluna     = 90
lblcoluna   = '$d_1 = 8R_e$'
cor         = 'r'
tamanho     = 1.5
ordem       = 4
alpha       = 0.6
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

""" ********************************************
CONVERGENCE PROFILES - LONG-TERM - EPVP_CRE
******************************************** """ 

# Formatação do gráfico
figura      = 4
titulo      = 'Convergence Profiles - Long-term - EPVP_CRE'
eixox       = r'$y/R_e$'  
eixoy       = r'$U=-u(R_e,\theta = 90^\circ)/R_{e}$ [\%]'
ymin        = 0
ymax        = 1.5
xmin        = 5
xmax        = 35
invertx     = True
inserirx0   = True
x0          = 80*1/3
suavizar    = True

# parametros para o filtro de suavização
filterx1    = 35
filterx2    = 90
wl          = 30
poly        = 10


arquivo     = 'EPVP-CRE-SG-D1-INF-AXI\convergencias.txt'
ncoluna     = 109
lblcoluna   = '$d_1 = \infty$ and without gallery'
cor         = 'b'
tamanho     = 1.5
ordem       = 4
alpha       = 1
estilo      = 'dashed'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRE_CG_D1_16RE_3D\convergencias_90.txt'
ncoluna     = 137
lblcoluna   = '$d_1 = 16R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.3
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRE_CG_D1_8RE_3D\convergencias_90.txt'
ncoluna     = 120
lblcoluna   = ' $d_1 = 8R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 2
alpha       = 0.6
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRE_CG_D1_4RE_3D\convergencias_90.txt'
ncoluna     = 111
lblcoluna   = '$d_1 = 4R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 1
alpha       = 1
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

""" ********************************************
CONVERGENCE PROFILES - FINAL-EXCAVATION - EPVP_CRE
******************************************** """ 

# Formatação do gráfico
figura      = 5
titulo      = 'Convergence Profiles - Final Excavation - EPVP_CRE'
eixox       = r'$y/R_e$'  
eixoy       = r'$U=-u(R_e,\theta = 90^\circ)/R_{e}$ [\%]'
ymin        = 0
ymax        = 1.5
xmin        = 5
xmax        = 35
invertx     = True
inserirx0   = True
x0          = 80*1/3
suavizar    = True

# parametros para o filtro de suavização
filterx1    = 35
filterx2    = 90
wl          = 30
poly        = 10


arquivo     = 'EPVP-CRE-SG-D1-INF-AXI\convergencias.txt'
ncoluna     = 79
lblcoluna   = '$d_1 = \infty$ and without gallery'
cor         = 'b'
tamanho     = 1.5
ordem       = 4
alpha       = 1
estilo      = 'dashed'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRE_CG_D1_16RE_3D\convergencias_90.txt'
ncoluna     = 107
lblcoluna   = '$d_1 = 16R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.3
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRE_CG_D1_8RE_3D\convergencias_90.txt'
ncoluna     = 91
lblcoluna   = ' $d_1 = 8R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 2
alpha       = 0.6
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRE_CG_D1_4RE_3D\convergencias_90.txt'
ncoluna     = 81
lblcoluna   = '$d_1 = 4R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 1
alpha       = 1
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

""" ********************************************
CONVERGENCE PROFILES - LONG-TERM - EPVP_CRVE
******************************************** """ 

# Formatação do gráfico
figura      = 6
titulo      = 'Convergence Profiles - Long-term - EPVP_CRVE'
eixox       = r'$y/R_e$'  
eixoy       = r'$U=-u(R_e,\theta = 90^\circ)/R_{e}$ [\%]'
ymin        = 0
ymax        = 1.5
xmin        = 5
xmax        = 35
invertx     = True
inserirx0   = True
x0          = 80*1/3
suavizar    = True

# parametros para o filtro de suavização
filterx1    = 35
filterx2    = 90
wl          = 30
poly        = 10


arquivo     = 'EPVP-CRVE-SG-D1-INF-AXI\convergencias.txt'
ncoluna     = 109
lblcoluna   = '$d_1 = \infty$ and without gallery'
cor         = 'b'
tamanho     = 1.5
ordem       = 4
alpha       = 1
estilo      = 'dashed'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRVE_CG_D1_16RE_3D\convergencias_90.txt'
ncoluna     = 137
lblcoluna   = '$d_1 = 16R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.3
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRVE_CG_D1_8RE_3D\convergencias_90.txt'
ncoluna     = 120
lblcoluna   = ' $d_1 = 8R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 2
alpha       = 0.6
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRVE_CG_D1_4RE_3D\convergencias_90.txt'
ncoluna     = 111
lblcoluna   = '$d_1 = 4R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 1
alpha       = 1
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

""" ********************************************
CONVERGENCE PROFILES - LONG-TERM - EPVP_CRVE
******************************************** """ 

# Formatação do gráfico
figura      = 7
titulo      = 'Convergence Profiles - Final excavation - EPVP_CRVE'
eixox       = r'$y/R_e$'  
eixoy       = r'$U=-u(R_e,\theta = 90^\circ)/R_{e}$ [\%]'
ymin        = 0
ymax        = 1.5
xmin        = 5
xmax        = 35
invertx     = True
inserirx0   = True
x0          = 80*1/3
suavizar    = True

# parametros para o filtro de suavização
filterx1    = 35
filterx2    = 90
wl          = 30
poly        = 10


arquivo     = 'EPVP-CRVE-SG-D1-INF-AXI\convergencias.txt'
ncoluna     = 79
lblcoluna   = '$d_1 = \infty$ and without gallery'
cor         = 'b'
tamanho     = 1.5
ordem       = 4
alpha       = 1
estilo      = 'dashed'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRVE_CG_D1_16RE_3D\convergencias_90.txt'
ncoluna     = 108
lblcoluna   = '$d_1 = 16R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.3
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRVE_CG_D1_8RE_3D\convergencias_90.txt'
ncoluna     = 91
lblcoluna   = ' $d_1 = 8R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 2
alpha       = 0.6
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRVE_CG_D1_4RE_3D\convergencias_90.txt'
ncoluna     = 82
lblcoluna   = '$d_1 = 4R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 1
alpha       = 1
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)


""" ********************************************
CONVERGENCE PROFILES - LONG-TERM - D1=16Re
******************************************** """ 

# Formatação do gráfico
figura      = 8
titulo      = 'Convergence Profiles - Long-term - $d_1=16R_e$'
eixox       = r'$y/R_e$'  
eixoy       = r'$U=-u(R_e,\theta = 90^\circ)/R_{e}$ [\%]'
ymin        = 0
ymax        = 1.5
xmin        = 5
xmax        = 35
invertx     = True
inserirx0   = True
x0          = 80*1/3
suavizar    = True

# parametros para o filtro de suavização
filterx1    = 35
filterx2    = 90
wl          = 30
poly        = 10


arquivo     = 'EP_CRE_CG_D1_16RE_3D\convergencias_90.txt'
ncoluna     = 107
lblcoluna   = 'EP_CRE'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.3
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRE_CG_D1_16RE_3D\convergencias_90.txt'
ncoluna     = 137
lblcoluna   = 'EPVP_CRE'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.6
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRVE_CG_D1_16RE_3D\convergencias_90.txt'
ncoluna     = 137
lblcoluna   = 'EPVP_CRVE'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.9
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)


""" ********************************************
CONVERGENCE PROFILES - LONG-TERM - D1=8Re
******************************************** """ 

# Formatação do gráfico
figura      = 9
titulo      = 'Convergence Profiles - Long-term - $d_1=8R_e$'
eixox       = r'$y/R_e$'  
eixoy       = r'$U=-u(R_e,\theta = 90^\circ)/R_{e}$ [\%]'
ymin        = 0
ymax        = 1.5
xmin        = 5
xmax        = 35
invertx     = True
inserirx0   = True
x0          = 80*1/3
suavizar    = True

# parametros para o filtro de suavização
filterx1    = 35
filterx2    = 90
wl          = 30
poly        = 10


arquivo     = 'EP_CRE_CG_D1_8RE_3D\convergencias_90.txt'
ncoluna     = 90
lblcoluna   = 'EP_CRE'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.3
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRE_CG_D1_8RE_3D\convergencias_90.txt'
ncoluna     = 120
lblcoluna   = 'EPVP_CRE'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.6
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRVE_CG_D1_8RE_3D\convergencias_90.txt'
ncoluna     = 120
lblcoluna   = 'EPVP_CRVE'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.9
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

""" ********************************************
CONVERGENCE PROFILES - LONG-TERM - D1=4Re
******************************************** """ 

# Formatação do gráfico
figura      = 10
titulo      = 'Convergence Profiles - Long-term - $d_1=4R_e$'
eixox       = r'$y/R_e$'  
eixoy       = r'$U=-u(R_e,\theta = 90^\circ)/R_{e}$ [\%]'
ymin        = 0
ymax        = 1.5
xmin        = 5
xmax        = 35
invertx     = True
inserirx0   = True
x0          = 80*1/3
suavizar    = True

# parametros para o filtro de suavização
filterx1    = 35
filterx2    = 90
wl          = 30
poly        = 10


arquivo     = 'EP_CRE_CG_D1_4RE_3D\convergencias_90.txt'
ncoluna     = 81
lblcoluna   = 'EP_CRE'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.3
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRE_CG_D1_4RE_3D\convergencias_90.txt'
ncoluna     = 111
lblcoluna   = 'EPVP_CRE'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.6
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRVE_CG_D1_4RE_3D\convergencias_90.txt'
ncoluna     = 111
lblcoluna   = 'EPVP_CRVE'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.9
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

""" ********************************************
GALLERY CONVERGENCE PROFILES - LONG-TERM - D1=16Re
******************************************** """ 

# Formatação do gráfico
figura      = 11
titulo      = 'Gallery Convergence Profiles - Long-term - $d_1 = 16R_e$'
eixox       = r'$y/R_{e1}$'  
eixoy       = r'$U{1}=-u{1}(R_{e1},\theta = 90^\circ)/R_{e1}$ [%]'
ymin        = 0
ymax        = 2
xmin        = 0
xmax        = 12
invertx     = False
inserirx0   = False
x0          = 0
suavizar    = True

# parametros para o filtro de suavização
filterx1    = 0
filterx2    = 80
wl          = 30
poly        = 10

arquivo     = 'EP_CRE_SG_D1_16RE_3D\convergencias1_90.txt'
ncoluna     = 79
lblcoluna   = 'EP_CRE - without gallery'
cor         = 'blue'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'dashed'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EP_CRE_CG_D1_16RE_3D\convergencias1_90.txt'
ncoluna     = 107
lblcoluna   = 'EP_CRE'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.3
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRE_CG_D1_16RE_3D\convergencias1_90.txt'
ncoluna     = 137
lblcoluna   = 'EPVP_CRE'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.6
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRVE_CG_D1_16RE_3D\convergencias1_90.txt'
ncoluna     = 137
lblcoluna   = 'EPVP_CRVE'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.9
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)


""" ********************************************
GALLERY CONVERGENCE PROFILES - LONG-TERM - D1=8Re
******************************************** """ 

# Formatação do gráfico
figura      = 12
titulo      = 'Gallery Convergence Profiles - Long-term - $d_1 = 8R_e$'
eixox       = r'$y/R_{e1}$'  
eixoy       = r'$U{1}=-u{1}(R_{e1},\theta = 90^\circ)/R_{e1}$ [%]'
ymin        = 0
ymax        = 2
xmin        = 0
xmax        = 12
invertx     = False
inserirx0   = False
x0          = 0
suavizar    = True

# parametros para o filtro de suavização
filterx1    = 0
filterx2    = 80
wl          = 20
poly        = 5

arquivo     = 'EP_CRE_SG_D1_8RE_3D\convergencias1_90.txt'
ncoluna     = 79
lblcoluna   = 'EP_CRE - without gallery'
cor         = 'blue'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'dashed'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EP_CRE_CG_D1_8RE_3D\convergencias1_90.txt'
ncoluna     = 90
lblcoluna   = 'EP_CRE'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.3
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRE_CG_D1_8RE_3D\convergencias1_90.txt'
ncoluna     = 120
lblcoluna   = 'EPVP_CRE'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.6
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRVE_CG_D1_8RE_3D\convergencias1_90.txt'
ncoluna     = 120
lblcoluna   = 'EPVP_CRVE'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.9
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)


""" ********************************************
GALLERY CONVERGENCE PROFILES - LONG-TERM - D1=4Re
******************************************** """ 

# Formatação do gráfico
figura      = 13
titulo      = 'Gallery Convergence Profiles - Long-term - $d_1 = 4R_e$'
eixox       = r'$y/R_{e1}$'  
eixoy       = r'$U{1}=-u{1}(R_{e1},\theta = 90^\circ)/R_{e1}$ [%]'
ymin        = 0
ymax        = 2
xmin        = 0
xmax        = 12
invertx     = False
inserirx0   = False
x0          = 0
suavizar    = True

# parametros para o filtro de suavização
filterx1    = 0
filterx2    = 80
wl          = 10
poly        = 6

arquivo     = 'EP_CRE_SG_D1_4RE_3D\convergencias1_90.txt'
ncoluna     = 79
lblcoluna   = 'EP_CRE - without gallery'
cor         = 'blue'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'dashed'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EP_CRE_CG_D1_4RE_3D\convergencias1_90.txt'
ncoluna     = 81
lblcoluna   = 'EP_CRE'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.3
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRE_CG_D1_4RE_3D\convergencias1_90.txt'
ncoluna     = 111
lblcoluna   = 'EPVP_CRE'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.6
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRVE_CG_D1_4RE_3D\convergencias1_90.txt'
ncoluna     = 111
lblcoluna   = 'EPVP_CRVE'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.9
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)



""" ********************************************
GALLERY CONVERGENCE PROFILES EP-CRE
******************************************** """ 

# Formatação do gráfico
figura      = 14
titulo      = 'Gallery Convergence Profiles EP_CRE'
eixox       = r'$y/R_{e1}$'  
eixoy       = r'$U{1}=-u{1}(R_{e1},\theta = 90^\circ)/R_{e1}$ [%]'
ymin        = 0.75
ymax        = 2
xmin        = 0
xmax        = 12
invertx     = False
inserirx0   = False
x0          = 0
suavizar    = True

# parametros para o filtro de suavização
filterx1    = 0
filterx2    = 80
wl          = 10
poly        = 6

arquivo     = 'EP_CRE_CG_D1_4RE_3D\convergencias1_90.txt'
ncoluna     = 81
lblcoluna   = '$d_1 = 4R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.3
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

# parametros para o filtro de suavização
filterx1    = 0
filterx2    = 80
wl          = 20
poly        = 5

arquivo     = 'EP_CRE_CG_D1_8RE_3D\convergencias1_90.txt'
ncoluna     = 90
lblcoluna   = '$d_1 = 8R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.6
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EP_CRE_CG_D1_16RE_3D\convergencias1_90.txt'
ncoluna     = 107
lblcoluna   = '$d_1 = 16R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.9
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)



""" ********************************************
GALLERY CONVERGENCE PROFILES - LONG-TERM - EPVP-CRE
******************************************** """ 

# Formatação do gráfico
figura      = 15
titulo      = 'Gallery Convergence Profiles - Long-term - EPVP_CRE'
eixox       = r'$y/R_{e1}$'  
eixoy       = r'$U{1}=-u{1}(R_{e1},\theta = 90^\circ)/R_{e1}$ [%]'
ymin        = 0.75
ymax        = 2
xmin        = 0
xmax        = 12
invertx     = False
inserirx0   = False
x0          = 0
suavizar    = True

# parametros para o filtro de suavização
filterx1    = 0
filterx2    = 80
wl          = 10
poly        = 6

arquivo     = 'EPVP_CRE_CG_D1_4RE_3D\convergencias1_90.txt'
ncoluna     = 111
lblcoluna   = '$d_1 = 4R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.3
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

# parametros para o filtro de suavização
filterx1    = 0
filterx2    = 80
wl          = 20
poly        = 5

arquivo     = 'EPVP_CRE_CG_D1_8RE_3D\convergencias1_90.txt'
ncoluna     = 120
lblcoluna   = '$d_1 = 8R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.6
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRE_CG_D1_16RE_3D\convergencias1_90.txt'
ncoluna     = 137
lblcoluna   = '$d_1 = 16R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.9
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

""" ********************************************
GALLERY CONVERGENCE PROFILES - LONG-TERM - EPVP-CRVE
******************************************** """ 

# Formatação do gráfico
figura      = 16
titulo      = 'Gallery Convergence Profiles - Long-term - EPVP_CRVE'
eixox       = r'$y/R_{e1}$'  
eixoy       = r'$U{1}=-u{1}(R_{e1},\theta = 90^\circ)/R_{e1}$ [%]'
ymin        = 0.75
ymax        = 2
xmin        = 0
xmax        = 12
invertx     = False
inserirx0   = False
x0          = 0
suavizar    = True

# parametros para o filtro de suavização
filterx1    = 0
filterx2    = 80
wl          = 10
poly        = 6

arquivo     = 'EPVP_CRVE_CG_D1_4RE_3D\convergencias1_90.txt'
ncoluna     = 111
lblcoluna   = '$d_1 = 4R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.3
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

# parametros para o filtro de suavização
filterx1    = 0
filterx2    = 80
wl          = 20
poly        = 5

arquivo     = 'EPVP_CRVE_CG_D1_8RE_3D\convergencias1_90.txt'
ncoluna     = 120
lblcoluna   = '$d_1 = 8R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.6
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRVE_CG_D1_16RE_3D\convergencias1_90.txt'
ncoluna     = 137
lblcoluna   = '$d_1 = 16R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.9
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)




""" ********************************************
PRESSURE PROFILES - EP_CRE
******************************************** """ 

# Formatação do gráfico
figura      = 17
titulo      = 'Pressure Profiles - EP_CRE'
eixox       = r'$y/R_e$'  
eixoy       = r'$p=p(R_e,\theta = 90^\circ)$ [MPa]'
ymin        = -15
ymax        = 1
xmin        = 5
xmax        = 35
invertx     = True
inserirx0   = True
x0          = 80*1/3
suavizar    = True

# parametros para o filtro de suavização
filterx1    = 35
filterx2    = 90
wl          = 40
poly        = 2


arquivo     = 'EP-CRE-SG-D1-INF-AXI\pressure.txt'
ncoluna     = 79
lblcoluna   = '$d_1 = \infty$ and without gallery'
cor         = 'b'
tamanho     = 1.5
ordem       = 4
alpha       = 1
estilo      = 'dashed'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EP_CRE_CG_D1_16RE_3D\pressure_90.txt'
ncoluna     = 107
lblcoluna   = '$d_1 = 16R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.3
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EP_CRE_CG_D1_8RE_3D\pressure_90.txt'
ncoluna     = 90
lblcoluna   = ' $d_1 = 8R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 2
alpha       = 0.6
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EP_CRE_CG_D1_4RE_3D\pressure_90.txt'
ncoluna     = 81
lblcoluna   = '$d_1 = 4R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 1
alpha       = 1
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

""" ********************************************
PRESSURE PROFILES - LONG-TERM - EPVP_CRE
******************************************** """ 

# Formatação do gráfico
figura      = 18
titulo      = 'Pressure Profiles - Long-term - EPVP_CRE'
eixox       = r'$y/R_e$'  
eixoy       = r'$p=p(R_e,\theta = 90^\circ)$ [MPa]'
ymin        = -15
ymax        = 1
xmin        = 5
xmax        = 35
invertx     = True
inserirx0   = True
x0          = 80*1/3
suavizar    = True

# parametros para o filtro de suavização
filterx1    = 35
filterx2    = 90
wl          = 30
poly        = 2


arquivo     = 'EPVP-CRE-SG-D1-INF-AXI\pressure.txt'
ncoluna     = 109
lblcoluna   = '$d_1 = \infty$ and without gallery'
cor         = 'b'
tamanho     = 1.5
ordem       = 4
alpha       = 1
estilo      = 'dashed'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRE_CG_D1_16RE_3D\pressure_90.txt'
ncoluna     = 137
lblcoluna   = '$d_1 = 16R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.3
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRE_CG_D1_8RE_3D\pressure_90.txt'
ncoluna     = 120
lblcoluna   = ' $d_1 = 8R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 2
alpha       = 0.6
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRE_CG_D1_4RE_3D\pressure_90.txt'
ncoluna     = 111
lblcoluna   = '$d_1 = 4R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 1
alpha       = 1
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

""" ********************************************
PRESSURE PROFILES - LONG-TERM - EPVP_CRVE
******************************************** """ 

# Formatação do gráfico
figura      = 19
titulo      = 'Pressure Profiles - Long-term - EPVP_CRVE'
eixox       = r'$y/R_e$'  
eixoy       = r'$p=p(R_e,\theta = 90^\circ)$ [MPa]'
ymin        = -15
ymax        = 1
xmin        = 5
xmax        = 35
invertx     = True
inserirx0   = True
x0          = 80*1/3
suavizar    = True

# parametros para o filtro de suavização
filterx1    = 35
filterx2    = 90
wl          = 30
poly        = 2


arquivo     = 'EPVP-CRVE-SG-D1-INF-AXI\pressure.txt'
ncoluna     = 109
lblcoluna   = '$d_1 = \infty$ and without gallery'
cor         = 'b'
tamanho     = 1.5
ordem       = 4
alpha       = 1
estilo      = 'dashed'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRVE_CG_D1_16RE_3D\pressure_90.txt'
ncoluna     = 137
lblcoluna   = '$d_1 = 16R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 3
alpha       = 0.3
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRVE_CG_D1_8RE_3D\pressure_90.txt'
ncoluna     = 120
lblcoluna   = ' $d_1 = 8R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 2
alpha       = 0.6
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

arquivo     = 'EPVP_CRVE_CG_D1_4RE_3D\pressure_90.txt'
ncoluna     = 111
lblcoluna   = '$d_1 = 4R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 1
alpha       = 1
estilo      = 'solid'
graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

# figura      = 1
# arquivo     = 'EPVP_CRVE_CG_D1_4RE_3D\convergencias_90.txt'
# ncoluna     = 111
# lblcoluna   = 'EPVP_CRVE - $d_1 = 4R_e$'
# cor         = 'pink'
# tamanho     = 3
# ordem       = 1
# alpha       = 1
# graficar(arquivo,titulo,eixox,eixoy,
#          xmin,xmax,ymin,ymax,
#          ncoluna,lblcoluna,
#          cor,tamanho,ordem,alpha,
#          invertx,
#          suavizar,filterx1,filterx2,wl,poly,
#          figura)

# figura      = 1
# arquivo     = 'EP_CRE_CG_D1_8RE_3D\convergencias_90.txt'
# ncoluna     = 90
# lblcoluna   = 'EP_CRE - $d_1 = 8R_e$'
# cor         = 'g'
# tamanho     = 3
# ordem       = 1
# alpha       = 1
# graficar(arquivo,titulo,eixox,eixoy,
#           xmin,xmax,ymin,ymax,
#           ncoluna,lblcoluna,
#           cor,tamanho,ordem,alpha,
#           invertx,
#           suavizar,filterx1,filterx2,wl,poly,
#           figura)

# figura      = 1
# arquivo     = 'EP_CRE_CG_D1_16RE_3D\convergencias_90.txt'
# ncoluna     = 107
# lblcoluna   = 'EP_CRE - $d_1 = 16R_e$'
# cor         = 'r'
# tamanho     = 3
# ordem       = 1
# alpha       = 1
# graficar(arquivo,titulo,eixox,eixoy,
#           xmin,xmax,ymin,ymax,
#           ncoluna,lblcoluna,
#           cor,tamanho,ordem,alpha,
#           invertx,
#           suavizar,filterx1,filterx2,wl,poly,
#           figura)

# figura      = 1
# arquivo     = 'EP-CRE-SG-D1-INF-AXI\convergencias.txt'
# ncoluna     = 79
# lblcoluna   = 'EP_CRE - AXI'
# cor         = 'gray'
# tamanho     = 3
# ordem       = 1
# alpha       = 1
# graficar(arquivo,titulo,eixox,eixoy,
#           xmin,xmax,ymin,ymax,
#           ncoluna,lblcoluna,
#           cor,tamanho,ordem,alpha,
#           invertx,
#           suavizar,filterx1,filterx2,wl,poly,
#           figura)

# # Colocar uma linha vertical
# x0          = 80*1/3
# lblx0       = 'Face'
# plt.axvline(x0,color = 'k', label = lblx0, linestyle = '--')


# #GALERIA


# # Formatação do gráfico
# titulo      = 'Gallery Convergence Profiles'
# eixox       = r'$y/R_{e1}$'  
# eixoy       = r'$U{1}=-u{1}(R_{e1},\theta = 90^\circ)/R_{e1}$ [%]'
# ymin        = 0.75
# ymax        = 1.9
# xmin        = 0
# xmax        = 12
# invertx     = False

# # parametros para o filtro de suavização
# filterx1    = 0
# filterx2    = 80
# wl          = 20
# poly        = 6


# figura      = 2
# arquivo     = 'EPVP_CRVE_CG_D1_16RE_3D\convergencias1_90.txt'
# ncoluna     = 79
# lblcoluna   = 'EPVP_CRVE - $d_1 = 16R_e$'
# cor         = 'r'
# tamanho     = 3
# ordem       = 1
# alpha       = 1
# graficar(arquivo,titulo,eixox,eixoy,
#           xmin,xmax,ymin,ymax,
#           ncoluna,lblcoluna,
#           cor,tamanho,ordem,alpha,
#           invertx,
#           suavizar,filterx1,filterx2,wl,poly,
#           figura)

# figura      = 2
# arquivo     = 'EPVP_CRVE_CG_D1_8RE_3D\convergencias1_90.txt'
# ncoluna     = 79
# lblcoluna   = 'EPVP_CRVE - $d_1 = 8R_e$'
# cor         = 'green'
# tamanho     = 3
# ordem       = 1
# alpha       = 1
# graficar(arquivo,titulo,eixox,eixoy,
#           xmin,xmax,ymin,ymax,
#           ncoluna,lblcoluna,
#           cor,tamanho,ordem,alpha,
#           invertx,
#           suavizar,filterx1,filterx2,wl,poly,
#           figura)

# # parametros para o filtro de suavização
# filterx1    = 0
# filterx2    = 80
# wl          = 10
# poly        = 6

# figura      = 2
# arquivo     = 'EPVP_CRVE_CG_D1_4RE_3D\convergencias1_90.txt'
# ncoluna     = 79
# lblcoluna   = 'EPVP_CRVE - $d_1 = 4R_e$'
# cor         = 'b'
# tamanho     = 3
# ordem       = 1
# alpha       = 1
# graficar(arquivo,titulo,eixox,eixoy,
#           xmin,xmax,ymin,ymax,
#           ncoluna,lblcoluna,
#           cor,tamanho,ordem,alpha,
#           invertx,
#           suavizar,filterx1,filterx2,wl,poly,
#           figura)