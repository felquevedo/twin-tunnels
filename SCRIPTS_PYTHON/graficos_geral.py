# -*- coding: utf-8 -*-
""" ********************************************
SCRIPT PARA PLOTAGEM DA CURVA DE CONVERGÊNCIA
DAS ANÁLISES EM AXISSIMETRIA
Versão: 2023.1
Situação : Teste (11/07/2020) 
******************************************** """ 

#%% 1. IMPORTAR BIBLIOTECAS

import pandas as pd                   # importa o pacote para manmipular tabelas 
import matplotlib.pyplot as plt       # importa o módulo para plotagem
from scipy.signal import savgol_filter # importa filtro

#%% 2. FUNÇÃO GRAFICAR

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
    fig = plt.figure(figura,figsize = (9,5))

    # Eixo x
    if invertx == True:
        x = -(data[:,1]-max(data[:,1]))-x0
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
    plt.xlim([xmin-x0, xmax-x0])
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
        plt.axvline(x0-x0,color = 'k', lw = 2, linestyle = 'dotted')
    
    # adicionando título
    plt.title(titulo, fontsize = 16) 
    #plt.autoscale(axis='y')
    
    # Formatando a legenda
    plt.legend(
        loc = 'center',
        shadow=False,
        framealpha = 0,
        ncol = 4,
        columnspacing = 0.5,
        bbox_to_anchor=(0.5, -0.2))
    
    # Salvando em arquivo    
    plt.savefig(str(titulo) + '.pdf', 
                dpi = fig.dpi, 
                bbox_inches='tight', 
                pad_inches=0.2)

#%% 3. DEFININDO OS DICIONÁRIOS COM AS COLUNAS DOS RESULTADOS
dicncolunalongterm = {
   
    'EP_CRE_SG_D1_INF_AXI': 79,
    'EP_CRE_CG_D1_16RE_3D': 107,
    'EP_CRE_CG_D1_8RE_3D': 90,
    'EP_CRE_CG_D1_4RE_3D': 81,
    
    'EP_CRE_SG_D1_16RE_3D': 79,
    'EP_CRE_SG_D1_8RE_3D': 79,
    'EP_CRE_SG_D1_4RE_3D': 79,

    'VP_CRE_SG_D1_INF_AXI': 109,
    'VP_CRE_CG_D1_16RE_3D': 137,
    'VP_CRE_CG_D1_8RE_3D': 120,
    'VP_CRE_CG_D1_4RE_3D': 111, 
    
    'VP_CRE_SG_D1_16RE_3D': 109,
    'VP_CRE_SG_D1_8RE_3D': 109,
    'VP_CRE_SG_D1_4RE_3D': 109, 

    'EPVP_CRE_SG_D1_INF_AXI': 109,
    'EPVP_CRE_CG_D1_16RE_3D': 137,
    'EPVP_CRE_CG_D1_8RE_3D': 120,
    'EPVP_CRE_CG_D1_4RE_3D': 111,
    
    'EPVP_CRE_SG_D1_16RE_3D': 109,
    'EPVP_CRE_SG_D1_8RE_3D': 109,
    'EPVP_CRE_SG_D1_4RE_3D': 109,
    
    'EPVP_CRVE_SG_D1_INF_AXI': 109,
    'EPVP_CRVE_CG_D1_16RE_3D': 137,
    'EPVP_CRVE_CG_D1_8RE_3D': 120,
    'EPVP_CRVE_CG_D1_4RE_3D': 111,
    
    'EPVP_CRVE_SG_D1_16RE_3D': 109,
    'EPVP_CRVE_SG_D1_8RE_3D': 109,
    'EPVP_CRVE_SG_D1_4RE_3D': 109,
       
    }

dicncolunafinalexcavation = {

    'VP_CRE_SG_D1_INF_AXI': 79,
    'VP_CRE_CG_D1_16RE_3D': 107,
    'VP_CRE_CG_D1_8RE_3D': 90,
    'VP_CRE_CG_D1_4RE_3D': 81,
    
    'VP_CRE_SG_D1_16RE_3D': 79,
    'VP_CRE_SG_D1_8RE_3D': 79,
    'VP_CRE_SG_D1_4RE_3D': 79,

    'EPVP_CRE_SG_D1_INF_AXI': 79,
    'EPVP_CRE_CG_D1_16RE_3D': 107,
    'EPVP_CRE_CG_D1_8RE_3D': 90,
    'EPVP_CRE_CG_D1_4RE_3D': 81,
    
    'EPVP_CRE_SG_D1_16RE_3D': 79,
    'EPVP_CRE_SG_D1_8RE_3D': 79,
    'EPVP_CRE_SG_D1_4RE_3D': 79,
    
    'EPVP_CRVE_SG_D1_INF_AXI': 79,
    'EPVP_CRVE_CG_D1_16RE_3D': 107,
    'EPVP_CRVE_CG_D1_8RE_3D': 90,
    'EPVP_CRVE_CG_D1_4RE_3D': 82,
    
    'EPVP_CRVE_SG_D1_16RE_3D': 79,
    'EPVP_CRVE_SG_D1_8RE_3D': 79,
    'EPVP_CRVE_SG_D1_4RE_3D': 79,
       
    }

ncoluna = dicncolunalongterm['EP_CRE_SG_D1_INF_AXI']

#%% 4. CONVERGENCE PROFILES - MODEL EP_CRE
""" ********************************************
CONVERGENCE PROFILES - MODEL EP_CRE
******************************************** """ 

# Formatação do gráfico
figura      = 1
titulo      = 'Convergence Profiles - EP_CRE'
eixox       = r'$y/R_e$'  
eixoy       = r'$U=-u(R_e,\theta = 90^\circ)/R_{e}$ [%]'
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

modelo      = 'EP_CRE_SG_D1_INF_AXI'
arquivo     = modelo + '\convergencias.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = \infty$ and without gallery'
cor         = 'k'
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

modelo      = 'EP_CRE_CG_D1_16RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = 16R_e$'
cor         = 'orange'
tamanho     = 2
ordem       = 3
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


modelo      = 'EP_CRE_CG_D1_8RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = ' $d_1 = 8R_e$'
cor         = 'g'
tamanho     = 2
ordem       = 2
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


modelo      = 'EP_CRE_CG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
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

#%% 5. CONVERGENCE PROFILES - LONG-TERM - MODEL VP_CRE
""" ********************************************
CONVERGENCE PROFILES - LONG-TERM - MODEL VP_CRE
******************************************** """ 

# Formatação do gráfico
figura      = figura+1
titulo      = 'Convergence Profiles - Long-term - VP_CRE'
eixox       = r'$y/R_e$'  
eixoy       = r'$U=-u(R_e,\theta = 90^\circ)/R_{e}$ [%]'
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


modelo      = 'VP_CRE_SG_D1_INF_AXI'
arquivo     = modelo + '\convergencias.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = \infty$ without gallery'
cor         = 'k'
tamanho     = 2
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

modelo      = 'VP_CRE_CG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = 4R_e$'
cor         = 'r'
tamanho     = 2
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

modelo      = 'VP_CRE_CG_D1_8RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = 8R_e$'
cor         = 'g'
tamanho     = 2
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

#%% 6. CONVERGENCE PROFILES - FINAL EXCAVATION - MODEL VP_CRE
""" ********************************************
CONVERGENCE PROFILES - FINAL EXCAVATION - MODEL VP_CRE
******************************************** """ 

# Formatação do gráfico
figura      = figura+1
titulo      = 'Convergence Profiles - Final excavation - VP_CRE'
eixox       = r'$y/R_e$'  
eixoy       = r'$U=-u(R_e,\theta = 90^\circ)/R_{e}$ [%]'
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

modelo      = 'VP_CRE_SG_D1_INF_AXI'
arquivo     = modelo + '\convergencias.txt'
ncoluna     = dicncolunafinalexcavation[modelo]
lblcoluna   = '$d_1 = \infty$ without gallery'
cor         = 'k'
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

modelo      = 'VP_CRE_CG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunafinalexcavation[modelo]
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


modelo      = 'VP_CRE_CG_D1_8RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunafinalexcavation[modelo]
lblcoluna   = '$d_1 = 8R_e$'
cor         = 'g'
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

#%% 7. CONVERGENCE PROFILES - LONG-TERM - EPVP_CRE
""" ********************************************
CONVERGENCE PROFILES - LONG-TERM - EPVP_CRE
******************************************** """ 

# Formatação do gráfico
figura      = figura+1
titulo      = 'Convergence Profiles - Long-term - EPVP_CRE'
eixox       = r'$y/R_e$'  
eixoy       = r'$U=-u(R_e,\theta = 90^\circ)/R_{e}$ [%]'
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


modelo      = 'EPVP_CRE_SG_D1_INF_AXI'
arquivo     = modelo + '\convergencias.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = \infty$ and without gallery'
cor         = 'k'
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

modelo      = 'EPVP_CRE_CG_D1_16RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = 16R_e$'
cor         = 'orange'
tamanho     = 2
ordem       = 3
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

modelo      = 'EPVP_CRE_CG_D1_8RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = ' $d_1 = 8R_e$'
cor         = 'g'
tamanho     = 2
ordem       = 2
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

modelo      = 'EPVP_CRE_CG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
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

#%% 8. CONVERGENCE PROFILES - FINAL-EXCAVATION - EPVP_CRE
""" ********************************************
CONVERGENCE PROFILES - FINAL-EXCAVATION - EPVP_CRE
******************************************** """ 

# Formatação do gráfico
figura      = figura+1
titulo      = 'Convergence Profiles - Final Excavation - EPVP_CRE'
eixox       = r'$y/R_e$'  
eixoy       = r'$U=-u(R_e,\theta = 90^\circ)/R_{e}$ [%]'
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

modelo      = 'EPVP_CRE_SG_D1_INF_AXI'
arquivo     = modelo + '\convergencias.txt'
ncoluna     = dicncolunafinalexcavation[modelo]
lblcoluna   = '$d_1 = \infty$ and without gallery'
cor         = 'k'
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

modelo      = 'EPVP_CRE_CG_D1_16RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunafinalexcavation[modelo]
lblcoluna   = '$d_1 = 16R_e$'
cor         = 'orange'
tamanho     = 2
ordem       = 3
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

modelo      = 'EPVP_CRE_CG_D1_8RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunafinalexcavation[modelo]
lblcoluna   = ' $d_1 = 8R_e$'
cor         = 'g'
tamanho     = 2
ordem       = 2
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

modelo      = 'EPVP_CRE_CG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunafinalexcavation[modelo]
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

#%% 9. CONVERGENCE PROFILES - LONG-TERM - EPVP_CRVE
""" ********************************************
CONVERGENCE PROFILES - LONG-TERM - EPVP_CRVE
******************************************** """ 

# Formatação do gráfico
figura      = figura+1
titulo      = 'Convergence Profiles - Long-term - EPVP_CRVE'
eixox       = r'$y/R_e$'  
eixoy       = r'$U=-u(R_e,\theta = 90^\circ)/R_{e}$ [%]'
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


modelo      = 'EPVP_CRVE_SG_D1_INF_AXI'
arquivo     = modelo + '\convergencias.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = \infty$ and without gallery'
cor         = 'k'
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

modelo      = 'EPVP_CRVE_CG_D1_16RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = 16R_e$'
cor         = 'orange'
tamanho     = 2
ordem       = 3
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

modelo      = 'EPVP_CRVE_CG_D1_8RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = ' $d_1 = 8R_e$'
cor         = 'g'
tamanho     = 2
ordem       = 2
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

modelo      = 'EPVP_CRVE_CG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
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

#%% 10. CONVERGENCE PROFILES - FINAL EXCAVATION - EPVP_CRVE
""" ********************************************
CONVERGENCE PROFILES - FINAL EXCAVATION - EPVP_CRVE
******************************************** """ 

# Formatação do gráfico
figura      = figura+1
titulo      = 'Convergence Profiles - Final excavation - EPVP_CRVE'
eixox       = r'$y/R_e$'  
eixoy       = r'$U=-u(R_e,\theta = 90^\circ)/R_{e}$ [%]'
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


modelo      = 'EPVP_CRVE_SG_D1_INF_AXI'
arquivo     = modelo + '\convergencias.txt'
ncoluna     = dicncolunafinalexcavation[modelo]
lblcoluna   = '$d_1 = \infty$ and without gallery'
cor         = 'k'
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

modelo      = 'EPVP_CRVE_CG_D1_16RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunafinalexcavation[modelo]
lblcoluna   = '$d_1 = 16R_e$'
cor         = 'orange'
tamanho     = 2
ordem       = 3
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

modelo      = 'EPVP_CRVE_CG_D1_8RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunafinalexcavation[modelo]
lblcoluna   = ' $d_1 = 8R_e$'
cor         = 'g'
tamanho     = 2
ordem       = 2
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

modelo      = 'EPVP_CRVE_CG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunafinalexcavation[modelo]
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

#%% 11. CONVERGENCE PROFILES - LONG-TERM - D1=16Re
""" ********************************************
CONVERGENCE PROFILES - LONG-TERM - D1=16Re
******************************************** """ 

# Formatação do gráfico
figura      = figura+1
titulo      = 'Convergence Profiles - Long-term - $d_1=16R_e$'
eixox       = r'$y/R_e$'  
eixoy       = r'$U=-u(R_e,\theta = 90^\circ)/R_{e}$ [%]'
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


modelo      = 'EP_CRE_CG_D1_16RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EP_CRE'
cor         = 'orange'
tamanho     = 2
ordem       = 3
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

modelo      = 'EPVP_CRE_CG_D1_16RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EPVP_CRE'
cor         = 'g'
tamanho     = 2
ordem       = 3
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

modelo      = 'EPVP_CRVE_CG_D1_16RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EPVP_CRVE'
cor         = 'r'
tamanho     = 2
ordem       = 3
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

#%% 12. CONVERGENCE PROFILES - LONG-TERM - D1=8Re
""" ********************************************
CONVERGENCE PROFILES - LONG-TERM - D1=8Re
******************************************** """ 

# Formatação do gráfico
figura      = figura+1
titulo      = 'Convergence Profiles - Long-term - $d_1=8R_e$'
eixox       = r'$y/R_e$'  
eixoy       = r'$U=-u(R_e,\theta = 90^\circ)/R_{e}$ [%]'
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

modelo      = 'EP_CRE_CG_D1_8RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EP_CRE'
cor         = 'orange'
tamanho     = 2
ordem       = 3
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

modelo      = 'EPVP_CRE_CG_D1_8RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EPVP_CRE'
cor         = 'g'
tamanho     = 2
ordem       = 3
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

modelo      = 'EPVP_CRVE_CG_D1_8RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EPVP_CRVE'
cor         = 'r'
tamanho     = 2
ordem       = 3
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

#%% 13. CONVERGENCE PROFILES - LONG-TERM - D1=4Re
""" ********************************************
CONVERGENCE PROFILES - LONG-TERM - D1=4Re
******************************************** """ 

# Formatação do gráfico
figura      = figura+1
titulo      = 'Convergence Profiles - Long-term - $d_1=4R_e$'
eixox       = r'$y/R_e$'  
eixoy       = r'$U=-u(R_e,\theta = 90^\circ)/R_{e}$ [%]'
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

modelo      = 'EP_CRE_CG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EP_CRE'
cor         = 'orange'
tamanho     = 2
ordem       = 3
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

modelo      = 'EPVP_CRE_CG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EPVP_CRE'
cor         = 'g'
tamanho     = 2
ordem       = 3
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

modelo      = 'EPVP_CRVE_CG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EPVP_CRVE'
cor         = 'r'
tamanho     = 2
ordem       = 3
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

#%% 14. GALLERY CONVERGENCE PROFILES - LONG-TERM - D1=16Re
""" ********************************************
GALLERY CONVERGENCE PROFILES - LONG-TERM - D1=16Re
******************************************** """ 

# Formatação do gráfico
figura      = figura+1
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

modelo      = 'EP_CRE_SG_D1_16RE_3D'
arquivo     = modelo + '\convergencias1_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EP_CRE - without gallery'
cor         = 'k'
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

modelo      = 'EP_CRE_CG_D1_16RE_3D'
arquivo     = modelo + '\convergencias1_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EP_CRE'
cor         = 'orange'
tamanho     = 2
ordem       = 3
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

modelo      = 'EPVP_CRE_CG_D1_16RE_3D'
arquivo     = modelo + '\convergencias1_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EPVP_CRE'
cor         = 'g'
tamanho     = 2
ordem       = 3
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

modelo      = 'EPVP_CRVE_CG_D1_16RE_3D'
arquivo     = modelo + '\convergencias1_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EPVP_CRVE'
cor         = 'r'
tamanho     = 2
ordem       = 3
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

#%% 15. GALLERY CONVERGENCE PROFILES - LONG-TERM - D1=8Re
""" ********************************************
GALLERY CONVERGENCE PROFILES - LONG-TERM - D1=8Re
******************************************** """ 

# Formatação do gráfico
figura      = figura+1
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

modelo      = 'EP_CRE_SG_D1_8RE_3D'
arquivo     = modelo + '\convergencias1_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EP_CRE - without gallery'
cor         = 'k'
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

modelo      = 'EP_CRE_CG_D1_8RE_3D'
arquivo     = modelo + '\convergencias1_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EP_CRE'
cor         = 'orange'
tamanho     = 2
ordem       = 3
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

modelo      = 'EPVP_CRE_CG_D1_8RE_3D'
arquivo     = modelo + '\convergencias1_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EPVP_CRE'
cor         = 'g'
tamanho     = 2
ordem       = 3
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

modelo      = 'EPVP_CRVE_CG_D1_8RE_3D'
arquivo     = modelo + '\convergencias1_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EPVP_CRVE'
cor         = 'r'
tamanho     = 2
ordem       = 3
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

#%% 16. GALLERY CONVERGENCE PROFILES - LONG-TERM - D1=4Re
""" ********************************************
GALLERY CONVERGENCE PROFILES - LONG-TERM - D1=4Re
******************************************** """ 

# Formatação do gráfico
figura      = figura+1
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

modelo      = 'EP_CRE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias1_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EP_CRE - without gallery'
cor         = 'k'
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

modelo      = 'EP_CRE_CG_D1_4RE_3D'
arquivo     = modelo + '\convergencias1_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EP_CRE'
cor         = 'orange'
tamanho     = 2
ordem       = 3
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

modelo      = 'EPVP_CRE_CG_D1_4RE_3D'
arquivo     = modelo + '\convergencias1_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EPVP_CRE'
cor         = 'g'
tamanho     = 2
ordem       = 3
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

modelo      = 'EPVP_CRVE_CG_D1_4RE_3D'
arquivo     = modelo + '\convergencias1_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EPVP_CRVE'
cor         = 'r'
tamanho     = 2
ordem       = 3
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


#%% 17. GALLERY CONVERGENCE PROFILES EP-CRE
""" ********************************************
GALLERY CONVERGENCE PROFILES EP-CRE
******************************************** """ 

# Formatação do gráfico
figura      = figura+1
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

modelo      = 'EP_CRE_CG_D1_4RE_3D'
arquivo     = modelo + '\convergencias1_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = 4R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 3
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

# parametros para o filtro de suavização
filterx1    = 0
filterx2    = 80
wl          = 20
poly        = 5

modelo      = 'EP_CRE_CG_D1_8RE_3D'
arquivo     = modelo + '\convergencias1_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = 8R_e$'
cor         = 'g'
tamanho     = 2
ordem       = 3
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

modelo      = 'EP_CRE_CG_D1_16RE_3D'
arquivo     = modelo + '\convergencias1_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = 16R_e$'
cor         = 'orange'
tamanho     = 2
ordem       = 3
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


#%% 18. GALLERY CONVERGENCE PROFILES - LONG-TERM - EPVP-CRE
""" ********************************************
GALLERY CONVERGENCE PROFILES - LONG-TERM - EPVP-CRE
******************************************** """ 

# Formatação do gráfico
figura      = figura+1
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

modelo      = 'EPVP_CRE_CG_D1_4RE_3D'
arquivo     = modelo + '\convergencias1_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = 4R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 3
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

# parametros para o filtro de suavização
filterx1    = 0
filterx2    = 80
wl          = 20
poly        = 5

modelo      = 'EPVP_CRE_CG_D1_8RE_3D'
arquivo     = modelo + '\convergencias1_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = 8R_e$'
cor         = 'g'
tamanho     = 2
ordem       = 3
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

modelo      = 'EPVP_CRE_CG_D1_16RE_3D'
arquivo     = modelo + '\convergencias1_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = 16R_e$'
cor         = 'orange'
tamanho     = 2
ordem       = 3
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

#%% 19. GALLERY CONVERGENCE PROFILES - LONG-TERM - EPVP-CRVE
""" ********************************************
GALLERY CONVERGENCE PROFILES - LONG-TERM - EPVP-CRVE
******************************************** """ 

# Formatação do gráfico
figura      = figura+1
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

modelo      = 'EPVP_CRVE_CG_D1_4RE_3D'
arquivo     = modelo + '\convergencias1_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = 4R_e$'
cor         = 'r'
tamanho     = 2
ordem       = 3
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

# parametros para o filtro de suavização
filterx1    = 0
filterx2    = 80
wl          = 20
poly        = 5

modelo      = 'EPVP_CRVE_CG_D1_8RE_3D'
arquivo     = modelo + '\convergencias1_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = 8R_e$'
cor         = 'g'
tamanho     = 2
ordem       = 3
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

modelo      = 'EPVP_CRVE_CG_D1_16RE_3D'
arquivo     = modelo + '\convergencias1_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = 16R_e$'
cor         = 'orange'
tamanho     = 2
ordem       = 3
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



#%% 20. PRESSURE PROFILES - EP_CRE
""" ********************************************
PRESSURE PROFILES - EP_CRE
******************************************** """ 

# Formatação do gráfico
figura      = figura+1
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

modelo      = 'EP_CRE_SG_D1_INF_AXI'
arquivo     = modelo + '\pressure.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = \infty$ and without gallery'
cor         = 'k'
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

modelo      = 'EP_CRE_CG_D1_16RE_3D'
arquivo     = modelo + '\pressure_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = 16R_e$'
cor         = 'orange'
tamanho     = 2
ordem       = 3
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

modelo      = 'EP_CRE_CG_D1_8RE_3D'
arquivo     = modelo + '\pressure_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = ' $d_1 = 8R_e$'
cor         = 'g'
tamanho     = 2
ordem       = 2
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

modelo      = 'EP_CRE_CG_D1_4RE_3D'
arquivo     = modelo + '\pressure_90.txt'
ncoluna     = dicncolunalongterm[modelo]
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

#%% 21. PRESSURE PROFILES - LONG-TERM - EPVP_CRE
""" ********************************************
PRESSURE PROFILES - LONG-TERM - EPVP_CRE
******************************************** """ 

# Formatação do gráfico
figura      = figura+1
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

modelo      = 'EPVP_CRE_SG_D1_INF_AXI'
arquivo     = modelo + '\pressure.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = \infty$ and without gallery'
cor         = 'k'
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

modelo      = 'EPVP_CRE_CG_D1_16RE_3D'
arquivo     = modelo + '\pressure_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = 16R_e$'
cor         = 'orange'
tamanho     = 2
ordem       = 3
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

modelo      = 'EPVP_CRE_CG_D1_8RE_3D'
arquivo     = modelo + '\pressure_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = ' $d_1 = 8R_e$'
cor         = 'g'
tamanho     = 2
ordem       = 2
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

modelo      = 'EPVP_CRE_CG_D1_4RE_3D'
arquivo     = modelo + '\pressure_90.txt'
ncoluna     = dicncolunalongterm[modelo]
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

#%% 22. PRESSURE PROFILES - LONG-TERM - EPVP_CRVE
""" ********************************************
PRESSURE PROFILES - LONG-TERM - EPVP_CRVE
******************************************** """ 

# Formatação do gráfico
figura      = figura+1
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

modelo      = 'EPVP_CRVE_SG_D1_INF_AXI'
arquivo     = modelo + '\pressure.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = \infty$ and without gallery'
cor         = 'k'
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

modelo      = 'EPVP_CRVE_CG_D1_16RE_3D'
arquivo     = modelo + '\pressure_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$d_1 = 16R_e$'
cor         = 'orange'
tamanho     = 2
ordem       = 3
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

modelo      = 'EPVP_CRVE_CG_D1_8RE_3D'
arquivo     = modelo + '\pressure_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = ' $d_1 = 8R_e$'
cor         = 'g'
tamanho     = 2
ordem       = 2
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

modelo      = 'EPVP_CRVE_CG_D1_4RE_3D'
arquivo     = modelo + '\pressure_90.txt'
ncoluna     = dicncolunalongterm[modelo]
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

