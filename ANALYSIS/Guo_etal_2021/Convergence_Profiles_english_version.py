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
#import locale                          # importa módulo para definir a localização usada no ponto decimal
from matplotlib.ticker import StrMethodFormatter # importa módulo para formatar eixo

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
    
    # define localização para o ponto decimal
    #locale.setlocale(locale.LC_NUMERIC,"ru_RU.utf8")
    
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
    plt.ylabel(eixoy, fontsize=12)
    plt.xlabel(eixox, fontsize=12)
    plt.legend()
    
    # numero de dígitos após o ponto decimal
    #plt.gca().yaxis.set_major_formatter(StrMethodFormatter("{x:.2f}"))
    
    # aplica localização para o ponto decimal
    #plt.rcParams['axes.formatter.use_locale'] = True
    
    # Formatando grades
    plt.rcParams['axes.axisbelow'] = True 
    plt.grid(True,which = 'major')
    plt.grid(True,which = 'minor', alpha = 0.3)
    plt.minorticks_on()
    
    # Inserir linha vertical em x0
    if inserirx0 == True:
        plt.axvline(x0-x0,color = 'k', lw = 2, linestyle = 'dotted')
    
    # adicionando título
    #plt.title(titulo, fontsize = 16, fontweight="bold") 
    #plt.autoscale(axis='y')
    
    # Formatando a legenda
    plt.legend(
        loc = 'center',
        shadow=False,
        framealpha = 0,
        ncol = 4,
        columnspacing = 0.5,
        bbox_to_anchor=(0.5, -0.2),
        fontsize="11")
    
    # Salvando em arquivo    
    plt.savefig(str(titulo) + '.pdf', 
                dpi = fig.dpi, 
                bbox_inches='tight', 
                pad_inches=0.2)

#%% 3. DEFININDO OS DICIONÁRIOS COM AS COLUNAS DOS RESULTADOS
dicncolunalongterm = {

    'GUO_AXI': 2,
    'GUO_D1_25RE': 2,
    'GUO_D1_3RE': 2,
    'GUO_D1_4RE': 2,
    'GUO_D1_5RE': 2,
    'GUO_D1_6RE': 2,
    'GUO_D1_8RE': 2,
    'GUO_D1_10RE': 2,    
       
    }

dicncolunafinalexcavation = {

       
    }

# Parametros para o túnel gêmeo
x0_twin_profile                         = 100*1/3
xmin_twin_profile                       = 5
xmax_twin_profile                       = 40
ymin_twin_convergence_profile           = 0
ymax_twin_convergence_profile           = 0.9
ymin_twin_pressure_profile              = -9
ymax_twin_pressure_profile              = 0

suavizar_twin                           = True

filterx1_twin_convergence_profile       = 40
filterx2_twin_convergence_profile       = 100
wl_twin_convergence_profile             = 30
poly_twin_convergence_profile           = 10

filterx1_twin_pressure_profile          = 40
filterx2_twin_pressure_profile          = 100
wl_twin_pressure_profile                = 30
poly_twin_pressure_profile              = 2

# Parametros para galeria
x0_gallery_profile                      = 0
xmin_gallery_profile                    = 0
xmax_gallery_profile                    = 12
ymin_gallery_convergence_profile        = 0
ymax_gallery_convergence_profile        = 2
ymin_gallery_pressure_profile           = 0
ymax_gallery_pressure_profile           = 1.5

suavizar_gallery                        = True

filterx1_gallery_convergence_profile    = 0
filterx2_gallery_convergence_profile    = 80
wl_gallery_convergence_profile          = 10
poly_gallery_convergence_profile        = 4

figura = 1

#%% CONVERGENCE PROFILES - FIXED MODEL VARIOUS D1
""" ********************************************
CONVERGENCE PROFILES - FIXED MODEL VARIOUS D1
******************************************** """

#%% #.  CONVERGENCE PROFILES - IN POINT B
""" ********************************************
CONVERGENCE PROFILES IN POINT B
******************************************** """ 

# Formatação do gráfico
figura      = figura+1
titulo      = 'Convergence Profiles in B'
eixox       = r'$z/R_t$'  
eixoy       = r'$U_B=-u(r = R_t,\theta = 90^\circ)/R_{t}$ [%]'
ymin        = ymin_twin_convergence_profile
ymax        = ymax_twin_convergence_profile
xmin        = xmin_twin_profile
xmax        = xmax_twin_profile
invertx     = True
inserirx0   = True
x0          = x0_twin_profile
suavizar    = suavizar_twin

# parametros para o filtro de suavização
filterx1    = filterx1_twin_convergence_profile
filterx2    = filterx2_twin_convergence_profile
wl          = wl_twin_convergence_profile
poly        = poly_twin_convergence_profile


modelo      = 'GUO_D1_25RE'
arquivo     = modelo + '\convergencex_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1/2R_t = 1.25$'
cor         = '#6a040f'
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


modelo      = 'GUO_D1_3RE'
arquivo     = modelo + '\convergencex_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1/2R_t = 1.5$'
cor         = '#f94144'
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

modelo      = 'GUO_D1_4RE'
arquivo     = modelo + '\convergencex_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1/2R_t = 2.0$'
cor         = '#f3722c'
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

modelo      = 'GUO_D1_5RE'
arquivo     = modelo + '\convergencex_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1/2R_t = 2.5$'
cor         = '#f8961e'
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

modelo      = 'GUO_D1_6RE'
arquivo     = modelo + '\convergencex_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1/2R_t = 3.0$'
cor         = '#F9C74F'
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

modelo      = 'GUO_D1_8RE'
arquivo     = modelo + '\convergencex_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1/2R_t = 4.0$'
cor         = '#90BE6D'
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

modelo      = 'GUO_D1_10RE'
arquivo     = modelo + '\convergencex_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1/2R_t = 5.0$'
cor         = '#43AA8B'
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

modelo      = 'GUO_AXI'
arquivo     = modelo + '\convergencias.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'Single Tunnel'
cor         = '#577590'
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



#%% #.  CONVERGENCE PROFILES - IN POINT A
""" ********************************************
CONVERGENCE PROFILES IN POINT A
******************************************** """ 

# Formatação do gráfico
figura      = figura+1
titulo      = 'Convergence Profiles in A'
eixox       = r'$z/R_t$'  
eixoy       = r'$U_A=-u(r = R_t,\theta = 0^\circ)/R_{t}$ [%]'
ymin        = ymin_twin_convergence_profile
ymax        = ymax_twin_convergence_profile
xmin        = xmin_twin_profile
xmax        = xmax_twin_profile
invertx     = True
inserirx0   = True
x0          = x0_twin_profile
suavizar    = suavizar_twin

# parametros para o filtro de suavização
filterx1    = filterx1_twin_convergence_profile
filterx2    = filterx2_twin_convergence_profile
wl          = wl_twin_convergence_profile
poly        = poly_twin_convergence_profile


modelo      = 'GUO_D1_25RE'
arquivo     = modelo + '\convergencex_0.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = 2.5R_t$'
cor         = '#6a040f'
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

modelo      = 'GUO_D1_3RE'
arquivo     = modelo + '\convergencex_0.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = 3R_t$'
cor         = '#f94144'
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

modelo      = 'GUO_D1_4RE'
arquivo     = modelo + '\convergencex_0.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = 4R_t$'
cor         = '#f3722c'
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

modelo      = 'GUO_D1_5RE'
arquivo     = modelo + '\convergencex_0.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = 5R_t$'
cor         = '#f8961e'
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

modelo      = 'GUO_D1_6RE'
arquivo     = modelo + '\convergencex_0.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = 6R_t$'
cor         = '#F9C74F'
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

modelo      = 'GUO_D1_8RE'
arquivo     = modelo + '\convergencex_0.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = 8R_t$'
cor         = '#90BE6D'
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

modelo      = 'GUO_D1_10RE'
arquivo     = modelo + '\convergencex_0.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = 10R_t$'
cor         = '#43AA8B'
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

modelo      = 'GUO_AXI'
arquivo     = modelo + '\convergencias.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = \infty R_t$'
cor         = '#577590'
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





#%% #.  ORTHORADIAL STRESS PROFILES - IN POINT B
""" ********************************************
ORTHORADIAL STRESS PROFILES IN POINT B
******************************************** """ 

# Formatação do gráfico
figura      = figura+1
titulo      = 'Orthoradial Stress Profiles in B'
eixox       = r'$z/R_t$'  
eixoy       = r'$\sigma_{\theta \theta}(r = R_t,\theta = 90^\circ)$ [MPa]'
ymin        = ymin_twin_pressure_profile
ymax        = ymax_twin_pressure_profile
xmin        = xmin_twin_profile
xmax        = xmax_twin_profile
invertx     = True
inserirx0   = True
x0          = x0_twin_profile
suavizar    = suavizar_twin

# parametros para o filtro de suavização
filterx1    = filterx1_twin_convergence_profile
filterx2    = filterx2_twin_convergence_profile
wl          = wl_twin_convergence_profile
poly        = poly_twin_convergence_profile


modelo      = 'GUO_D1_25RE'
arquivo     = modelo + '\stressy_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = 2.5R_t$'
cor         = '#6a040f'
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


modelo      = 'GUO_D1_3RE'
arquivo     = modelo + '\stressy_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = 3R_t$'
cor         = '#f94144'
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

modelo      = 'GUO_D1_4RE'
arquivo     = modelo + '\stressy_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = 4R_t$'
cor         = '#f3722c'
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

modelo      = 'GUO_D1_5RE'
arquivo     = modelo + '\stressy_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = 5R_t$'
cor         = '#f8961e'
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

modelo      = 'GUO_D1_6RE'
arquivo     = modelo + '\stressy_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = 6R_t$'
cor         = '#F9C74F'
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

modelo      = 'GUO_D1_8RE'
arquivo     = modelo + '\stressy_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = 8R_t$'
cor         = '#90BE6D'
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

modelo      = 'GUO_D1_10RE'
arquivo     = modelo + '\stressy_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = 10R_t$'
cor         = '#43AA8B'
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

modelo      = 'GUO_AXI'
arquivo     = modelo + '\pressurey.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = \infty R_t$'
cor         = '#577590'
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




#%% #.  ORTHORADIAL STRESS PROFILES - IN POINT A
""" ********************************************
ORTHORADIAL STRESS PROFILES IN POINT A
******************************************** """ 

# Formatação do gráfico
figura      = figura+1
titulo      = 'Orthoradial Stress Profiles in A'
eixox       = r'$z/R_t$'  
eixoy       = r'$\sigma_{\theta \theta}(r = R_t,\theta = 0^\circ)$ [MPa]'
ymin        = ymin_twin_pressure_profile
ymax        = ymax_twin_pressure_profile
xmin        = xmin_twin_profile
xmax        = xmax_twin_profile
invertx     = True
inserirx0   = True
x0          = x0_twin_profile
suavizar    = suavizar_twin

# parametros para o filtro de suavização
filterx1    = filterx1_twin_convergence_profile
filterx2    = filterx2_twin_convergence_profile
wl          = wl_twin_convergence_profile
poly        = poly_twin_convergence_profile


modelo      = 'GUO_D1_25RE'
arquivo     = modelo + '\stressy_0.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = 2.5R_t$'
cor         = '#6a040f'
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


modelo      = 'GUO_D1_3RE'
arquivo     = modelo + '\stressy_0.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = 3R_t$'
cor         = '#f94144'
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

modelo      = 'GUO_D1_4RE'
arquivo     = modelo + '\stressy_0.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = 4R_t$'
cor         = '#f3722c'
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

modelo      = 'GUO_D1_5RE'
arquivo     = modelo + '\stressy_0.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = 5R_t$'
cor         = '#f8961e'
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

modelo      = 'GUO_D1_6RE'
arquivo     = modelo + '\stressy_0.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = 6R_t$'
cor         = '#F9C74F'
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

modelo      = 'GUO_D1_8RE'
arquivo     = modelo + '\stressy_0.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = 8R_t$'
cor         = '#90BE6D'
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

modelo      = 'GUO_D1_10RE'
arquivo     = modelo + '\stressy_0.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = 10R_t$'
cor         = '#43AA8B'
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

modelo      = 'GUO_AXI'
arquivo     = modelo + '\pressurey.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = r'$d_1 = \infty R_t$'
cor         = '#577590'
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