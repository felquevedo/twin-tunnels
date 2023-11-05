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
    plt.figure(figura,figsize = (6,6))
    
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
        plt.plot(x,y_espelhado, color=cor, lw = tamanho)
    
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


#%% DEFORMATION OF SECTION
modelo      = 'ETESTE'
arquivox     = modelo + '\convergencias_x.txt'
arquivoy     = modelo + '\convergencias_y.txt'
titulo = "Deformada da seção"
xmin = -1.1
xmax = 1.1
ymin = -1.1
ymax = 1.1
lblcoluna = '$d_1 = 16R_e$ - LP'
ncoluna     = 85

apenasdeformada = False
figura = 1
cor = "k"
tamanho = 2
ordem = 1
alpha = 1
estilo = "dashed"
escala = 20

graficar_secao_deformada(arquivox, arquivoy,                
                             titulo,                            
                             xmin,xmax,                        
                             ymin,ymax,                         
                             ncoluna,                           
                             lblcoluna,                         
                             cor,tamanho,ordem,alpha,estilo,    
                             figura)