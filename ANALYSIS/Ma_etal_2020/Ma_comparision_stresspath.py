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
    fig = plt.figure(figura,figsize = (4.5,5))    
    
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
             fillstyle = 'full')

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
    


#%% #.  STRESS IN PATH 1
""" ********************************************
STRESS IN PATH 1
******************************************** """ 

# Ler arquivo txt e guarda em um array
file_path = 'MA_SigmaRR_theta45.txt'
data_array = np.loadtxt(file_path)

# Separa os dados em x e y
x = data_array[:,0]
y = data_array[:,1]

figura      = 1
titulo      = 'MA_sigmaRR_sigmaTT_theta45'
eixoy       = r'$\sigma_{ii}$ [MPa]'
eixox       = r'$r$ [m], $\theta = 45^\circ$'
xmin        = 1.0
xmax        = 3.5
xstep       = 0.5
ymin        = 0
ymax        = 100
ystep       = 10

lbldata     = r'$\sigma_{rr}$ Analytical Solution [9]'
cor         = 'r'
tamanho     = 2
ordem       = 2
alpha       = 1
estilo      = 'solid'
marker      = "v"

graficar(x,y,titulo,eixox,eixoy,
          xmin,xmax,xstep,ymin,ymax,ystep,
          lbldata,
          cor,tamanho,ordem,alpha,estilo,marker,
          figura)



# Ler arquivo txt e guarda em um array
file_path = 'MA_C50_FI30_D1_5_SIGMAV_30_SIGMAH_40/stressx_zf_45.txt'
data_array = np.loadtxt(file_path)

# Separa os dados em x e y
x = data_array[:,1]
y = -data_array[:,-1]

lbldata     = r'$\sigma_{rr}$ 3D F.E. Solution'
cor         = 'k'
tamanho     = 1
ordem       = 2
alpha       = 1
estilo      = 'solid'
marker      = "+"

graficar(x,y,titulo,eixox,eixoy,
          xmin,xmax,xstep,ymin,ymax,ystep,
          lbldata,
          cor,tamanho,ordem,alpha,estilo,marker,
          figura)


# Ler arquivo txt e guarda em um array
file_path = 'MA_SigmaTT_theta45.txt'
data_array = np.loadtxt(file_path)

# Separa os dados em x e y
x = data_array[:,0]
y = data_array[:,1]


lbldata     = r'$\sigma_{\theta \theta}$ Analytical Solution [9]'
cor         = 'orange'
tamanho     = 2
ordem       = 1
alpha       = 1
estilo      = 'solid'
marker      = "s"

graficar(x,y,titulo,eixox,eixoy,
          xmin,xmax,xstep,ymin,ymax,ystep,
          lbldata,
          cor,tamanho,ordem,alpha,estilo,marker,
          figura)



# Ler arquivo txt e guarda em um array
file_path = 'MA_C50_FI30_D1_5_SIGMAV_30_SIGMAH_40/stressy_zf_45.txt'
data_array = np.loadtxt(file_path)

# Separa os dados em x e y
x = data_array[:,1]
y = -data_array[:,-1]

lbldata     = r'$\sigma_{\theta \theta}$ 3D F.E. Solution'
cor         = 'b'
tamanho     = 1
ordem       = 2
alpha       = 1
estilo      = 'solid'
marker      = "x"

graficar(x,y,titulo,eixox,eixoy,
          xmin,xmax,xstep,ymin,ymax,ystep,
          lbldata,
          cor,tamanho,ordem,alpha,estilo,marker,
          figura)




#%% #.  STRESS IN PATH 2
""" ********************************************
STRESS IN PATH 2
******************************************** """ 

# Ler arquivo txt e guarda em um array
file_path = 'MA_SigmaRR_theta90.txt'
data_array = np.loadtxt(file_path)

# Separa os dados em x e y
x = data_array[:,0]
y = data_array[:,1]

figura      = 2
titulo      = 'MA_sigmaRR_sigmaTT_theta90'
eixoy       = r'$\sigma_{ii}$ [MPa]'
eixox       = r'$r$ [m], $\theta = 90^\circ$'
xmin        = 1.0
xmax        = 3.5
xstep       = 0.5
ymin        = 0
ymax        = 100
ystep       = 10

lbldata     = r'$\sigma_{rr}$ Analytical Solution [9]'
cor         = 'r'
tamanho     = 2
ordem       = 2
alpha       = 1
estilo      = 'solid'
marker      = "v"

graficar(x,y,titulo,eixox,eixoy,
          xmin,xmax,xstep,ymin,ymax,ystep,
          lbldata,
          cor,tamanho,ordem,alpha,estilo,marker,
          figura)



# Ler arquivo txt e guarda em um array
file_path = 'MA_C50_FI30_D1_5_SIGMAV_30_SIGMAH_40/stressx_zf_90.txt'
data_array = np.loadtxt(file_path)

# Separa os dados em x e y
x = data_array[:,1]
y = -data_array[:,-1]

lbldata     = r'$\sigma_{rr}$ 3D F.E. Solution'
cor         = 'k'
tamanho     = 1
ordem       = 2
alpha       = 1
estilo      = 'solid'
marker      = "+"

graficar(x,y,titulo,eixox,eixoy,
          xmin,xmax,xstep,ymin,ymax,ystep,
          lbldata,
          cor,tamanho,ordem,alpha,estilo,marker,
          figura)


# Ler arquivo txt e guarda em um array
file_path = 'MA_SigmaTT_theta90.txt'
data_array = np.loadtxt(file_path)

# Separa os dados em x e y
x = data_array[:,0]
y = data_array[:,1]

lbldata     = r'$\sigma_{\theta \theta}$ Analytical Solution [9]'
cor         = 'orange'
tamanho     = 2
ordem       = 1
alpha       = 1
estilo      = 'solid'
marker      = "s"

graficar(x,y,titulo,eixox,eixoy,
          xmin,xmax,xstep,ymin,ymax,ystep,
          lbldata,
          cor,tamanho,ordem,alpha,estilo,marker,
          figura)



# Ler arquivo txt e guarda em um array
file_path = 'MA_C50_FI30_D1_5_SIGMAV_30_SIGMAH_40/stressy_zf_90.txt'
data_array = np.loadtxt(file_path)

# Separa os dados em x e y
x = data_array[:,1]
y = -data_array[:,-1]

lbldata     = r'$\sigma_{\theta \theta}$ 3D F.E. Solution'
cor         = 'b'
tamanho     = 1
ordem       = 2
alpha       = 1
estilo      = 'solid'
marker      = "x"

graficar(x,y,titulo,eixox,eixoy,
          xmin,xmax,xstep,ymin,ymax,ystep,
          lbldata,
          cor,tamanho,ordem,alpha,estilo,marker,
          figura)



#%% #.  STRESS IN PATH 3
""" ********************************************
STRESS IN PATH 3
******************************************** """ 

# Ler arquivo txt e guarda em um array
file_path = 'MA_SigmaRR_theta135.txt'
data_array = np.loadtxt(file_path)

# Separa os dados em x e y
x = data_array[:,0]
y = data_array[:,1]

figura      = 3
titulo      = 'MA_sigmaRR_sigmaTT_theta135'
eixoy       = r'$\sigma_{ii}$ [MPa]'
eixox       = r'$r$ [m], $\theta = 135^\circ$'
xmin        = 1.0
xmax        = 3.5
xstep       = 0.5
ymin        = 0
ymax        = 100
ystep       = 10

lbldata     = r'$\sigma_{rr}$ Analytical Solution [9]'
cor         = 'r'
tamanho     = 2
ordem       = 2
alpha       = 1
estilo      = 'solid'
marker      = "v"

graficar(x,y,titulo,eixox,eixoy,
          xmin,xmax,xstep,ymin,ymax,ystep,
          lbldata,
          cor,tamanho,ordem,alpha,estilo,marker,
          figura)



# Ler arquivo txt e guarda em um array
file_path = 'MA_C50_FI30_D1_5_SIGMAV_30_SIGMAH_40/stressx_zf_135.txt'
data_array = np.loadtxt(file_path)

# Separa os dados em x e y
x = data_array[:,1]
y = -data_array[:,-1]

lbldata     = r'$\sigma_{rr}$ 3D F.E. Solution'
cor         = 'k'
tamanho     = 1
ordem       = 2
alpha       = 1
estilo      = 'solid'
marker      = "+"

graficar(x,y,titulo,eixox,eixoy,
          xmin,xmax,xstep,ymin,ymax,ystep,
          lbldata,
          cor,tamanho,ordem,alpha,estilo,marker,
          figura)


# Ler arquivo txt e guarda em um array
file_path = 'MA_SigmaTT_theta135.txt'
data_array = np.loadtxt(file_path)

# Separa os dados em x e y
x = data_array[:,0]
y = data_array[:,1]

lbldata     = r'$\sigma_{\theta \theta}$ Analytical Solution [9]'
cor         = 'orange'
tamanho     = 2
ordem       = 1
alpha       = 1
estilo      = 'solid'
marker      = "s"

graficar(x,y,titulo,eixox,eixoy,
          xmin,xmax,xstep,ymin,ymax,ystep,
          lbldata,
          cor,tamanho,ordem,alpha,estilo,marker,
          figura)



# Ler arquivo txt e guarda em um array
file_path = 'MA_C50_FI30_D1_5_SIGMAV_30_SIGMAH_40/stressy_zf_135.txt'
data_array = np.loadtxt(file_path)

# Separa os dados em x e y
x = data_array[:,1]
y = -data_array[:,-1]

lbldata     = r'$\sigma_{\theta \theta}$ 3D F.E. Solution'
cor         = 'b'
tamanho     = 1
ordem       = 2
alpha       = 1
estilo      = 'solid'
marker      = "x"

graficar(x,y,titulo,eixox,eixoy,
          xmin,xmax,xstep,ymin,ymax,ystep,
          lbldata,
          cor,tamanho,ordem,alpha,estilo,marker,
          figura)