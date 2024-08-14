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
    fig = plt.figure(figura,figsize = (4.5,2.5))

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
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter("{x:.2f}"))
    
    # aplica localização para o ponto decimal
    #plt.rcParams['axes.formatter.use_locale'] = True
    
    # Formatando grades
    plt.rcParams['axes.axisbelow'] = True 
    plt.grid(True,which = 'major')
    plt.grid(True,which = 'minor', alpha = 0.3)
    plt.minorticks_on()
    
    # Formatando fontes
    #rc('font',{'family':'Times New Roman','size' :12})
    #rc('font',{'family':'Times New Roman','size' :12})
    plt.rcParams['axes.unicode_minus'] = False
    plt.rc('text', usetex=True)
    plt.rc('axes', labelsize=12)
    plt.rc('xtick', labelsize=12) 
    plt.rc('ytick', labelsize=12)
    plt.rc('lines', lw=1.0,color='k')
    plt.rc('axes',lw=0.75)
    plt.rc('legend', fontsize=12)
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "Times"
        })
    
    # Inserir linha vertical em x0
    if inserirx0 == True:
        plt.axvline(x0-x0,color = 'k', lw = 2, linestyle = 'dotted')
    
    # adicionando título
    #plt.title(titulo, fontsize = 16, fontweight="bold") 
    #plt.autoscale(axis='y')
    
    # Formatando a legenda
    plt.legend(loc = 'lower left', ncol = 2, fontsize = 'medium')
    #plt.legend(
        #loc = 'center',
        #shadow=False,
        #framealpha = 0,
        #ncol = 4,
       # columnspacing = 0.5,
       # bbox_to_anchor=(0.5, -0.2),
        #fontsize="11")
    
    # Salvando em arquivo    
    plt.savefig(str(titulo) + '.svg', format='svg')
    #plt.savefig(str(titulo) + '.pdf', 
    #            dpi = fig.dpi, 
    #            bbox_inches='tight', 
    #            pad_inches=0.2)
    return x, y


def graficarxy(x,y,                   # nome do arquivo de leitura
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
    #data = pd.read_csv(arquivo,delim_whitespace= True).values

    # Definindo as dimensões do layout da figura
    fig = plt.figure(figura,figsize = (4.5,2.5))

    # Eixo x
   # if invertx == True:
    #    x = -(data[:,1]-max(data[:,1]))-x0
    #elif invertx == False:
    #    x =  data[:,1]
    #x = data[:,1]

    # dados do eixo y
    #y = data[:,ncoluna]
    #y = savgol_filter(data[:,ncoluna],20,10)
    
    #if suavizar == True:
    #    for i in range(1,3):
    #        y[filterx1:filterx2] = savgol_filter(data[filterx1:filterx2,ncoluna],wl,poly, mode = 'interp')
        
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
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter("{x:.2f}"))
    
    # aplica localização para o ponto decimal
    #plt.rcParams['axes.formatter.use_locale'] = True
    
    # Formatando grades
    plt.rcParams['axes.axisbelow'] = True 
    plt.grid(True,which = 'major')
    plt.grid(True,which = 'minor', alpha = 0.3)
    plt.minorticks_on()
    
    # Formatando fontes
    #rc('font',{'family':'Times New Roman','size' :12})
    #rc('font',{'family':'Times New Roman','size' :12})
    plt.rcParams['axes.unicode_minus'] = False
    plt.rc('text', usetex=True)
    plt.rc('axes', labelsize=12)
    plt.rc('xtick', labelsize=12) 
    plt.rc('ytick', labelsize=12)
    plt.rc('lines', lw=1.0,color='k')
    plt.rc('axes',lw=0.75)
    plt.rc('legend', fontsize=12)
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "Times"
        })
    
    # Inserir linha vertical em x0
    if inserirx0 == True:
        plt.axvline(x0-x0,color = 'k', lw = 2, linestyle = 'dotted')
    
    # adicionando título
    #plt.title(titulo, fontsize = 16, fontweight="bold") 
    #plt.autoscale(axis='y')
    
    # Formatando a legenda
    plt.legend(loc = 'lower left', ncol = 2, fontsize = 'medium')
    #plt.legend(
        #loc = 'center',
        #shadow=False,
        #framealpha = 0,
        #ncol = 4,
       # columnspacing = 0.5,
       # bbox_to_anchor=(0.5, -0.2),
        #fontsize="11")
    
    # Salvando em arquivo    
    plt.savefig(str(titulo) + '.svg', format='svg')
    #plt.savefig(str(titulo) + '.pdf', 
    #            dpi = fig.dpi, 
    #            bbox_inches='tight', 
    #            pad_inches=0.2)

#%% 3. DEFININDO OS DICIONÁRIOS COM AS COLUNAS DOS RESULTADOS
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
 
    'EP_CRE_ESP003_SG_D1_INF_AXI': 99,
    'EP_CRE_SG_D1_INF_AXI': 99,
    'EP_CRE_CG_D1_16RE_3D': 127,
    'EP_CRE_ESP003_CG_D1_16RE_3D': 127,
    'EP_CRE_CG_D1_8RE_3D': 110,
    'EP_CRE_CG_D1_4RE_3D': 101,
    'EP_CRE_ESP003_CG_D1_4RE_3D': 101,
    
    'EP_CRE_SG_D1_16RE_3D': 99,
    'EP_CRE_ESP003_SG_D1_16RE_3D': 99,
    'EP_CRE_SG_D1_8RE_3D': 99,
    'EP_CRE_SG_D1_4RE_3D': 99,
    'EP_CRE_ESP003_SG_D1_4RE_3D': 99,

    'VP_CRE_SG_D1_INF_AXI': 129,
    'VP_CRE_CG_D1_16RE_3D': 157,
    'VP_CRE_CG_D1_8RE_3D': 140,
    'VP_CRE_CG_D1_4RE_3D': 131, 
    
    'VP_CRE_SG_D1_16RE_3D': 129,
    'VP_CRE_SG_D1_8RE_3D': 129,
    'VP_CRE_SG_D1_4RE_3D': 129, 

    'EPVP_SR_SG_D1_INF_AXI': 129,

    'EPVP_CRE_ESP003_SG_D1_INF_AXI': 129,
    'EPVP_CRE_SG_D1_INF_AXI': 129,
    'EPVP_CRE_CG_D1_16RE_3D': 157,
    'EPVP_CRE_ESP003_CG_D1_16RE_3D': 157,
    'EPVP_CRE_CG_D1_8RE_3D': 140,
    'EPVP_CRE_CG_D1_4RE_3D': 131,
    'EPVP_CRE_ESP003_CG_D1_4RE_3D': 131,
    
    'EPVP_CRE_SG_D1_16RE_3D': 129,
    'EPVP_CRE_ESP003_SG_D1_16RE_3D': 129,
    'EPVP_CRE_SG_D1_8RE_3D': 129,
    'EPVP_CRE_SG_D1_4RE_3D': 129,
    'EPVP_CRE_ESP003_SG_D1_4RE_3D': 129,
    
    'EPVP_CRVE_ESP003_SG_D1_INF_AXI': 129,
    'EPVP_CRVE_SG_D1_INF_AXI': 129,
    'EPVP_CRVE_CG_D1_16RE_3D': 157,
    'EPVP_CRVE_ESP003_CG_D1_16RE_3D': 157,
    'EPVP_CRVE_CG_D1_8RE_3D': 140,
    'EPVP_CRVE_CG_D1_4RE_3D': 131,
    'EPVP_CRVE_ESP003_CG_D1_4RE_3D': 131,
    
    'EPVP_CRVE_SG_D1_16RE_3D': 129,
    'EPVP_CRVE_ESP003_SG_D1_16RE_3D': 129,
    'EPVP_CRVE_SG_D1_8RE_3D': 129,
    'EPVP_CRVE_SG_D1_4RE_3D': 129,
    'EPVP_CRVE_ESP003_SG_D1_4RE_3D': 129,
       
    }

dicncolunafinalexcavation = {

    'VP_CRE_SG_D1_INF_AXI': 99,
    'VP_CRE_CG_D1_16RE_3D': 127,
    'VP_CRE_CG_D1_8RE_3D': 110,
    'VP_CRE_CG_D1_4RE_3D': 101,
    
    'VP_CRE_SG_D1_16RE_3D': 99,
    'VP_CRE_SG_D1_8RE_3D': 99,
    'VP_CRE_SG_D1_4RE_3D': 99,

    'EPVP_SR_SG_D1_INF_AXI': 99,

    'EPVP_CRE_ESP003_SG_D1_INF_AXI': 99,
    'EPVP_CRE_SG_D1_INF_AXI': 99,
    'EPVP_CRE_CG_D1_16RE_3D': 127,
    'EPVP_CRE_ESP003_CG_D1_16RE_3D': 127,
    'EPVP_CRE_CG_D1_8RE_3D': 110,
    'EPVP_CRE_CG_D1_4RE_3D': 101,
    'EPVP_CRE_ESP003_CG_D1_4RE_3D': 101,
    
    'EPVP_CRE_SG_D1_16RE_3D': 99,
    'EPVP_CRE_ESP003_SG_D1_16RE_3D': 99,
    'EPVP_CRE_SG_D1_8RE_3D': 99,
    'EPVP_CRE_SG_D1_4RE_3D': 99,
    'EPVP_CRE_ESP003_SG_D1_4RE_3D': 99,
    
    'EPVP_CRVE_ESP003_SG_D1_INF_AXI': 99,
    'EPVP_CRVE_SG_D1_INF_AXI': 99,
    'EPVP_CRVE_CG_D1_16RE_3D': 127,
    'EPVP_CRVE_ESP003_CG_D1_16RE_3D': 127,
    'EPVP_CRVE_CG_D1_8RE_3D': 110,
    'EPVP_CRVE_CG_D1_4RE_3D': 101,
    'EPVP_CRVE_ESP003_CG_D1_4RE_3D': 101,
    
    'EPVP_CRVE_SG_D1_16RE_3D': 99,
    'EPVP_CRVE_ESP003_SG_D1_16RE_3D': 99,
    'EPVP_CRVE_SG_D1_8RE_3D': 99,
    'EPVP_CRVE_SG_D1_4RE_3D': 99,
    'EPVP_CRVE_ESP003_SG_D1_4RE_3D': 99,
       
    }

# Parametros para o túnel gêmeo
x0_twin_profile                         = 100*1/3
xmin_twin_profile                       = 5
xmax_twin_profile                       = 40
ymin_twin_convergence_profile           = 0
ymax_twin_convergence_profile           = 1.5
ymin_twin_pressure_profile              = -15
ymax_twin_pressure_profile              = 2.5

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

ncoluna = dicncolunalongterm['EP_CRE_SG_D1_INF_AXI']

figura = 1



#%% #. CONVERGENCE PROFILES - UB/UA - D1=4Re LT
""" ********************************************
CONVERGENCE PROFILES - UB e UA - D1=4Re LT
******************************************** """ 
# Formatação do gráfico
figura      = figura+1
titulo      = 'Convergence Profiles - UB-UA - $d_1=4R_t - Lt$'
eixox       = r'$z/R_t$'  
eixoy       = r'$U$ [\%]'
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


modelo      = 'EP_CRE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$U_B$, EP, EL, SG'
cor         = 'blue'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'solid'
x1 , y1 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

modelo      = 'EP_CRE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_0.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$U_A$, EP, EL, SG'
cor         = 'blue'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'dashed'
x2 , y2 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

modelo      = 'VP_CRE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$U_B$, VP, EL, SG, LT'
cor         = 'orange'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'solid'
x3 , y3 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

modelo      = 'VP_CRE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_0.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$U_A$, VP, EL, SG, LT'
cor         = 'orange'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'dashed'
x4 , y4 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

# parametros para o filtro de suavização
filterx1    = filterx1_twin_convergence_profile
filterx2    = filterx2_twin_convergence_profile
wl          = wl_twin_convergence_profile
poly        = poly_twin_convergence_profile

modelo      = 'EPVP_CRE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$U_B$, EPVP, EL, SG, LT'
cor         = 'black'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'solid'
x5 , y5 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

modelo      = 'EPVP_CRE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_0.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$U_A$, EPVP, EL, SG, LT'
cor         = 'black'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'dashed'
x6 , y6 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)


modelo      = 'EPVP_CRVE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$U_B$, EPVP, VEL, SG, LT'
cor         = 'red'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'solid'
x7 , y7 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

modelo      = 'EPVP_CRVE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_0.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$U_A$, EPVP, VEL, SG, LT'
cor         = 'red'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'dashed'
x8 , y8 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)


#%% #. CONVERGENCE PROFILES - UB/UA - D1=4Re LT
""" ********************************************
CONVERGENCE PROFILES - UB/UA - D1=4Re
******************************************** """

figura      = 30
titulo      = 'Convergence Profiles - UBUA - $d_1=4R_t - Lt$'
eixox       = r'$z/R_t$'  
eixoy       = r'$U_B/U_A$'
estilo      = 'solid'

ya = y2/y1
lblcoluna   = 'EP, EL, SG'
cor         = 'blue'
graficarxy(x1,ya,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)


yb = y4/y3
lblcoluna   = 'VP, EL, SG, LT'
cor         = 'orange'
graficarxy(x1,yb,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)


yc = y6/y5
lblcoluna   = 'EPVP, EL, SG, LT'
cor         = 'black'
graficarxy(x1,yc,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

yd = y8/y7
lblcoluna   = 'EPVP, VEL, SG, LT'
cor         = 'red'
graficarxy(x1,yd,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)





#%% #. CONVERGENCE PROFILES - UB/UA - D1=4Re ST
""" ********************************************
CONVERGENCE PROFILES - UB e UA - D1=4Re ST
******************************************** """ 
# Formatação do gráfico
figura      = figura+1
titulo      = 'Convergence Profiles - UB-UA - $d_1=4R_t - ST$'
eixox       = r'$z/R_t$'  
eixoy       = r'$U$ [\%]'
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


modelo      = 'EP_CRE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$U_B$, EP, EL, SG'
cor         = 'blue'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'solid'
x1 , y1 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

modelo      = 'EP_CRE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_0.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = '$U_A$, EP, EL, SG'
cor         = 'blue'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'dashed'
x2 , y2 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

modelo      = 'VP_CRE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunafinalexcavation[modelo]
lblcoluna   = '$U_B$, VP, EL, SG, ST'
cor         = 'orange'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'solid'
x3 , y3 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

modelo      = 'VP_CRE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_0.txt'
ncoluna     = dicncolunafinalexcavation[modelo]
lblcoluna   = '$U_A$, VP, EL, SG, ST'
cor         = 'orange'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'dashed'
x4 , y4 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

# parametros para o filtro de suavização
filterx1    = filterx1_twin_convergence_profile
filterx2    = filterx2_twin_convergence_profile
wl          = wl_twin_convergence_profile
poly        = poly_twin_convergence_profile

modelo      = 'EPVP_CRE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunafinalexcavation[modelo]
lblcoluna   = '$U_B$, EPVP, EL, SG, ST'
cor         = 'black'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'solid'
x5 , y5 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

modelo      = 'EPVP_CRE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_0.txt'
ncoluna     = dicncolunafinalexcavation[modelo]
lblcoluna   = '$U_A$, EPVP, EL, SG, ST'
cor         = 'black'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'dashed'
x6 , y6 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)


modelo      = 'EPVP_CRVE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunafinalexcavation[modelo]
lblcoluna   = '$U_B$, EPVP, VEL, SG, ST'
cor         = 'red'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'solid'
x7 , y7 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

modelo      = 'EPVP_CRVE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_0.txt'
ncoluna     = dicncolunafinalexcavation[modelo]
lblcoluna   = '$U_A$, EPVP, VEL, SG, ST'
cor         = 'red'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'dashed'
x8 , y8 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)


#%% #. CONVERGENCE PROFILES - UB/UA - D1=4Re ST
""" ********************************************
CONVERGENCE PROFILES - UB/UA - D1=4Re ST
******************************************** """

figura      = 32
titulo      = 'Convergence Profiles - UBUA - $d_1=4R_t - ST$'
eixox       = r'$z/R_t$'  
eixoy       = r'$U_B/U_A$'
estilo      = 'dashed'

ya = y2/y1
lblcoluna   = 'EP, EL, SG'
cor         = 'blue'
graficarxy(x1,ya,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)


yb = y4/y3
lblcoluna   = 'VP, EL, SG, ST'
cor         = 'orange'
graficarxy(x1,yb,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)


yc = y6/y5
lblcoluna   = 'EPVP, EL, SG, ST'
cor         = 'black'
graficarxy(x1,yc,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

yd = y8/y7
lblcoluna   = 'EPVP, VEL, SG, ST'
cor         = 'red'
graficarxy(x1,yd,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)



#%% #. CONVERGENCE PROFILES - UB/UA - D1=4Re ST-LT
""" ********************************************
CONVERGENCE PROFILES - UB e UA - D1=4Re LT
******************************************** """ 
# Formatação do gráfico
figura      = figura+1
titulo      = 'Convergence Profiles - UB - $d_1=4R_t - ST_Lt$'
eixox       = r'$z/R_t$'  
eixoy       = r'$U_B$ [\%]'
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


modelo      = 'EP_CRE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EP, EL, SG'
cor         = 'blue'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'solid'
x1 , y1 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

modelo      = 'VP_CRE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'VP, EL, SG, LT'
cor         = 'orange'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'solid'
x3 , y3 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

modelo      = 'VP_CRE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunafinalexcavation[modelo]
lblcoluna   = 'VP, EL, SG, ST'
cor         = 'orange'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'dashed'
x4 , y4 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

# parametros para o filtro de suavização
filterx1    = filterx1_twin_convergence_profile
filterx2    = filterx2_twin_convergence_profile
wl          = wl_twin_convergence_profile
poly        = poly_twin_convergence_profile

modelo      = 'EPVP_CRE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EPVP, EL, SG, LT'
cor         = 'black'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'solid'
x5 , y5 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

modelo      = 'EPVP_CRE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunafinalexcavation[modelo]
lblcoluna   = 'EPVP, EL, SG, ST'
cor         = 'black'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'dashed'
x6 , y6 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)


modelo      = 'EPVP_CRVE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunalongterm[modelo]
lblcoluna   = 'EPVP, VEL, SG, LT'
cor         = 'red'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'solid'
x7 , y7 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)

modelo      = 'EPVP_CRVE_SG_D1_4RE_3D'
arquivo     = modelo + '\convergencias_90.txt'
ncoluna     = dicncolunafinalexcavation[modelo]
lblcoluna   = 'EPVP, VEL, SG, ST'
cor         = 'red'
tamanho     = 2
ordem       = 3
alpha       = 1
estilo      = 'dashed'
x8 , y8 = graficar(arquivo,titulo,eixox,eixoy,
          xmin,xmax,ymin,ymax,
          ncoluna,lblcoluna,
          cor,tamanho,ordem,alpha,estilo,
          invertx,
          inserirx0,x0,
          suavizar,filterx1,filterx2,wl,poly,
          figura)