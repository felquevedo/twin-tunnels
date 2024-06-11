

import matplotlib.pyplot as plt        # importa o módulo para plotagem
#from matplotlib.ticker import StrMethodFormatter # importa módulo para formatar eixo
import numpy as np
from matplotlib import rc
#import locale                          # importa módulo para definir a localização usada no ponto decimal

def graficar(x,y,                       # eixo x e y
             titulo,                    # titulo do gráfico
             eixox,eixoy,               # nome dos eixos x e y
             xmin,xmax,xstep,           # intervalo eixo x
             ymin,ymax,ystep,           # intervalo eixo y
             lbldata,                   # legenda dos dados
             cor,tamanho,ordem,alpha,estilo,marker,   # formatacao
             figura):

    # define localização para o ponto decimal
    #locale.setlocale(locale.LC_NUMERIC,"ru_RU.utf8")
    
    # adicionando título
    #plt.title(titulo, fontsize = 16, fontweight="bold") 
    
    # Definindo as dimensões do layout da figura
    fig = plt.figure(figura,figsize = (9,5))    
    
    # Definindo ponto decimal
    #plt.gca().yaxis.set_major_formatter(StrMethodFormatter("{x:.2f}"))

    # aplica localização para o ponto decimal
    #plt.rcParams['axes.formatter.use_locale'] = True

    # Formatando grades
    plt.rcParams['axes.axisbelow'] = True 
    plt.grid(True,which = 'major')
    plt.grid(True,which = 'minor', alpha = 0.3)
    plt.minorticks_on()
    
    # Formatando legendas
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
    
    # Formatando os eixos
    plt.ylim([ymin, ymax])
    plt.xlim([xmin, xmax])
    plt.ylabel(eixoy, fontsize=12)
    plt.xlabel(eixox, fontsize=12)
    # Formatando eixos
    plt.xticks(np.arange(xmin, xmax+0.01, step=xstep))
    plt.yticks(np.arange(ymin, ymax+0.01, step=ystep))
    plt.legend()
    
    # Plotando
    plt.plot(x,y,color = cor,
             zorder = ordem, 
             linestyle=estilo, 
             lw = tamanho, 
             alpha = alpha, 
             label = lbldata,
             marker = marker,
             fillstyle = 'none')

    # Formatando a legenda
    plt.legend(loc = 'upper right', ncol = 1)
    #plt.legend(
    #    loc = 'center',
    #    shadow=False,
    #    framealpha = 0,
    #    ncol = 2,
    #    columnspacing = 0.5,
    #    bbox_to_anchor=(0.5, -0.22),
    #    fontsize="11")

    # Salvando em arquivo    
    plt.savefig(str(titulo) + '.pdf', 
                dpi = fig.dpi, 
                bbox_inches='tight', 
                pad_inches=0.2)

Rt = 1

q0 = 30

# Valores coletados no bloco de notas
#sttA = np.array([17.7, 23.50, 23.0, 24.25, 23.0, 24.40])/q0
#sttB = np.array([20.16, 23.0, 22.6, 23.76, 22.60, 24.15])/q0
#UA   = np.array([1.50, 0.61, 0.505, 0.472, 0.470, 0.470])
#UB   = np.array([0.576, 0.476, 0.464, 0.460, 0.470, 0.470])


# Ajustando os casos de d1/2Rt de 5 e 8
x = np.array([3, 4,5, 6,8, 10])/(2)
sttA = np.array([17.7, 23.50, 24+0, 24.25, 24.3, 24.40])/q0
sttB = np.array([20.16, 23.0, 22.6, 23.76, 22.60, 24.15])/q0

UA   = np.array([1.50, 0.61, 0.505, 0.472, 0.470, 0.470])
UB   = np.array([0.576, 0.476, 0.464, 0.460, 0.470, 0.470])



# Retirando os casos de d1/2Rt 5 e 8
#x = np.array([3, 4, 6, 10])/(2)
#sttA = np.array([17.7, 23.50, 24.25, 24.40])/q0
#sttB = np.array([20.16, 23.0, 23.76, 24.15])/q0
#UA   = np.array([1.50, 0.61, 0.472, 0.470])
#UB   = np.array([0.576, 0.476, 0.460, 0.470])

#x_analitycal = np.array([2.5, 3, 3.5, 4, 4.5, 5, 5.5,6])/(2)
#sttA_analitycal = [3.874, 3.077, 2.761, 2.576, 2.456, 2.383, 2.317, 2.283]

#x_numerical = np.array([2.5, 3, 3.5, 4, 4.5, 5, 5.5,6])/(2)
#sttA_numerical = [3.854, 2.965, 2.616, 2.411, 2.285, 2.199, 2.132, 2.079]

#x_Ling = np.array([3, 4, 6])/(2)
#sttA_Ling = [2.867, 2.372, 2.112]


figura      = 1
titulo      = 'Tangencial stress concentration factor in A'
eixoy       = r'$\sigma_{\theta \theta}/\sigma_v$'
eixox       = r'$d_1/2R_t$'
xmin        = 1.25
xmax        = 5.0
xstep       = 0.25
ymin        = 0
ymax        = 1.5
ystep       = 0.25

lbldata     = '3D F.E. Solution'
cor         = 'r'
tamanho     = 1.5
ordem       = 1
alpha       = 1
estilo      = 'solid'
marker      = "D"

graficar(x,sttA,titulo,eixox,eixoy,
          xmin,xmax,xstep,ymin,ymax,ystep,
          lbldata,
          cor,tamanho,ordem,alpha,estilo,marker,
          figura)

lbldata     = 'Single Tunnel'
cor         = 'k'
tamanho     = 1.5
ordem       = 1
alpha       = 1
estilo      = 'dashed'
marker      = ""

graficar([0,5.0],[25.1/q0,25.1/q0],titulo,eixox,eixoy,
          xmin,xmax,xstep,ymin,ymax,ystep,
          lbldata,
          cor,tamanho,ordem,alpha,estilo,marker,
          figura)




# graficar(x_analitycal,sttA_analitycal,titulo,eixox,eixoy,
#           xmin,xmax,xstep,ymin,ymax,ystep,
#           lbldata,
#           cor,tamanho,ordem,alpha,estilo,marker,
#           figura)

# lbldata     = 'Numerical Solution [6] '
# cor         = 'g'
# tamanho     = 1.5
# ordem       = 1
# alpha       = 1
# estilo      = 'solid'
# marker      = "x"

# graficar(x_numerical,sttA_numerical,titulo,eixox,eixoy,
#           xmin,xmax,xstep,ymin,ymax,ystep,
#           lbldata,
#           cor,tamanho,ordem,alpha,estilo,marker,
#           figura)

# lbldata     = 'Analytical Solution [37]'
# cor         = 'k'
# tamanho     = 1.5
# ordem       = 1
# alpha       = 1
# estilo      = 'solid'
# marker      = "^"

# graficar(x_Ling,sttA_Ling,titulo,eixox,eixoy,
#           xmin,xmax,xstep,ymin,ymax,ystep,
#           lbldata,
#           cor,tamanho,ordem,alpha,estilo,marker,
#           figura)

# lbldata     = 'Single Tunnel'
# cor         = 'k'
# tamanho     = 1.5
# ordem       = 1
# alpha       = 1
# estilo      = 'dashed'
# marker      = ""

# graficar([1.25,5.0],[2,2],titulo,eixox,eixoy,
#           xmin,xmax,xstep,ymin,ymax,ystep,
#           lbldata,
#           cor,tamanho,ordem,alpha,estilo,marker,
#           figura)


figura      = 2
titulo      = 'Relationship between Convergence in B and A'
eixoy       = r'$U_B/U_A$'
eixox       = r'$d_1/2R_t$'
xmin        = 1.25
xmax        = 5
xstep       = 0.25
ymin        = 0
ymax        = 1.5
ystep       = 0.25

lbldata     = '3D F.E. Solution'
cor         = 'r'
tamanho     = 1.5
ordem       = 1
alpha       = 1
estilo      = 'solid'
marker      = "D"

graficar(x,UB/UA,titulo,eixox,eixoy,
          xmin,xmax,xstep,ymin,ymax,ystep,
          lbldata,
          cor,tamanho,ordem,alpha,estilo,marker,
          figura)

lbldata     = 'Single Tunnel'
cor         = 'k'
tamanho     = 1.5
ordem       = 1
alpha       = 1
estilo      = 'dashed'
marker      = ""

graficar([0,5.0],[1,1],titulo,eixox,eixoy,
          xmin,xmax,xstep,ymin,ymax,ystep,
          lbldata,
          cor,tamanho,ordem,alpha,estilo,marker,
          figura)