import svgutils.compose as sc
from IPython.display import SVG
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


def anotar(titulo, coords, texts, styles, cores, xytexts):

    # drawing a random figure on top of your SVG
    fig, ax = plt.subplots(1, figsize=(9,5))
    
    # Definir a fonte Times New Roman
    font = FontProperties()
    font.set_name('Times')
    
    ax.axis('off')
    ax.set_frame_on(False)
    ax.invert_yaxis() 
    
    for (x, y), text, style, cor,xytext in zip(coords, texts, styles, cores,xytexts):
        ax.annotate(
            text,
            xy=(x, y),  # Coordenadas da anotação
            textcoords='offset points',
            xytext = xytext,
            arrowprops=dict(arrowstyle="-",
                            connectionstyle=style),
            bbox=dict(boxstyle="round,pad=0.1", edgecolor='black', facecolor='white', alpha=1),
            fontsize=12,
            fontname='Times New Roman',
            fontweight='bold',
            color=cor
            ) 
    
    fig.savefig('cover.svg', transparent=True)
    plt.close(fig)
    
    sc.Figure("648","360", 
        sc.Panel(sc.SVG("./" + titulo + ".svg").scale(1).move(0,0)),
        sc.Panel(sc.SVG("cover.svg"))
        ).save(titulo + "_anotate.svg")
    SVG(titulo + '_anotate.svg')

    display(SVG(filename=titulo + '_anotate.svg'))

# Dimensões da imagem no inkscape
L1 = 33
A1 = 1.5


#%% #. CONVERGENCE PROFILES - CG_CP_LP - D1=16Re
""" ********************************************
CONVERGENCE PROFILES - CG_CP_LP - D1=16Re
******************************************** """ 
# Adicionar anotações
coords = [(11.2/L1, (A1-1.33)/A1), (11.2/L1, (A1-1.06)/A1), (11.2/L1, (A1-0.94)/A1), (11.2/L1, (A1-0.83)/A1),
          (11.2/L1, (A1-1.07)/A1), (11.2/L1, (A1-1.01)/A1), (11.2/L1, (A1-1.01)/A1), (11.2/L1, (A1-0.84)/A1)]

texts = ['1.33', '1.06', '0.94', '0.83', 
         '1.07', '1.01', '1.01', '0.84']

styles = ['arc', 'arc', 'arc', 'arc', 
          'arc', 'arc', 'arc', 'arc']

cores = ['red', 'red', 'magenta', 'blue', 
         'green', 'green', 'orange', 'magenta']

xytexts =[(50, 10), (50, 40), (50, -15), (35, -30),
          (-60, 50), (-60, 10), (-60, -30), (-60, -35)]

titulo = 'Convergence Profiles - WG_ST_LT - $d_1=16R_i$'
anotar(titulo, coords, texts, styles, cores, xytexts)


#%% #. CONVERGENCE PROFILES - CG_CP_LP - D1=8Re
""" ********************************************
CONVERGENCE PROFILES - CG_CP_LP - D1=8Re
******************************************** """ 
# Adicionar anotações
coords = [(11.2/L1, (A1-1.322)/A1), (11.2/L1, (A1-1.074)/A1), (11.2/L1, (A1-0.940)/A1), (11.2/L1, (A1-0.842)/A1),
          (11.2/L1, (A1-1.081)/A1), (11.2/L1, (A1-1.027)/A1), (11.2/L1, (A1-1.030)/A1), (11.2/L1, (A1-0.844)/A1)]

texts = ['1.32', '1.07', '0.94', '0.84', 
         '1.08', '1.03', '1.03', '0.84']

styles = ['arc', 'arc', 'arc', 'arc', 
          'arc', 'arc', 'arc', 'arc']

cores = ['red', 'red', 'magenta', 'blue', 
         'green', 'green', 'orange', 'magenta']

xytexts =[(50, 15), (50, 40), (50, -15), (35, -30),
          (-60, 50), (-60, 10), (-60, -30), (-60, -35)]

titulo = 'Convergence Profiles - WG_ST_LT - $d_1=8R_i$'
anotar(titulo, coords, texts, styles, cores, xytexts)

#%% #. CONVERGENCE PROFILES - CG_CP_LP - D1=4Re
""" ********************************************
CONVERGENCE PROFILES - CG_CP_LP - D1=4Re
******************************************** """ 
# Adicionar anotações
coords = [(11.2/L1, (A1-1.408)/A1), (11.2/L1, (A1-1.174)/A1), (11.2/L1, (A1-0.977)/A1), (11.2/L1, (A1-0.889)/A1),
          (11.2/L1, (A1-1.143)/A1), (11.2/L1, (A1-1.100)/A1), (11.2/L1, (A1-1.096)/A1), (11.2/L1, (A1-0.889)/A1)]

texts = ['1.41', '1.17', '0.98', '0.89', 
         '1.14', '1.10', '1.10', '0.89']

styles = ['arc', 'arc', 'arc', 'arc', 
          'arc', 'arc', 'arc', 'arc']

cores = ['red', 'red', 'magenta', 'blue', 
         'green', 'green', 'orange', 'magenta']

xytexts =[(50, 0), (50, 15), (50, -15), (35, -30),
          (-60, 50), (-60, 5), (-60, -35), (-60, -35)]

titulo = 'Convergence Profiles - WG_ST_LT - $d_1=4R_i$'
anotar(titulo, coords, texts, styles, cores, xytexts)

#%% #.  CONVERGENCE PROFILES - MODEL VP_EPVP_CRE_CRVE_CG_LP
""" ********************************************
CONVERGENCE PROFILES - MODEL VP_EPVP_CRE_CRVE_CG_LP
******************************************** """ 
# Adicionar anotações
coords = [(11.2/L1, (A1-1.408)/A1), (11.2/L1, (A1-1.143)/A1), (11.2/L1, (A1-1.071)/A1), (11.2/L1, (A1-0.977)/A1),(11.2/L1, (A1-0.936)/A1),
          (11.2/L1, (A1-1.322)/A1), (11.2/L1, (A1-1.332)/A1), (11.2/L1, (A1-1.081)/A1), (11.2/L1, (A1-0.940)/A1)]

texts = ['1.41', '1.14', '1.07', '0.98', '0.94', 
         '1.32', '1.33', '1.08', '0.94']

styles = ['arc', 'arc', 'arc', 'arc', 'arc', 
          'arc', 'arc', 'arc', 'arc']

cores = ['red', 'red', 'orange', 'red', 'orange' ,
         'green', 'orange', 'green', 'green']

xytexts =[(50, 0), (50, 30), (50, 0), (50, -20),(50, -50),
          (-60, 15), (-60, -10), (-60, -35), (-60, -50)]

titulo = 'Convergence Profiles - VP_EPVP_EL_VEL_WG_LT'
anotar(titulo, coords, texts, styles, cores, xytexts)

#%% #.  CONVERGENCE PROFILES - MODEL EP_CRE_EPVP_CRVE_CG_CP_LP
""" ********************************************
CONVERGENCE PROFILES - MODEL EP_CRE_EPVP_CRVE_CG_CP_LP
******************************************** """ 
# Adicionar anotações
coords = [(11.2/L1, (A1-1.408)/A1), (11.2/L1, (A1-1.174)/A1), (11.2/L1, (A1-1.096)/A1), (11.2/L1, (A1-1.030)/A1),(11.2/L1, (A1-1.005)/A1),
          (11.2/L1, (A1-1.322)/A1), (11.2/L1, (A1-1.332)/A1), (11.2/L1, (A1-1.094)/A1), (11.2/L1, (A1-1.064)/A1)]

texts = ['1.41', '1.74', '1.10', '1.03', '1.01', 
         '1.32', '1.33', '1.09', '1.06']

styles = ['arc', 'arc', 'arc', 'arc', 'arc', 
          'arc', 'arc', 'arc', 'arc']

cores = ['red', 'red', 'red', 'green', 'orange' ,
         'green', 'orange', 'green', 'orange']

xytexts =[(50, 0), (50, 20), (50, 0), (50, -40),(50, -60),
          (-60, 15), (-60, -10), (-60, -45), (-60, -65)]

titulo = 'Convergence Profiles - EP_EL_EPVP_VEL_WG_ST_LT'
anotar(titulo, coords, texts, styles, cores, xytexts)

#%% #.  CONVERGENCE PROFILES - MODEL EP_D1_16RE
""" ********************************************
CONVERGENCE PROFILES - MODEL EP_D1_16RE
******************************************** """ 

# Dimensões da imagem no inkscape
L1 = 33
A1 = 2.5


# Adicionar anotações
coords = [(11.2/L1, (A1-1.63)/A1), (11.2/L1, (A1-1.16)/A1), (11.2/L1, (A1-1.00)/A1)]

texts = ['1.63', '1.16', '1.00']

styles = ['arc', 'arc', 'arc']

cores = ['blue', 'blue', 'blue']

xytexts =[(50, 20), (50, 10), (50, -23)]

titulo = 'Convergence Profiles - EP_d1_16Ri'
anotar(titulo, coords, texts, styles, cores, xytexts)

#%% #.  CONVERGENCE PROFILES - MODEL EP_D1_4RE
""" ********************************************
CONVERGENCE PROFILES - MODEL EP_D1_4RE
******************************************** """ 
# Adicionar anotações
coords = [(11.2/L1, (A1-2.03)/A1), (11.2/L1, (A1-1.28)/A1), (11.2/L1, (A1-1.10)/A1)]

texts = ['2.03', '1.28', '1.10']

styles = ['arc', 'arc', 'arc']

cores = ['blue', 'blue', 'blue']

xytexts =[(50, 20), (50, 30), (50, -33)]

titulo = 'Convergence Profiles - EP_d1_4Ri'
anotar(titulo, coords, texts, styles, cores, xytexts)

#%% #.  CONVERGENCE PROFILES - MODEL EPVP_CRVE_D1_16RE
""" ********************************************
CONVERGENCE PROFILES - MODEL EPVP_CRVE_D1_16RE
******************************************** """
# Adicionar anotações
coords = [(11.2/L1, (A1-1.86)/A1), (11.2/L1, (A1-1.32)/A1)]

texts = ['1.86', '1.32']

styles = ['arc', 'arc']

cores = ['blue', 'blue']

xytexts =[(50, 20), (50, 10)]

titulo = 'Convergence Profiles - EPVP_VEL_d1_16Ri'
anotar(titulo, coords, texts, styles, cores, xytexts)

#%% #.  CONVERGENCE PROFILES - MODEL EPVP_CRVE_D1_4RE
""" ********************************************
CONVERGENCE PROFILES - MODEL EPVP_CRVE_D1_4RE
******************************************** """
# Adicionar anotações
coords = [(11.2/L1, (A1-2.04)/A1), (11.2/L1, (A1-1.39)/A1)]

texts = ['2.04', '1.39']

styles = ['arc', 'arc']

cores = ['blue', 'blue']

xytexts =[(50, 20), (50, 10)]

titulo = 'Convergence Profiles - EPVP_VEL_d1_4Ri'
anotar(titulo, coords, texts, styles, cores, xytexts)

#%% #.  CONVERGENCE PROFILES - MODEL EPVP_CRE_CRVE_D1_16RE
""" ********************************************
CONVERGENCE PROFILES - MODEL EPVP_CRE_CRVE_D1_16RE
******************************************** """ 
# Adicionar anotações
coords = [(11.2/L1, (A1-1.38)/A1), (11.2/L1, (A1-1.08)/A1)]

texts = ['1.38', '1.08']

styles = ['arc', 'arc']

cores = ['blue', 'blue']

xytexts =[(50, 10), (50, 0)]

titulo = 'Convergence Profiles - EPVP_EL_VEL_d1_16Ri'
anotar(titulo, coords, texts, styles, cores, xytexts)

#%% #.  CONVERGENCE PROFILES - MODEL EPVP_CRE_CRVE_D1_4RE
""" ********************************************
CONVERGENCE PROFILES - MODEL EPVP_CRE_CRVE_D1_4RE
******************************************** """ 
# Adicionar anotações
coords = [(11.2/L1, (A1-1.51)/A1), (11.2/L1, (A1-1.15)/A1)]

texts = ['1.51', '1.15']

styles = ['arc', 'arc']

cores = ['blue', 'blue']

xytexts =[(50, 0), (50, -5)]

titulo = 'Convergence Profiles - EPVP_EL_VEL_d1_4Ri'
anotar(titulo, coords, texts, styles, cores, xytexts)



