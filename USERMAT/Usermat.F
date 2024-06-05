*deck,usermat      USERDISTRIB  parallel                                gal
      subroutine usermat(
     &                   matId, elemId,kDomIntPt, kLayer, kSectPt,
     &                   ldstep,isubst,keycut,
     &                   nDirect,nShear,ncomp,nStatev,nProp,
     &                   Time,dTime,Temp,dTemp,
     &                   stress,ustatev,dsdePl,sedEl,sedPl,epseq,
     &                   Strain,dStrain, epsPl, prop, coords, 
     &                   var0, defGrad_t, defGrad,
     &                   tsstif, epsZZ,
     &                   cutFactor, pVolDer, hrmflg, var3, var4,
     &                   var5, var6, var7)
#include "impcom.inc"
c     !**************************************************************************!
c     !** SUBROTINA: USERMAT                                                   **!
c     !**                                                                      **!
c     !** Objetivo: seleciona as subrotinas que atualizam as tensões,          **!
c     !**           variáveis de estado e matriz constitutiva                  **!
c     !**                                                                      **!
c     !** Situação:                                                            **!
c     !**                                                                      **!
c     !**************************************************************************!         
c     !
c     ! OBSERVAÇÕES:
c     ! ------------
c     !      
c     !     - Essa rotina funciona para 3D, EPD e AXI
c     ! 
c     !**************************************************************************! 
c     ! Informações sobre as variáveis                                           !
c     !**************************************************************************! 
c     ! 
c     ! CÓDIGOS:
c     ! --------
c     ! 
c     !     int - inteiro
c     !     dp  - dupla precisão
c     !     sc  - escalar
c     !     ar  - arranjo(número de componentes)
c     !     i   - entrada
c     !     o   - saída
c     !     io  - entrada e saída
c     !     l   - local
c     ! 
c     ! VARIÁVEIS DE ENTRADA:
c     ! ----------------------
c     ! 
c     !  matId      (int,sc,i)               número do material
c     !  elemId     (int,sc,i)               número do elemento
c     !  kDomIntPt  (int,sc,i)               k-ésimo ponto de integração
c     !  kLayer     (int,sc,i)               k-ésima camada
c     !  kSectPt    (int,sc,i)               k-ésimo ponto de integração da seção
c     !  ldstep     (int,sc,i)               número do passo
c     !  isubst     (int,sc,i)               número do subpasso
c     !  nDirect    (int,sc,in)              quantidade de componentes normais
c     !  nShear     (int,sc,in)              quantidade de componentes de cisalhamento
c     !  ncomp      (int,sc,in)              total de componentes (nDirect + nShear)
c     !  nstatev    (int,sc,i)               quantidade de variáveis de estado
c     !  nProp      (int,sc,i)               quantidade de constantes do material
c     !  Temp       (dp,sc,in)               temperatura no inicio do incremento de tempo
c     !  dTemp      (dp,sc,in)               incremento de temperatura
c     !  Time       (dp,sc,in)               tempo no inicio do incremento (t)
c     !  dTime      (dp,sc,in)               incremento de tempo (dt)
c     !  Strain     (dp,ar(ncomp),i)         deformação no inicio do incremento de tempo
c     !  dStrain    (dp,ar(ncomp),i)         incremento de deformação
c     !  prop       (dp,ar(nprop),i)         constantes do material definidas pelo comando TB,USER
c     !  coords     (dp,ar(3),i)             coordenadas
c     !  defGrad_t  (dp,ar(3,3),i)           gradiente de deformação no tempo t
c     !  defGrad    (dp,ar(3,3),i)           gradiente de deformação no tempo t+dt
c     !  hrmflg     (dp,sc,io)               flag que indica análise harmônica (não usada)
c     ! 
c     ! VARIÁVEIS DE ENTRADA E SAIDA:
c     ! ------------------------------
c     !        
c     !  stress     (dp,ar(ncomp),io)        tensão
c     !  ustatev    (dp,ar(nstatev),io)      variaveis de estado do usuario
c     !  sedEl      (dp,sc,io)               trabalho elástico
c     !  sedPl      (dp,sc,io)               trabalho plástico
c     !  epseq      (dp,sc,io)               deformação plástica equivalente
c     !  epsPl      (dp,ar(ncomp),io)        deformação plastica
c     !  var?       (dp,sc,io)               variáveis não utilizadas
c     ! 
c     ! VARIÁVEIS DE SAIDA:
c     ! --------------------
c     ! 
c     !  keycut     (int,sc,io)             inteiro que controla o método bisect/cut (não usada)
c     !                                     (variável que será determinada no controle de solução do ANSYS)
c     !  dsdePl     (dp,ar(ncomp,ncomp),io) matriz constitutiva tangente (ou algoritmica)
c     !  pVolDer    (dp,ar(3),o)            derivada do potencial volumétrico com relação a J (não usada)
c     !                                         pVolDer(1) = dU/dJ
c     !                                         pVolDer(2) = d^2U/dJ^2
c     !                                         pVolDer(3) = d^3U/dJ^3
c     !  tsstif     (dp,ar(2),o)            módulo de rigidez transversal
c     !                                         tsstif(1) - Gxz
c     !                                         tsstif(2) - Gyz
c     !                                         tsstif(1) é também utilizado para calcular rigidez hourglass 
c     !                                         este valor deve ser definido quando elementos de baixa ordem
c     !                                         tais como 181, 182 e 185 com integração uniforme for usada.
c     !  epsZZ      (dp,sc,o)               deformação ZZ para estado plano de tensões (não usada)
c     !  cutFactor  (dp,sc,o)               fator de corte do tamanho do passo (recomendado entre 0 e 1) (não usada)  
c     ! 
c     ! VARIÁVEIS LOCAIS:
c     ! -----------------
c     !  
c     !  modelo     (int,sc,l)              identifica o modelo do material
c     !
c     !**************************************************************************! 
c     ! Informações sobre as componentes e notação de Voigt adotada              !
c     !**************************************************************************! 
c     ! 
c     !  ncomp   6   para 3D  (nshear=3)
c     !  ncomp   4   para EPD e AXI (nShear = 1)
c     ! 
c     !  Vetores de tensão e deformação
c     ! 
c     !      11, 22, 33, 12, 23, 13    para 3D
c     !      11, 22, 33, 12            para EPD e AXI
c     ! 
c     !  Matriz constitutiva 3D
c     !       dsdePl    |  1111   1122   1133   1112   1123   1113 |
c     !       dsdePl    |  2211   2222   2233   2212   2223   2213 |
c     !       dsdePl    |  3311   3322   3333   3312   3323   3313 |
c     !       dsdePl    |  1211   1222   1233   1212   1223   1213 |
c     !       dsdePl    |  2311   2322   2333   2312   2323   2313 |
c     !       dsdePl    |  1311   1322   1333   1312   1323   1313 |
c     !  
c     !   Matriz constitutiva EPD e AXI (11, 22, 33, 12)
c     !       dsdePl    |  1111   1122   1133   1112 |
c     !       dsdePl    |  2211   2222   2233   2212 |
c     !       dsdePl    |  3311   3322   3333   3312 |
c     !       dsdePl    |  1211   1222   1233   1212 |
c     ! 
c     !**************************************************************************! 
c     ! Declaração das variáveis                                                 !
c     !**************************************************************************!  
c     !
      INTEGER          
     &                 matId, elemId,
     &                 kDomIntPt, kLayer, kSectPt,
     &                 ldstep,isubst,keycut,
     &                 nDirect,nShear,ncomp,nStatev,nProp,
     &                 modmat
      DOUBLE PRECISION 
     &                 Time,    dTime,   Temp,    dTemp,
     &                 sedEl,   sedPl,   epseq,   epsZZ, cutFactor
      DOUBLE PRECISION 
     &                 stress  (ncomp  ), ustatev (nStatev),
     &                 dsdePl  (ncomp,ncomp),
     &                 pVolDer (3),
     &                 Strain  (ncomp  ), dStrain (ncomp  ), 
     &                 epsPl   (ncomp  ), prop    (nProp  ), 
     &                 coords  (3),       
     &                 defGrad (3,3),     defGrad_t(3,3),
     &                 tsstif  (2)
      DOUBLE PRECISION hrmflg
c     !
c     !
      DOUBLE PRECISION var0, var1, var2, var3, var4, var5,
     &                 var6, var7
      DATA             var1/0.0d0/
      DATA             var2/0.0d0/
c     !
      EXTERNAL        usermat3d_vm_ansys
      EXTERNAL        usermat3d_elastico
      EXTERNAL        usermat3d_EP
      EXTERNAL        usermat3d_VP
c     ! 
c     !**************************************************************************! 
c     ! Selecionando subrotinas do material                                      !
c     !**************************************************************************! 
c     !
c     ! modmat = 4 - elastoplástico von-Mises bilinear (nativa do ANSYS)
c     ! modmat = 5 - usermat3D_elastico
c     ! modmat = 6 - usermat3D_EP
c     ! modmat = 7 - usermat3D_VP
c     ! modmat = 8 - usermat3D_EPVP
c     ! modmat = 9 - usermat3d_VE_CONCRETO
c     !
      modmat = prop(1)
c     !
      SELECT CASE (modmat)
c     !
      CASE(4) 
              CALL usermat3d_vm_ansys (
     &                   matId, elemId,kDomIntPt, kLayer, kSectPt,
     &                   ldstep,isubst,keycut,
     &                   nDirect,nShear,ncomp,nStatev,nProp,
     &                   Time,dTime,Temp,dTemp,
     &                   stress,ustatev,dsdePl,sedEl,sedPl,epseq,
     &                   Strain,dStrain, epsPl, prop, coords,
     &                   var0, defGrad_t, defGrad,
     &                   tsstif, epsZZ, cutFactor, 
     &                   var1, var2, var3, var4, var5,
     &                   var6, var7) 
      CASE(5)
              CALL usermat3d_elastico (
     &                   matId, elemId,kDomIntPt, kLayer, kSectPt,
     &                   ldstep,isubst,keycut,
     &                   nDirect,nShear,ncomp,nStatev,nProp,
     &                   Time,dTime,Temp,dTemp,
     &                   stress,ustatev,dsdePl,sedEl,sedPl,epseq,
     &                   Strain,dStrain, epsPl, prop, coords, 
     &                   var0, defGrad_t, defGrad,
     &                   tsstif, epsZZ, cutFactor, 
     &                   var1, var2, var3, var4, var5,
     &                   var6, var7)   
      CASE(6)
              CALL usermat3d_EP (
     &                   matId, elemId,kDomIntPt, kLayer, kSectPt,
     &                   ldstep,isubst,keycut,
     &                   nDirect,nShear,ncomp,nStatev,nProp,
     &                   Time,dTime,Temp,dTemp,
     &                   stress,ustatev,dsdePl,sedEl,sedPl,epseq,
     &                   Strain,dStrain, epsPl, prop, coords,
     &                   var0, defGrad_t, defGrad,
     &                   tsstif, epsZZ, cutFactor, 
     &                   var1, var2, var3, var4, var5,
     &                   var6, var7)            
      CASE(7)
              CALL usermat3d_VP (
     &                   matId, elemId,kDomIntPt, kLayer, kSectPt,
     &                   ldstep,isubst,keycut,
     &                   nDirect,nShear,ncomp,nStatev,nProp,
     &                   Time,dTime,Temp,dTemp,
     &                   stress,ustatev,dsdePl,sedEl,sedPl,epseq,
     &                   Strain,dStrain, epsPl, prop, coords,
     &                   var0, defGrad_t, defGrad,
     &                   tsstif, epsZZ, cutFactor, 
     &                   var1, var2, var3, var4, var5,
     &                   var6, var7)  
      CASE(8)
              CALL usermat3d_EPVP (
     &                   matId, elemId,kDomIntPt, kLayer, kSectPt,
     &                   ldstep,isubst,keycut,
     &                   nDirect,nShear,ncomp,nStatev,nProp,
     &                   Time,dTime,Temp,dTemp,
     &                   stress,ustatev,dsdePl,sedEl,sedPl,epseq,
     &                   Strain,dStrain, epsPl, prop, coords,
     &                   var0, defGrad_t, defGrad,
     &                   tsstif, epsZZ, cutFactor, 
     &                   var1, var2, var3, var4, var5,
     &                   var6, var7)  
      CASE(9)
              CALL usermat3d_VE_CONCRETO (
     &                   matId, elemId,kDomIntPt, kLayer, kSectPt,
     &                   ldstep,isubst,keycut,
     &                   nDirect,nShear,ncomp,nStatev,nProp,
     &                   Time,dTime,Temp,dTemp,
     &                   stress,ustatev,dsdePl,sedEl,sedPl,epseq,
     &                   Strain,dStrain, epsPl, prop, coords,
     &                   var0, defGrad_t, defGrad,
     &                   tsstif, epsZZ, cutFactor, 
     &                   var1, var2, var3, var4, var5,
     &                   var6, var7)  
      END SELECT     
      RETURN
      END
c     ! 
c     !
c     !
c     ! --------------------------------------------------------------------------
c     !
c     !
c     !
*deck,usermat3d    USERDISTRIB  parallel                                gal
      SUBROUTINE usermat3d_elastico (
     &                   matId, elemId,kDomIntPt, kLayer, kSectPt,
     &                   ldstep,isubst,keycut,
     &                   nDirect,nShear,ncomp,nStatev,nProp,
     &                   Time,dTime,Temp,dTemp,
     &                   stress,ustatev,dsdePl,sedEl,sedPl,epseq,
     &                   Strain,dStrain, epsPl, prop, coords, 
     &                   var0, defGrad_t, defGrad,
     &                   tsstif, epsZZ, cutFactor, 
     &                   var1, var2, var3, var4, var5,
     &                   var6, var7)
#include "impcom.inc"
c     !**************************************************************************!
c     !** SUBROTINA: USERMAT3D_ELASTICO                                        **!
c     !**                                                                      **!
c     !** Objetivo: atualiza as tensões, variáveis de estado e matriz          **!
c     !**           constitutiva para o modelo constitutivo elástico           **!
c     !**                                                                      **!
c     !** Situação:                                                            **!
c     !**                                                                      **!
c     !**************************************************************************!         
c     ! 
c     !**************************************************************************! 
c     ! Declaração variáveis de entrada e saída da subrotina                     !
c     !**************************************************************************! 
      INTEGER          
     &                 matId, elemId,
     &                 kDomIntPt, kLayer, kSectPt,
     &                 ldstep,isubst,keycut,
     &                 nDirect,nShear,ncomp,nStatev,nProp
      DOUBLE PRECISION 
     &                 Time,    dTime,   Temp,    dTemp,
     &                 sedEl,   sedPl,   epseq,   epsZZ,   cutFactor
      DOUBLE PRECISION 
     &                 stress  (ncomp  ), ustatev (nStatev),
     &                 dsdePl  (ncomp,ncomp),
     &                 Strain  (ncomp  ), dStrain (ncomp  ), 
     &                 epsPl   (ncomp  ), prop    (nProp  ), 
     &                 coords  (3),
     &                 defGrad (3,3),     defGrad_t(3,3),
     &                 tsstif  (2)
      DOUBLE PRECISION var0, var1, var2, var3, var4, var5,
     &                 var6, var7
c     ! 
c     !**************************************************************************! 
c     ! Informações sobre as variáveis locais                                    !
c     !**************************************************************************! 
c     ! i,j           (int,sc,l)               contadores
c     ! stresstrial   (dp,ar(6),l)             tensão tentativa
c     ! dsdeEl        (dp,ar(6,6),l)           matriz constitutiva elastica
c     ! young         (dp,sc,l)                módulo de Young
c     ! posn          (dp,sc,l)                coeficiente de Poisson
c     ! 
c     !**************************************************************************! 
c     ! Declaração das variáveis locais                                          !
c     !**************************************************************************! 
      INTEGER             i, j,ncompgt
      DOUBLE PRECISION    dsdeEl(ncomp,ncomp),
     &                    sigi(ncomp), young, posn, stresstrial(ncomp)
      EXTERNAL            vzero, vmove, get_ElmData, get_ElmInfo
      EXTERNAL            matrizD
c     ! 
c     !**************************************************************************! 
c     ! Entrada de dados                                                         !
c     !**************************************************************************! 
      young    = prop(2)
      posn     = prop(3)
c     ! 
c     !**************************************************************************! 
c     ! Calculo da matriz constitutiva                                           !
c     !**************************************************************************! 
      dsdeEl   = 0.0d0 
      CALL MatrizD(young,posn,ncomp,dsdeEl)
c     ! 
c     !**************************************************************************! 
c     ! Calculo módulo de rigidez transversal para hourglass                     !
c     !**************************************************************************!  
      tsstif(1) = 0.5d0*(young /(1.0d0+posn))
c     !
c     !**************************************************************************! 
c     ! Coletando tensões iniciais                                               !
c     !**************************************************************************! 
      call get_ElmInfo('NCOMP', ncompgt)
      call vzero(sigi(1),ncompgt)
      call get_ElmData ('ISIG', elemId,kDomIntPt, ncompgt, sigi)  
c     !
c     !**************************************************************************! 
c     ! Calculo preditor elástico                                                !
c     !**************************************************************************! 
      stresstrial = 0.0d0
      stresstrial = MATMUL(dsdeEl(1:ncomp,1:ncomp),
     &              strain(1:ncomp)+dstrain(1:ncomp)) + sigi
c     !
c     !**************************************************************************! 
c     ! Atualizando a tensão e variáveis de estado                               !
c     !**************************************************************************!       
      stress = stresstrial
c     !
c     !**************************************************************************! 
c     ! Atualizando o módulo constitutivo                                        !
c     !**************************************************************************!       
      dsdePl = dsdeEl
c     !
      RETURN
      END
c     !
*deck,usermat3d    USERDISTRIB  parallel                                gal
      subroutine usermat3d_EP (
     &                   matId, elemId,kDomIntPt, kLayer, kSectPt,
     &                   ldstep,isubst,keycut,
     &                   nDirect,nShear,ncomp,nStatev,nProp,
     &                   Time,dTime,Temp,dTemp,
     &                   stress,ustatev,dsdePl,sedEl,sedPl,epseq,
     &                   Strain,dStrain, epsPl, prop, coords, 
     &                   var0, defGrad_t, defGrad,
     &                   tsstif, epsZZ, cutFactor, 
     &                   var1, var2, var3, var4, var5,
     &                   var6, var7)
#include "impcom.inc"  
c     !**************************************************************************!
c     !** SUBROTINA: USERMAT3D_EP                                              **!
c     !**                                                                      **!
c     !** Objetivo: atualiza as tensões, variáveis de estado e matriz          **!
c     !**           constitutiva para o modelo constitutivo elastoplastico     **!
c     !**                                                                      **!
c     !** Situação:                                                            **!
c     !**                                                                      **!
c     !**************************************************************************!         
c     ! 
c     !**************************************************************************! 
c     ! Declaração variáveis de entrada e saída da subrotina                     !
c     !**************************************************************************! 
      INTEGER          
     &                 matId, elemId,
     &                 kDomIntPt, kLayer, kSectPt,
     &                 ldstep,isubst,keycut,
     &                 nDirect,nShear,ncomp,nStatev,nProp
      DOUBLE PRECISION 
     &                 Time,    dTime,   Temp,    dTemp,
     &                 sedEl,   sedPl,   epseq,   epsZZ,   cutFactor
      DOUBLE PRECISION 
     &                 stress  (ncomp  ), ustatev (nStatev),
     &                 dsdePl  (ncomp,ncomp),
     &                 Strain  (ncomp  ), dStrain (ncomp  ), 
     &                 epsPl   (ncomp  ), prop    (nProp  ), 
     &                 coords  (3),
     &                 defGrad (3,3),     defGrad_t(3,3),
     &                 tsstif  (2)
      DOUBLE PRECISION var0, var1, var2, var3, var4, var5,
     &                 var6, var7
c     ! 
c     !**************************************************************************! 
c     ! Informações sobre as variáveis locais                                    !
c     !**************************************************************************! 
c     ! c             (dp,sc,l)                coesão
c     ! c1,c2,c3      (dp,sc,l)                magnitudes das componentes do vetor de fluxo
c     ! cp,ci,cr      (dp,sc,l)                coesão inicial, pico e residual
c     ! czao          (dp,sc,l)                constante para o calculo da deformação plástica equivalente
c     ! dalg          (int,sc,l)               1 - calcula módulo consistente, 0 - não calcula
c     ! ddlam         (dp,sc,l)                incremento de dlam pelo NR do corretor plástico
c     ! dfds          (dp,ar(ncomp),l)         derivada da função de escoamento em relação às tensões
c     ! dfds_m        (dp,ar(1,ncomp),l)       df/ds^T em forma de matriz para aplicar MATMUL
c     ! dgds          (dp,ar(ncomp),l)         vetor de fluxo
c     ! dgds_m        (dp,ar(ncomp,1),l)       dg/ds em forma de matriz para aplicar MATMUL
c     ! dhdq,dfdq,dfdc,dcde (dp,sc,l)          dh/dq, df/dq, df/dc, dc/de para o endurecimento/amolecimento
c     ! dlam          (dp,sc,l)                incremento da magnitude da deformação plástica
c     ! depsEP        (dp,ar(ncomp),l)         incremento de deformações plásticas
c     ! depsEPeq      (dp,sc,l)                incremento de deformação plástica equivalente 
c     ! DgftD         (dp,ar(ncomp,ncomp),l)   produto D*dg/ds*df/ds^T*D
c     ! dsdeEl        (dp,ar(ncomp,ncomp),l)   matriz constitutiva elastica
c     ! dsdeElinv     (dp,ar(ncomp,ncomp),l)   inversa da matriz constitutiva elastica
c     ! eps1,eps2,eps3(dp,sc,l)                deformações plásticas equivalentes limites 
c     ! epsEP         (dp,ar(ncomp),l)         deformações plásticas
c     ! epsEPeq       (dp,sc,l)                deformação plástica equivalente
c     ! f             (dp,sc,l)                função de escoamento
c     ! fi            (dp,sc,l)                ângulo de atrito 
c     ! ftDg          (dp,sc,l)                produto df/ds^T*D*dg/ds
c     ! g1,g2,g3      (dp,ar(ncomp),l)         componentes diretoras do vetor de fluxo
c     ! i,j,k         (int,sc,l)               contadores
c     ! I1            (dp,sc,l)                primeiro invariante das tensões
c     ! J2            (dp,sc,l)                segundo invariante do desviador
c     ! J3            (dp,sc,l)                terceiro invariante do desviador
c     ! ncompgt       (int,sc,l)               componentes de tensões iniciais
c     ! nrmax         (int,sc,l)               quantidade máxima de interações de NR
c     ! psi           (dp,sc,l)                ângulo de dilatância
c     ! s             (dp,ar(ncomp),l)         tensor desviador
c     ! sigi          (dp,ar(ncomp),l)         tensão inicial
c     ! stressn       (dp,ar(ncomp),l)         tensão no inicio do passo
c     ! stresstrial   (dp,ar(ncomp),l)         tensão tentativa
c     ! theta         (dp,sc,l)                angulo de Lode
c     ! young         (dp,sc,l)                módulo de Young
c     ! posn          (dp,sc,l)                coeficiente de Poisson
c     ! q1,dq         (dp,sc,l)                variaveis auxiliares
c     ! superficief   (int,sc,l)               identifica a função de escoamento: 1-VM, 2-DP, 3-TR, 4-MC
c     ! superficieg   (int,sc,l)               identifica a função potencial: 1-VM, 2-DP, 3-TR, 4-MC
c     ! vPi           (dp,sc,l)                Pi
c     ! 
c     ! 
c     !**************************************************************************! 
c     ! INFORMAÇÕES DAS VARIÁVEIS DE ESTADO                                      !
c     !**************************************************************************!
c     !
c     !   nstatev    = 20 
c     !   ustatev(1) = epsEPeq
c     !   ustatev(2) = dlam
c     !   ustatev(3) = c
c     !   ustatev(3) = q
c     !   ustatev(3) = f
c     !   ustatev(6:ncomp) = epsEP(1:ncomp)
c     !   ustatev(12:ncomp) = stress(1:ncomp)
c     !
c     ! OBS: as variáveis de estados podem ser plotadas na GUI do ANSYS
c     ! utilizando o comando PLESOL,SVAR,[componente] ou PLNESOL,SVAR,[componente]
c     !  
c     !**************************************************************************! 
c     ! Declaração das variáveis locais                                          !
c     !**************************************************************************! 
      INTEGER 
     &                i, j, k, nrmax, ncompgt, dalg         
      DOUBLE PRECISION
     &                vPi,tolEP,
     &                I1,J2,J3,theta,
     &                c1,c2,c3,
     &                f,
     &                dlam,ddlam,ftDg,
     &                dhdq,dfdq,dqdc,dcde,              
     &                epsEPeq,depsEPeq,czao,
     &                q,dq,Xi
      DOUBLE PRECISION
     &                dstress(ncomp),sigi(ncomp),
     &                dsdeEl(ncomp,ncomp),dsdeElinv(ncomp,ncomp),
     &                s(ncomp),
     &                g1(ncomp),g2(ncomp),g3(ncomp),
     &                stresstrial(ncomp),
     &                dgds(ncomp),dfds(ncomp),
     &                dfds_m(1,ncomp),dgds_m(ncomp,1),
     &                epsEP(ncomp),depsEP(ncomp),
     &                DgftD(ncomp,ncomp),
     &                stressn(ncomp)
      INTEGER         
     &                superficief,superficieg   
      DOUBLE PRECISION
     &                young,posn,c,fi,psi,ci,cp,cr,eps1,eps2,eps3
      PARAMETER           (nrmax = 100000,
     &                     vPi = 3.14159265358979323846d0,
     &                     tolEP = 0.0000000000001d0
     &                    )   
      EXTERNAL        
     &                vzero, vmove, get_ElmData, get_ElmInfo,
     &                matrizD,invars,yield,c1c2c3,g1g2g3,
     &                calcula_Xi,calcula_dcde,
     &                matinv,normatensor,calcula_czao
c     ! 
c     !**************************************************************************! 
c     ! Entrada de dados                                                         !
c     !**************************************************************************! 
c     !
c     ! Variavel que controla o método da bisseção caso não haja convergência
      keycut      = 0
c     !
c     ! Propriedades elásticas
      young       = prop(2)
      posn        = prop(3)
c     !
c     ! Propriedades do modelo EP
      superficief = prop(4)
      superficieg = prop(5)
      fi          = prop(6)*vPi/180
      psi         = prop(7)*vPi/180
      ci          = prop(8)
      cp          = prop(9)
      cr          = prop(10)
      eps1        = prop(11)
      eps2        = prop(12)
      eps3        = prop(13)
      dalg        = prop(14)
c     !
c     ! Limpando variáveis
      depsEP      = 0.0d0
      depsEPeq    = 0.0d0
      dq          = 0.0d0
      f           = 0.0d0
      stressn     = 0.0d0
      dcde        = 0.0d0
      k           = 0
c     !
c     !**************************************************************************! 
c     ! Coletando variáveis de estado e deformações plásticas do passo convergido!
c     !**************************************************************************! 
      epsEPeq = ustatev(1)
      dlam    = ustatev(2)
      c       = ustatev(3)
      q       = ustatev(4)
      CALL vmove(ustatev(6), epsEP(1), ncomp)
c     !
c     ! Inicializa o valor da coesão
      IF(c.EQ.0.0d0)c=ci
      IF(q.EQ.0.0d0)THEN
          CALL calcula_Xi(superficief,fi,Xi)
          q=Xi*ci
      ENDIF
c     ! 
c     !**************************************************************************! 
c     ! Calculo da matriz constitutiva                                           !
c     !**************************************************************************! 
      dsdeEl      = 0.0d0
      CALL MatrizD(young,posn,ncomp,dsdeEl)
c     ! 
c     !**************************************************************************! 
c     ! Calculo módulo de rigidez transversal para hourglass                     !
c     !**************************************************************************!  
      tsstif(1) = 0.5d0*(young /(1.0d0+posn))
c     !
c     !**************************************************************************! 
c     ! Coletando tensões iniciais                                               !
c     !**************************************************************************! 
      call get_ElmInfo('NCOMP', ncompgt)
      call vzero(sigi(1),ncompgt)
      call get_ElmData ('ISIG', elemId,kDomIntPt, ncompgt, sigi)  
c     !
c     !**************************************************************************! 
c     ! Calculo preditor elástico                                                !
c     !**************************************************************************! 
      stresstrial = 0.0d0
      stresstrial = MATMUL(dsdeEl(1:ncomp,1:ncomp),
     &              strain(1:ncomp)+dstrain(1:ncomp)
     &              -epsEP(1:ncomp)) + sigi
      stress = stresstrial
c     !
c     !**************************************************************************! 
c     ! Atualizando matriz constitutiva                                          !
c     !**************************************************************************! 
      dsdePl = dsdeEl
c     !
c     !**************************************************************************! 
c     ! Calcula função de escoamento                                             !
c     !**************************************************************************!    
      CALL invars(stresstrial,ncomp,I1,J2,J3,theta,s)     ! Invariantes
      CALL yield(superficief,I1,J2,theta,c,fi,f)     ! função de escoamento
c     !
c     !**************************************************************************! 
c     ! Verifica o critério de escoamento                                        !
c     !**************************************************************************! 
      IF(f.GT.tolEP)THEN
c         !
c         ! Aplica o corretor plástico
c         !
c         !**************************************************************************! 
c         ! Calcula dgds                                                             !
c         !**************************************************************************!  
          dgds = 0.0d0
          stressn = stresstrial  
          CALL invars(stressn,ncomp,I1,J2,J3,theta,s)             ! Invariantes do tensor de tensões 
          CALL g1g2g3(s,ncomp,J2,g1,g2,g3)                        ! Direção vetor de fluxo
          CALL c1c2c3(J2,theta,superficieg,psi,c1,c2,c3)     ! componentes vetor de fluxo
          dgds = c1*g1 + c2*g2 + c3*g3      
c         !
c         !**************************************************************************! 
c         ! Calcula dhdq referente ao endurecimento e amolecimento                   !
c         !**************************************************************************! 
          dhdq = 0.0d0
          dfdq = -1.0d0
          CALL calcula_Xi(superficief,fi,Xi)
          dqdc = Xi
          CALL calcula_dcde(ci,cp,cr,eps1,eps2,eps3,epsEPeq,dcde)
          dhdq  = -dfdq*dqdc*dcde
c         !
c         !**************************************************************************! 
c         ! Interações de NR local do modelo constitutivo                            !
c         !**************************************************************************! 
          k = 0
          DO
c             !**************************************************************************! 
c             ! Calculo de ddlamb                                                        !
c             !**************************************************************************!
c             !
c             ! Calcula dfds
              dfds = 0.0d0
              CALL invars(stress,ncomp,I1,J2,J3,theta,s)
              CALL g1g2g3(s,ncomp,J2,g1,g2,g3)
              CALL c1c2c3(J2,theta,superficief,fi,c1,c2,c3)
              dfds    = c1*g1 + c2*g2 + c3*g3
c             !
c             ! Calcula dfdq
              dfdq = -1.0d0
              !
c             ! Calcula denominador de ddlamb
              ftDg    = DOT_PRODUCT(dfds,MATMUL(dsdeEl,dgds))
c             !
c             ! Calcula ddlamb
              ddlam   = f/(ftDg - dfdq*dhdq)
c             !
c             !**************************************************************************! 
c             ! Calculo do corretor plástico                                             !
c             !**************************************************************************!
              dstress = -ddlam*MATMUL(dsdeEl,dgds)
              dq      = -ddlam*(-dhdq)
c             !
c             !**************************************************************************! 
c             ! Incremento das tensões e do dlam                                         !
c             !**************************************************************************!
              stress  = stress + dstress
              c       = c + dq/Xi
              dlam    = dlam + ddlam
              q       = q + dq
              k = k + 1
c             !
c             !**************************************************************************! 
c             ! Calcula deformação plástica equivalente                                  !
c             !**************************************************************************!
              call matinv(ncomp,dsdeEl,dsdeElinv)
              depsEP = depsEP-MATMUL(dsdeElinv,dstress)
c             !
c             !**************************************************************************! 
c             ! Verifica critério de escoamento                                          !
c             !**************************************************************************!
              CALL invars(stress,ncomp,I1,J2,J3,theta,s)           ! Invariantes
              CALL yield(superficief,I1,J2,theta,c,fi,f)      ! função de escoamento
              IF(f.LE.tolEP)EXIT
c             !
c             ! Caso atinja o número de iterações limites, faça a bisseção
              IF(k.EQ.nrmax)THEN
                  keycut = 1
                  RETURN
              ENDIF
          ENDDO  
c         !
c         !**************************************************************************! 
c         ! Atualizando o módulo constitutivo                                        !
c         !**************************************************************************!       
          IF(dalg.EQ.1)THEN
              dfds_m(1,:) = dfds
              dgds_m(:,1) = dgds
              DgftD= MATMUL(MATMUL(MATMUL(dsdeEl,dgds_m),dfds_m),dsdeEl)
              dsdePl = dsdePl - DgftD/(ftDg - dfdq*dhdq)
          ENDIF
c         !
      ELSE
          depsEp = 0.0d0            
      ENDIF
c     !
c     !**************************************************************************! 
c     ! Guardando deformações plásticas totais                                   !
c     !**************************************************************************! 
c     !
c     ! Calcula as deformações plásticas totais
      epsEP = epsEP + depsEP
c     !
      CALL normatensor(epsEP,ncomp,epsEPeq)
      CALL calcula_Czao(superficief,fi,Czao)
      epsEPeq = Czao*epsEPeq
c     !
c     ! Retorna as deformações inelasticas totais e equivalentes (só tem plásticas)
      epsPl = epsEP
      epseq = epsEPeq
c     !
c     ! Calcula o trabalho elástico
      sedEl    = 0.0d0
      sedEl    = 1.0d0/2.0d0*DOT_PRODUCT(stress,strain+dstrain-epsPl)
c     !
c     ! Calcula o trabalho inelástico (só tem plástico)
      CALL normatensor(depsEP,ncomp,depsEPeq)
      CALL calcula_Czao(superficief,fi,Czao)
      depsEPeq = Czao*depsEPeq
      sedPl = sedPl + (q)*depsEPeq
c     !
c     ! Guarda valores nas variáveis de estado
      ustatev(1) = epsEPeq
      ustatev(2) = dlam
      ustatev(3) = c
      ustatev(4) = q
      ustatev(5) = f
      CALL vmove(epsEP(1), ustatev(6), ncomp)
      CALL vmove(stress(1), ustatev(12), ncomp)
c     !
      RETURN
      END
c     ! 
*deck,usermat3d    USERDISTRIB  parallel                                gal      
      subroutine usermat3d_VP (
     &                   matId, elemId,kDomIntPt, kLayer, kSectPt,
     &                   ldstep,isubst,keycut,
     &                   nDirect,nShear,ncomp,nStatev,nProp,
     &                   Time,dTime,Temp,dTemp,
     &                   stress,ustatev,dsdePl,sedEl,sedPl,epseq,
     &                   Strain,dStrain, epsPl, prop, coords, 
     &                   var0, defGrad_t, defGrad,
     &                   tsstif, epsZZ, cutFactor, 
     &                   var1, var2, var3, var4, var5,
     &                   var6, var7)
#include "impcom.inc"  
c     !**************************************************************************!
c     !** SUBROTINA: USERMAT3D_VP                                              **!
c     !**                                                                      **!
c     !** Objetivo: atualiza as tensões, variáveis de estado e matriz          **!
c     !**           constitutiva para o modelo constitutivo elastoplastico     **!
c     !**                                                                      **!
c     !** Situação:                                                            **!
c     !**                                                                      **!
c     !**************************************************************************!         
c     ! 
c     !**************************************************************************! 
c     ! Declaração variáveis de entrada e saída da subrotina                     !
c     !**************************************************************************! 
      INTEGER          
     &                 matId, elemId,
     &                 kDomIntPt, kLayer, kSectPt,
     &                 ldstep,isubst,keycut,
     &                 nDirect,nShear,ncomp,nStatev,nProp
      DOUBLE PRECISION 
     &                 Time,    dTime,   Temp,    dTemp,
     &                 sedEl,   sedPl,   epseq,   epsZZ,   cutFactor
      DOUBLE PRECISION 
     &                 stress  (ncomp  ), ustatev (nStatev),
     &                 dsdePl  (ncomp,ncomp),
     &                 Strain  (ncomp  ), dStrain (ncomp  ), 
     &                 epsPl   (ncomp  ), prop    (nProp  ), 
     &                 coords  (3),
     &                 defGrad (3,3),     defGrad_t(3,3),
     &                 tsstif  (2)
      DOUBLE PRECISION var0, var1, var2, var3, var4, var5,
     &                 var6, var7
c     ! 
c     !**************************************************************************! 
c     ! Informações sobre as variáveis locais                                    !
c     !**************************************************************************! 
c     ! aux1          (dp,sc,l)                denominador no dlambdaVP
c     ! cVP           (dp,sc,l)                coesão do modelo viscoplástio
c     ! c1,c2,c3      (dp,sc,l)                magnitudes das componentes do vetor de fluxo
c     ! czaoVP        (dp,sc,l)                constante para o calculo da deformação viscopástica equivalente
c     ! dgdsVP        (dp,ar(ncomp),l)         vetor de fluxo viscoplástico
c     ! dgdsVP_m      (dp,ar(ncomp,1),l)       dg/ds em forma de matriz para aplicar MATMUL
c     ! dgPHItD       (dp,ar(ncomp,ncomp),l)   produto dg/ds*PHI^T*D
c     ! dlambdaVP     (dp,sc,l)                incremento da magnitude da deformação viscoplástica
c     ! depsVP        (dp,ar(ncomp),l)         incremento de deformações viscoplásticas
c     ! dsdeEl        (dp,ar(ncomp,ncomp),l)   matriz constitutiva elastica
c     ! dt1,dt2       (dp,sc,l)                tempos limites do modelo viscoplástico
c     ! epsVP         (dp,ar(ncomp),l)         deformações viscoplasticas
c     ! epsVPeq       (dp,sc,l)                deformação viscoplástica equivalente
c     ! fVP           (dp,sc,l)                função de escoamento do modelo viscoplástico
c     ! fiVP          (dp,sc,l)                ângulo de atrito do modelo viscoplástico
c     ! g1,g2,g3      (dp,ar(ncomp),l)         componentes diretoras do vetor de fluxo
c     ! I1            (dp,sc,l)                primeiro invariante das tensões
c     ! J2            (dp,sc,l)                segundo invariante do desviador
c     ! J3            (dp,sc,l)                terceiro invariante do desviador
c     ! n,eta,f0      (dp,sc,l)                constantes de ajuste do modelo de Perzyna
c     ! ncompgt       (int,sc,l)               componentes de tensões iniciais
c     ! PHI           (dp,sc,l)                função de sobretensão
c     ! PHItDdeps     (dp,sc,l)                produto PHI^T*D*deps
c     ! PHItDg        (dp,sc,l)                produto dPHI/ds^T*D*dg/ds
c     ! psiVP         (dp,sc,l)                ângulo de dilatância do modelo viscoplástico
c     ! s             (dp,ar(ncomp),l)         tensor desviador
c     ! sigi          (dp,ar(ncomp),l)         tensão inicial
c     ! sigmap        (dp,ar(ncomp),l)         tensão inicial a descontar
c     ! thetaVP       (dp,sc,l)                angulo de Lode do modelo viscoplástico
c     ! young         (dp,sc,l)                módulo de Young
c     ! posn          (dp,sc,l)                coeficiente de Poisson
c     ! superficiefVP (int,sc,l)               identifica a função de escoamento: 1-VM, 2-DP, 3-TR, 4-MC
c     ! superficiegVP (int,sc,l)               identifica a função potencial: 1-VM, 2-DP, 3-TR, 4-MC
c     ! vPi           (dp,sc,l)                Pi
c     ! 
c     !**************************************************************************! 
c     ! INFORMAÇÕES DAS VARIÁVEIS DE ESTADO                                      !
c     !**************************************************************************!
c     !
c     !   nstatev    = 20 
c     !   ustatev(1) = epsVPeq
c     !   ustatev(2) = dt1
c     !   ustatev(3) = dt2
c     !   ustatev(4:ncomp) = epsVP(1:ncomp)
c     !   ustatev(10:ncomp) = stress(1:ncomp)
c     !
c     ! OBS: as variáveis de estados podem ser plotadas na GUI do ANSYS
c     ! utilizando o comando PLESOL,SVAR,[componente] ou PLNESOL,SVAR,[componente]
c     !  
c     !**************************************************************************! 
c     ! Declaração das variáveis locais                                          !
c     !**************************************************************************! 
      INTEGER 
     &                ncompgt         
      DOUBLE PRECISION
     &                vPi,
     &                I1,J2,J3,theta,
     &                c1,c2,c3,
     &                fVP,PHI,
     &                dlambdaVP,PHItDdeps,PHItDg,aux1,
     &                epsVPeq,czaoVP
      DOUBLE PRECISION
     &                dstress(ncomp),sigi(ncomp),
     &                dsdeEl(ncomp,ncomp),
     &                s(ncomp),
     &                g1(ncomp),g2(ncomp),g3(ncomp),
     &                dgdsVP(ncomp),dPHIds(ncomp),
     &                dPHIds_m(1,ncomp),dgdsVP_m(ncomp,1),
     &                epsVP(ncomp),depsVP(ncomp),
     &                dgPHItD(ncomp,ncomp),
     &                sigmap(ncomp),dt1,dt2
      INTEGER         
     &                superficiefVP,superficiegVP   
      DOUBLE PRECISION
     &                young,posn,cVP,fiVP,psiVP,n,eta,f0,thetaVP
      PARAMETER           (
     &                     vPi = 3.14159265358979323846d0
     &                    )   
      EXTERNAL        
     &                vzero, vmove, get_ElmData, get_ElmInfo,
     &                matrizD,invars,yield,c1c2c3,g1g2g3,
     &                normatensor,calcula_czao      
c     ! 
c     !**************************************************************************! 
c     ! Entrada de dados                                                         !
c     !**************************************************************************! 
c     !
c     ! Variavel que controla o método da bisseção caso não haja convergência
      keycut      = 0
c     !
c     ! Propriedades elásticas
      young       = prop(2)
      posn        = prop(3)
c     !
c     ! Propriedades do modelo VP
      superficiefVP = prop(4)
      superficiegVP = prop(5)
      fiVP          = prop(6)*vPi/180
      psiVP         = prop(7)*vPi/180
      cVP           = prop(8)
      n             = prop(9)
      eta           = prop(10)
      f0            = prop(11)
      thetaVP       = prop(12)
c     !
c     ! Limpando variáveis
      depsVP      = 0.0d0
      fVP         = 0.0d0
      dt1         = 0.0d0
      dt2         = 0.0d0
c     !
c     !**************************************************************************! 
c     ! Coletando variáveis de estado e deformações plásticas                    !
c     !**************************************************************************! 
      epsVP       = 0.0d0
      epsVPeq     = 0.0d0
      epsVPeq     = ustatev(1)
      CALL vmove(ustatev(4), epsVP(1), ncomp)
c     ! 
c     !**************************************************************************! 
c     ! Calculo da matriz constitutiva                                           !
c     !**************************************************************************! 
      dsdeEl      = 0.0d0
      CALL MatrizD(young,posn,ncomp,dsdeEl)
      dsdePl = dsdeEl
c     ! 
c     !**************************************************************************! 
c     ! Calculo módulo de rigidez transversal para hourglass                     !
c     !**************************************************************************!  
      tsstif(1) = 0.5d0*(young /(1.0d0+posn))
c     !
c     !**************************************************************************! 
c     ! Coletando tensões iniciais                                               !
c     !**************************************************************************! 
      call get_ElmInfo('NCOMP', ncompgt)
      call vzero(sigi(1),ncompgt)
      call get_ElmData ('ISIG', elemId,kDomIntPt, ncompgt, sigi)  
c     !
c     !**************************************************************************! 
c     ! Calculo da tensão no passo n                                             !
c     !**************************************************************************! 
      stress = MATMUL(dsdeEl(1:ncomp,1:ncomp),
     &        strain(1:ncomp)
     &        -epsVP(1:ncomp))+sigi
c     !
c     !**************************************************************************! 
c     ! Calculo da função de sobretensão                                         !
c     !**************************************************************************!
      PHI = 0.0d0
      CALL invars(stress,ncomp,I1,J2,J3,theta,s)
      CALL yield(superficiefVP,I1,J2,theta,cVP,fiVP,fVP)
      PHI = (fVP/f0)**n
      IF(PHI.LE.0.0d0)PHI = 0.0d0
c     !
c     !**************************************************************************! 
c     ! Calculo dgdsvp                                                           !
c     !**************************************************************************! 
      CALL g1g2g3(s,ncomp,J2,g1,g2,g3)
      CALL c1c2c3(J2,theta,superficiegVP,psiVP,c1,c2,c3)
      dgdsVP = c1*g1 + c2*g2 + c3*g3    
c     !
c     !**************************************************************************! 
c     ! Calculo dPHIds,PHItDg,PHItDdeps,aux1                                     !
c     !**************************************************************************! 
      CALL c1c2c3(J2,theta,superficiefVP,psiVP,c1,c2,c3)
      dPHIds = c1*g1 + c2*g2 + c3*g3
      IF(PHI.LE.0.0d0)dPHIds = 0.0d0
c     !
c     !**************************************************************************! 
c     ! Verificação do incremento de tempo                                       !
c     !**************************************************************************!
c     IF(PHI.GT.0.0d0)THEN
c     dt1 = 4.0d0/3.0d0*eta/PHI*(1.0d0+posn)/young*DSQRT(3.0d0*J2)
c     dt2 = eta*f0/(n*(fVP/f0)**(n-1))*
c    &        (1.0d0+posn)*(1.0d0-2.0d0*posn)/young*
c    &        ((3.0d0-DSIN(fiVP))**2)/
c    &        (3.0d0/4.0d0*(1.0d0-2.0d0*posn)*(3.0d0-DSIN(fiVP))**2+
c    &        6.0d0*(1.0d0+posn)*DSIN(fiVP)**2)     
c     IF(dtime.GT.dt1.OR.dtime.GT.dt2)THEN
c         keycut = 1
c         RETURN
c     ENDIF
c     ENDIF
c
c     !**************************************************************************! 
c     ! Atualização do módulo constitutivo                                       !
c     !**************************************************************************! 
      PHItDg = DOT_PRODUCT(dPHIds,MATMUL(dsdeEl,dgdsVP))
      aux1 = (eta/dtime + thetaVP*PHItDg)
      dPHIds_m(1,:) = dPHIds
      dgdsVP_m(:,1) = dgdsVP
      DgPHItD = MATMUL(MATMUL
     &              (MATMUL(dsdeEl,dgdsVP_m),dPHIds_m),dsdeEl)
      dsdePl = dsdePl - thetaVP*DgPHItD/aux1  
c     !
c     !**************************************************************************! 
c     ! Calculo do p                                                             !
c     !**************************************************************************!     
      sigmap = PHI*MATMUL(dsdeEl(1:ncomp,1:ncomp),
     &        dgdsVP(1:ncomp))/aux1    
c     !         
c     !**************************************************************************! 
c     ! Calculo do incremento de tensão                                          !
c     !**************************************************************************!       
      dstress = MATMUL(dsdePl(1:ncomp,1:ncomp),
     &        dstrain(1:ncomp)) - sigmap 
c     !
      stress = stress + dstress
c     !
c     !**************************************************************************! 
c     ! Calculo da deformação viscoplastica                                      !
c     !**************************************************************************!       
      PHItDdeps = DOT_PRODUCT(dPHIds,MATMUL(dsdeEl,dstrain))
      dlambdaVP = (PHI + thetaVP*PHItDdeps)/aux1
      depsVP = dlambdaVP*dgdsVP      
c     !
c     ! Calcula as deformações viscoplasticas totais
      epsVP = epsVP + depsVP
      CALL normatensor(epsVP,ncomp,epsVPeq)
      CALL calcula_Czao(superficiefVP,fiVP,CzaoVP)
      epsVPeq = CzaoVP*epsVPeq
c     !
c     ! Retorna as deformações inelasticas totais e equivalentes
      epsPl = epsVP
      epseq = epsVPeq
c     !
c     ! Guarda deformação viscoplastica equivalente
      ustatev(1) = epsVPeq
      ustatev(2) = dt1
      ustatev(3) = dt2
c     !
c     ! Guarda deformações viscoplasticas
      CALL vmove(epsVP(1), ustatev(4), ncomp)
c     !
c     ! Guarda tensões
      CALL vmove(stress(1), ustatev(10), ncomp)
c     !
      RETURN
      END
c     !        
*deck,usermat3d    USERDISTRIB  parallel                                gal
      subroutine usermat3d_EPVP (
     &                   matId, elemId,kDomIntPt, kLayer, kSectPt,
     &                   ldstep,isubst,keycut,
     &                   nDirect,nShear,ncomp,nStatev,nProp,
     &                   Time,dTime,Temp,dTemp,
     &                   stress,ustatev,dsdePl,sedEl,sedPl,epseq,
     &                   Strain,dStrain, epsPl, prop, coords, 
     &                   var0, defGrad_t, defGrad,
     &                   tsstif, epsZZ, cutFactor, 
     &                   var1, var2, var3, var4, var5,
     &                   var6, var7)
#include "impcom.inc"  
      !**************************************************************************!
      !** SUBROTINA: USERMAT3D_EPVP                                            **!
      !**                                                                      **!
      !** Objetivo: atualiza as tensões, variáveis de estado e matriz          **!
      !**           constitutiva para o modelo constitutivo EPVP               **!
      !**                                                                      **!
      !** Situação: OK (10/11/2021)                                            **!
      !**                                                                      **!
      !**************************************************************************!         
      ! 
      !**************************************************************************! 
      ! Declaração variáveis de entrada e saída da subrotina                     !
      !**************************************************************************! 
      INTEGER          
     &                 matId, elemId,
     &                 kDomIntPt, kLayer, kSectPt,
     &                 ldstep,isubst,keycut,
     &                 nDirect,nShear,ncomp,nStatev,nProp
      DOUBLE PRECISION 
     &                 Time,    dTime,   Temp,    dTemp,
     &                 sedEl,   sedPl,   epseq,   epsZZ,   cutFactor
      DOUBLE PRECISION 
     &                 stress  (ncomp  ), ustatev (nStatev),
     &                 dsdePl  (ncomp,ncomp),
     &                 Strain  (ncomp  ), dStrain (ncomp  ), 
     &                 epsPl   (ncomp  ), prop    (nProp  ), 
     &                 coords  (3),
     &                 defGrad (3,3),     defGrad_t(3,3),
     &                 tsstif  (2)
      DOUBLE PRECISION var0, var1, var2, var3, var4, var5,
     &                 var6, var7
      ! 
      !**************************************************************************! 
      ! Informações sobre as variáveis locais (precisão, tipo, escopo)           !
      !**************************************************************************!
c     ! aux1          (dp,sc,l)                denominador no dlambdaVP
c     ! c             (dp,sc,l)                coesão
c     ! c1,c2,c3      (dp,sc,l)                magnitudes das componentes do vetor de fluxo
c     ! cp,ci,cr      (dp,sc,l)                coesão inicial, pico e residual
c     ! czao          (dp,sc,l)                constante para o calculo da deformação plástica equivalente
c     ! czaoVP        (dp,sc,l)                constante para o calculo da deformação viscopástica equivalente
c     ! cVP           (dp,sc,l)                coesão do modelo viscoplástio
c     ! ddlam         (dp,sc,l)                incremento de dlam pelo NR do corretor plástico
c     ! dfds          (dp,ar(ncomp),l)         derivada da função de escoamento em relação às tensões
c     ! dfds_m        (dp,ar(1,ncomp),l)       df/ds^T em forma de matriz para aplicar MATMUL
c     ! dgds          (dp,ar(ncomp),l)         vetor de fluxo elastoplástico
c     ! dgdsVP        (dp,ar(ncomp),l)         vetor de fluxo viscoplástico
c     ! dgds_m        (dp,ar(ncomp,1),l)       dg/ds em forma de matriz para aplicar MATMUL
c     ! dgdsVP_m      (dp,ar(ncomp,1),l)       dg/dsVP em forma de matriz para aplicar MATMUL
c     ! dhdq,dfdq,dfdc,dcde (dp,sc,l)          dh/dq, df/dq, df/dc, dc/de para o endurecimento/amolecimento
c     ! dgPHItD       (dp,ar(ncomp,ncomp),l)   produto dg/ds*PHI^T*D
c     ! dlam          (dp,sc,l)                incremento da magnitude da deformação plástica
c     ! dlambdaVP     (dp,sc,l)                incremento da magnitude da deformação viscoplástica
c     ! depsEP        (dp,ar(ncomp),l)         incremento de deformações plásticas
c     ! depsVP        (dp,ar(ncomp),l)         incremento de deformações viscoplásticas
c     ! depsEPeq      (dp,sc,l)                incremento de deformação plástica equivalente 
c     ! DgftD         (dp,ar(ncomp,ncomp),l)   produto D*dg/ds*df/ds^T*D
c     ! dsdeEl        (dp,ar(ncomp,ncomp),l)   matriz constitutiva elastica
c     ! dsdeElinv     (dp,ar(ncomp,ncomp),l)   inversa da matriz constitutiva elastica
c     ! dt1,dt2       (dp,sc,l)                tempos limites do modelo viscoplástico
c     ! eps1,eps2,eps3(dp,sc,l)                deformações plásticas equivalentes limites 
c     ! epsEP         (dp,ar(ncomp),l)         deformações plásticas
c     ! epsVP         (dp,ar(ncomp),l)         deformações viscoplasticas
c     ! epsEPeq       (dp,sc,l)                deformação plástica equivalente
c     ! epsVPeq       (dp,sc,l)                deformação viscoplástica equivalente
c     ! f             (dp,sc,l)                função de escoamento do modelo elastoplástico
c     ! fVP           (dp,sc,l)                função de escoamento do modelo viscoplástico
c     ! fi            (dp,sc,l)                ângulo de atrito
c     ! fiVP          (dp,sc,l)                ângulo de atrito do modelo viscoplástico
c     ! flag          (int,sc,l)               1- DP coincide com as bordas externas MC ou VM circunscreve TR 
c     ! ftDg          (dp,sc,l)                produto df/ds^T*D*dg/ds
c     ! g1,g2,g3      (dp,ar(ncomp),l)         componentes diretoras do vetor de fluxo
c     ! i,j,k         (int,sc,l)               contadores
c     ! I1            (dp,sc,l)                primeiro invariante das tensões
c     ! J2            (dp,sc,l)                segundo invariante do desviador
c     ! J3            (dp,sc,l)                terceiro invariante do desviador
c     ! n,eta,f0      (dp,sc,l)                constantes de ajuste do modelo de Perzyna
c     ! ncompgt       (int,sc,l)               componentes de tensões iniciais
c     ! nrmax         (int,sc,l)               quantidade máxima de interações de NR
c     ! PHI           (dp,sc,l)                função de sobretensão
c     ! PHItDdeps     (dp,sc,l)                produto PHI^T*D*deps
c     ! PHItDg        (dp,sc,l)                produto dPHI/ds^T*D*dg/ds
c     ! psi           (dp,sc,l)                angulo de dilatância
c     ! psiVP         (dp,sc,l)                angulo de dilatância do modelo viscoplástico
c     ! s             (dp,ar(ncomp),l)         tensor desviador
c     ! sigi          (dp,ar(ncomp),l)         tensão inicial
c     ! sigmap        (dp,ar(ncomp),l)         tensão inicial a descontar
c     ! stressn       (dp,ar(ncomp),l)         tensão no inicio do passo
c     ! stresstrial   (dp,ar(ncomp),l)         tensão tentativa
c     ! theta         (dp,sc,l)                ângulo de Lode
c     ! thetaVP       (dp,sc,l)                ângulo de Lode do modelo viscoplástico
c     ! young         (dp,sc,l)                módulo de Young
c     ! posn          (dp,sc,l)                coeficiente de Poisson
c     ! q1,dq         (dp,sc,l)                variaveis auxiliares
c     ! superficief   (int,sc,l)               identifica a função de escoamento: 1-DPI, 2-DPII, 3-DPIII
c     ! superficiefVP (int,sc,l)               identifica a função de escoamento: 1-DPI, 2-DPII, 3-DPIII
c     ! superficiegVP (int,sc,l)               identifica a função potencial: 1-DPI, 2-DPII, 3-DPIII
c     ! superficieg   (int,sc,l)               identifica a função potencial: 1-DPI, 2-DPII, 3-DPIII
c     ! vPi           (dp,sc,l)                Pi
c     ! 
c     !**************************************************************************! 
c     ! INFORMAÇÕES DAS VARIÁVEIS DE ESTADO                                      !
c     !**************************************************************************!
c     !
c     !   nstatev    = 20 
c     !   ustatev(1) = epsEPeq
c     !   ustatev(2) = dlam
c     !   ustatev(3) = c
c     !   ustatev(4) = q
c     !   ustatev(5) = f
c     !   ustatev(6) = epsVPeq
c     !   ustatev(7) = dt1
c     !   ustatev(8) = dt2
c     !   ustatev(9:ncomp) = espEP(1:ncomp)
c     !   ustatev(15:ncomp) = espVP(1:ncomp)
c     !
c     ! OBS: as variáveis de estados podem ser plotadas na GUI do ANSYS
c     ! utilizando o comando PLESOL,SVAR,[componente] ou PLNESOL,SVAR,[componente]
c     ! 
c     !**************************************************************************! 
c     ! Declaração das variáveis locais                                          !
c     !**************************************************************************!
c     !
c     ! Variáveis comuns a ambos modelos
      INTEGER 
     &                i, j, k, ncompgt   
      DOUBLE PRECISION
     &                I1,J2,J3,theta,
     &                c1,c2,c3,
     &                vPi,
     &                dstress(ncomp),sigi(ncomp),
     &                dsdeEl(ncomp,ncomp),
     &                s(ncomp),
     &                g1(ncomp),g2(ncomp),g3(ncomp)
      DOUBLE PRECISION
     &                young,posn
      PARAMETER           (
     &                     vPi = 3.14159265358979323846d0
     &                    )
      EXTERNAL        
     &                vzero, vmove, get_ElmData, get_ElmInfo,
     &                matrizD,invars,normatensor,calcula_czao,  
     &                matinv,yield,c1c2c3,g1g2g3
c     !
c     ! variáveis do modelo viscoplástico
      DOUBLE PRECISION
     &                fVP,PHI,
     &                dlambdaVP,PHItDdeps,PHItDg,aux1,
     &                epsVPeq,depsVPeq,czaoVP
      DOUBLE PRECISION
     &                dgdsVP(ncomp),dPHIds(ncomp),
     &                dPHIds_m(1,ncomp),dgdsVP_m(ncomp,1),
     &                epsVP(ncomp),depsVP(ncomp),
     &                dgPHItD(ncomp,ncomp),
     &                sigmap(ncomp),dt1,dt2
      INTEGER         
     &                superficiefVP,superficiegVP   
      DOUBLE PRECISION
     &                cVP,fiVP,psiVP,n,eta,f0,thetaVP  
c     !
c     ! variáveis do modelo elastoplástico
      INTEGER 
     &                nrmax, dalg        
      DOUBLE PRECISION
     &                tolEP,
     &                f,
     &                dlam,ddlam,ftDg,
     &                dhdq,dfdq,dqdc,dcde,              
     &                epsEPeq,depsEPeq,czao,
     &                q,dq,Xi
      DOUBLE PRECISION
     &                dsdeElinv(ncomp,ncomp),
     &                stresstrial(ncomp),
     &                dgds(ncomp),dfds(ncomp),
     &                dfds_m(1,ncomp),dgds_m(ncomp,1),
     &                epsEP(ncomp),depsEP(ncomp),
     &                DgftD(ncomp,ncomp),
     &                stressn(ncomp)
      INTEGER         
     &                superficief,superficieg   
      DOUBLE PRECISION
     &                c,fi,psi,ci,cp,cr,eps1,eps2,eps3
      PARAMETER           (nrmax = 100000,
     &                     tolEP = 0.0000000000001d0
     &                    )   
      EXTERNAL        
     &                calcula_Xi,calcula_dcde
c     ! 
c     !**************************************************************************! 
c     ! Entrada de dados                                                         !
c     !**************************************************************************! 
c     !
c     ! Variavel que controla o método da bisseção caso não haja convergência
      keycut      = 0
c     !
c     ! Propriedades elásticas
      young       = prop(2)
      posn        = prop(3)
c     !
c     ! Propriedades do modelo EP
      superficief = prop(4)
      superficieg = prop(5)
      fi          = prop(6)*vPi/180
      psi         = prop(7)*vPi/180
      ci          = prop(8)
      cp          = prop(9)
      cr          = prop(10)
      eps1        = prop(11)
      eps2        = prop(12)
      eps3        = prop(13)
      dalg        = prop(14)
c     !
c     ! Propriedades do modelo VP
      superficiefVP = prop(15)
      superficiegVP = prop(16)
      fiVP          = prop(17)*vPi/180
      psiVP         = prop(18)*vPi/180
      cVP           = prop(19)
      n             = prop(20)
      eta           = prop(21)
      f0            = prop(22)
      thetaVP       = prop(23)
c     !
c     ! Limpando variáveis do modelo EP
      depsEP      = 0.0d0
      depsEPeq    = 0.0d0
      dq          = 0.0d0
      f           = 0.0d0
      stressn     = 0.0d0
      dcde        = 0.0d0
      k           = 0
c     !
c     ! Limpando variáveis do modelo VP
      depsVP      = 0.0d0
      fVP         = 0.0d0
      dt1         = 0.0d0
      dt2         = 0.0d0
c     !
c     !**************************************************************************! 
c     ! Coletando variáveis de estado e deformações plásticas do passo convergido!
c     !**************************************************************************! 
c     ! Modelo EP
      epsEPeq = ustatev(1)
      dlam    = ustatev(2)
      c       = ustatev(3)
      q       = ustatev(4)
      CALL vmove(ustatev(9), epsEP(1), ncomp)
c     !
c     ! Inicializa o valor da coesão
      IF(c.EQ.0.0d0)c=ci
      IF(q.EQ.0.0d0)THEN
          CALL calcula_Xi(superficief,fi,Xi)
          q=Xi*ci
      ENDIF
c     !
c     ! Modelo VP
      epsVPeq = ustatev(6)
      CALL vmove(ustatev(15), epsVP(1), ncomp)
c     ! 
c     !**************************************************************************! 
c     ! Calculo da matriz constitutiva                                           !
c     !**************************************************************************! 
      dsdeEl      = 0.0d0
      CALL MatrizD(young,posn,ncomp,dsdeEl)
      dsdePl = dsdeEl
c     !  
c     !**************************************************************************! 
c     ! Calculo módulo de rigidez transversal para hourglass                     !
c     !**************************************************************************!  
      tsstif(1) = 0.5d0*(young /(1.0d0+posn))
c     !
c     !**************************************************************************! 
c     ! Coletando tensões iniciais                                               !
c     !**************************************************************************! 
      call get_ElmInfo('NCOMP', ncompgt)
      call vzero(sigi(1),ncompgt)
      call get_ElmData ('ISIG', elemId,kDomIntPt, ncompgt, sigi)  
c     !
c     !**************************************************************************! 
c     ! Calculo da tensão no passo n                                             !
c     !**************************************************************************!  
      stress = MATMUL(dsdeEl(1:ncomp,1:ncomp),
     &        strain(1:ncomp)
     &        -epsVP(1:ncomp)
     &        -epsEP(1:ncomp))+sigi
c     !
c     !**************************************************************************! 
c     ! Calculo da função de sobretensão                                         !
c     !**************************************************************************!
      PHI = 0.0d0
      CALL invars(stress,ncomp,I1,J2,J3,theta,s)
      CALL yield(superficiefVP,I1,J2,theta,cVP,fiVP,fVP)
      PHI = (fVP/f0)**n
      IF(PHI.LE.0.0d0)PHI = 0.0d0
c     !
c     !**************************************************************************! 
c     ! Calculo dgdsvp                                                           !
c     !**************************************************************************! 
      CALL g1g2g3(s,ncomp,J2,g1,g2,g3)
      CALL c1c2c3(J2,theta,superficiegVP,psiVP,c1,c2,c3)
      dgdsVP = c1*g1 + c2*g2 + c3*g3    
c     !
c     !**************************************************************************! 
c     ! Calculo dPHIds,PHItDg,PHItDdeps,aux1                                     !
c     !**************************************************************************! 
      CALL c1c2c3(J2,theta,superficiefVP,psiVP,c1,c2,c3)
      dPHIds = c1*g1 + c2*g2 + c3*g3
      IF(PHI.LE.0.0d0)dPHIds = 0.0d0
c     !
c     !**************************************************************************! 
c     ! Verificação do incremento de tempo                                       !
c     !**************************************************************************!
c      IF(PHI.GT.0.0d0)THEN
c      dt1 = 4.0d0/3.0d0*eta/PHI*(1.0d0+posn)/young*DSQRT(3.0d0*J2)
c      dt2 = eta*f0/(n*(fVP/f0)**(n-1))*
c     &        (1.0d0+posn)*(1.0d0-2.0d0*posn)/young*
c     &        ((3.0d0-DSIN(fiVP))**2)/
c     &        (3.0d0/4.0d0*(1.0d0-2.0d0*posn)*(3.0d0-DSIN(fiVP))**2+
c     &        6.0d0*(1.0d0+posn)*DSIN(fiVP)**2)
c      IF(dtime.GT.dt1.OR.dtime.GT.dt2)THEN
c          keycut = 1
c          RETURN
c      ENDIF
c      ENDIF
c     !
c     !**************************************************************************! 
c     ! Atualização do módulo constitutivo                                       !
c     !**************************************************************************! 
      PHItDg = DOT_PRODUCT(dPHIds,MATMUL(dsdeEl,dgdsVP))
      aux1 = (eta/dtime + thetaVP*PHItDg)
      dPHIds_m(1,:) = dPHIds
      dgdsVP_m(:,1) = dgdsVP
      DgPHItD = MATMUL(MATMUL
     &              (MATMUL(dsdeEl,dgdsVP_m),dPHIds_m),dsdeEl)
      dsdePl = dsdePl - thetaVP*DgPHItD/aux1  
c     !
c     !**************************************************************************! 
c     ! Calculo do p                                                             !
c     !**************************************************************************!     
      sigmap = PHI*MATMUL(dsdeEl(1:ncomp,1:ncomp),
     &        dgdsVP(1:ncomp))/aux1    
c     !
c     !**************************************************************************! 
c     ! Calculo da deformação viscoplastica                                      !
c     !**************************************************************************!       
      PHItDdeps = DOT_PRODUCT(dPHIds,MATMUL(dsdeEl,dstrain))
      dlambdaVP = (PHI + thetaVP*PHItDdeps)/aux1
      depsVP = dlambdaVP*dgdsVP      
c     !
c     ! Calcula as deformações viscoplasticas totais
      epsVP = epsVP + depsVP
      CALL normatensor(epsVP,ncomp,epsVPeq)
      CALL calcula_Czao(superficiefVP,fiVP,CzaoVP)
      epsVPeq = CzaoVP*epsVPeq
c     !
c     !
c     !**************************************************************************! 
c     ! Calculo preditor elástico                                                !
c     !**************************************************************************! 
      stresstrial = 0.0d0
      stresstrial = MATMUL(dsdeEl(1:ncomp,1:ncomp),
     &              strain(1:ncomp)+dstrain(1:ncomp)
     &              -epsEP(1:ncomp)-epsVP(1:ncomp)) + sigi
      stress = stresstrial
c     !
c     !**************************************************************************! 
c     ! Calcula função de escoamento                                             !
c     !**************************************************************************!    
      CALL invars(stresstrial,ncomp,I1,J2,J3,theta,s)     ! Invariantes
      CALL yield(superficief,I1,J2,theta,c,fi,f)     ! função de escoamento
c     !
c     !**************************************************************************! 
c     ! Verifica o critério de escoamento                                        !
c     !**************************************************************************! 
      IF(f.GT.0.0d0)THEN
c         !
c         ! Aplica o corretor plástico
c         !
c         !**************************************************************************! 
c         ! Calcula dgds                                                             !
c         !**************************************************************************!  
          dgds = 0.0d0
          stressn = stresstrial  
          CALL invars(stressn,ncomp,I1,J2,J3,theta,s)             ! Invariantes do tensor de tensões 
          CALL g1g2g3(s,ncomp,J2,g1,g2,g3)                        ! Direção vetor de fluxo
          CALL c1c2c3(J2,theta,superficieg,psi,c1,c2,c3)     ! componentes vetor de fluxo
          dgds = c1*g1 + c2*g2 + c3*g3      
c         !
c         !**************************************************************************! 
c         ! Calcula dhdq referente ao endurecimento e amolecimento                   !
c         !**************************************************************************! 
          dhdq = 0.0d0
          dfdq = -1.0d0
          CALL calcula_Xi(superficief,fi,Xi)
          dqdc = Xi
          CALL calcula_dcde(ci,cp,cr,eps1,eps2,eps3,epsEPeq,dcde)
          dhdq  = -dfdq*dqdc*dcde
c         !
c         !**************************************************************************! 
c         ! Interações de NR local do modelo constitutivo                            !
c         !**************************************************************************! 
          k = 0
          DO
c             !**************************************************************************! 
c             ! Calculo de ddlamb                                                        !
c             !**************************************************************************!
c             !
c             ! Calcula dfds
              dfds = 0.0d0
              CALL invars(stress,ncomp,I1,J2,J3,theta,s)
              CALL g1g2g3(s,ncomp,J2,g1,g2,g3)
              CALL c1c2c3(J2,theta,superficief,fi,c1,c2,c3)
              dfds    = c1*g1 + c2*g2 + c3*g3
c             !
c             ! Calcula dfdq
              dfdq = -1.0d0
              !
c             ! Calcula denominador de ddlamb
              ftDg    = DOT_PRODUCT(dfds,MATMUL(dsdeEl,dgds))
c             !
c             ! Calcula ddlamb
              ddlam   = f/(ftDg - dfdq*dhdq)
c             !
c             !**************************************************************************! 
c             ! Calculo do corretor plástico                                             !
c             !**************************************************************************!
              dstress = -ddlam*MATMUL(dsdeEl,dgds)
              dq      = -ddlam*(-dhdq)
c             !
c             !**************************************************************************! 
c             ! Incremento das tensões e do dlam                                         !
c             !**************************************************************************!
              stress  = stress + dstress
              c       = c + dq/Xi
              dlam    = dlam + ddlam
              q       = q + dq
              k = k + 1
c             !
c             !**************************************************************************! 
c             ! Calcula deformação plástica equivalente                                  !
c             !**************************************************************************!
              call matinv(ncomp,dsdeEl,dsdeElinv)
              depsEP = depsEP-MATMUL(dsdeElinv,dstress)
c             !
c             !**************************************************************************! 
c             ! Verifica critério de escoamento                                          !
c             !**************************************************************************!
              CALL invars(stress,ncomp,I1,J2,J3,theta,s)           ! Invariantes
              CALL yield(superficief,I1,J2,theta,c,fi,f)      ! função de escoamento
              IF(f.LE.tolEP)EXIT
c             !
c             ! Caso atinja o número de iterações limites, faça a bisseção
              IF(k.EQ.nrmax)THEN
                  keycut = 1
                  RETURN
              ENDIF
          ENDDO  
c         !
c         !**************************************************************************! 
c         ! Atualizando o módulo constitutivo                                        !
c         !**************************************************************************!
          IF(dalg.EQ.1)THEN
              dfds_m(1,:) = dfds
              dgds_m(:,1) = dgds
              DgftD= MATMUL(MATMUL(MATMUL(dsdeEl,dgds_m),dfds_m),dsdeEl)
              dsdePl = dsdePl - DgftD/(ftDg - dfdq*dhdq)
          ENDIF
c         !
      ELSE
          depsEp = 0.0d0            
      ENDIF
c     !
c     !**************************************************************************! 
c     ! Guardando deformações plásticas totais                                   !
c     !**************************************************************************! 
c     !
c     ! Calcula as deformações plásticas totais
      epsEP = epsEP + depsEP
      CALL normatensor(epsEP,ncomp,epsEPeq)
      CALL calcula_Czao(superficief,fi,Czao)
      epsEPeq = Czao*epsEPeq      
c     !
c     ! Retorna as deformações inelasticas totais e equivalentes (só tem plásticas)
      epsPl = epsEP+epsVP
      epseq = epsEPeq+epsVPeq
c     !
c     ! Calcula o trabalho elástico
      sedEl    = 0.0d0
      sedEl    = 1.0d0/2.0d0*
     &           DOT_PRODUCT(stress,strain+dstrain-epsPl-epsVP)
c     !      
c     !
c     ! Calcula o trabalho inelástico (só tem plástico)
      CALL normatensor(depsEP,ncomp,depsEPeq)
      CALL calcula_Czao(superficief,fi,Czao)
      depsEPeq = Czao*depsEPeq
      CALL normatensor(depsVP,ncomp,depsVPeq)
      CALL calcula_Czao(superficief,fi,Czao)
      depsVPeq = Czao*depsVPeq
      sedPl = sedPl + (q)*depsEPeq+depsVPeq
c     !
c     ! Guarda valores nas variáveis de estado
      ustatev(1) = epsEPeq
      ustatev(2) = dlam
      ustatev(3) = c
      ustatev(4) = q
      ustatev(5) = f
      ustatev(6) = epsVPeq
      ustatev(7) = epsEPeq+epsVPeq
      ustatev(8) = dt2
      CALL vmove(epsEP(1), ustatev(9), ncomp)
      CALL vmove(epsVP(1), ustatev(15), ncomp)
c     !
      RETURN      
      END      
      !
c     !
      SUBROUTINE invars(stress,ncomp,I1,J2,J3,theta,s)      
c     !**************************************************************************!
c     !** Subrotina: invars                                                    **!
c     !**                                                                      **!
c     !** Objetivo: calcula os invariantes do tensor de tensões e o tensor     **!
c     !**           desviador. Adaptado de Chen e Han (1998, p.57-72)          **!
c     !**                                                                      **!      
c     !** Situação: (10-11-2021) OK                                            **!
c     !**                                                                      **!
c     !**************************************************************************!   
      IMPLICIT NONE
      DOUBLE PRECISION stress(ncomp)  ! tensões
      INTEGER          ncomp          ! numero de componentes
      DOUBLE PRECISION I1             ! primeiro invariante do tensor de tensões
      DOUBLE PRECISION J2,J3          ! segundo e terceiro invariante do desviador
      DOUBLE PRECISION theta          ! angulo de Lode
      DOUBLE PRECISION s(6)           ! desviador
      DOUBLE PRECISION p,q            ! pressão hidrostática e tensão eq. de vm
      DOUBLE PRECISION sine           ! variavel auxiliar
c     !
c     ! Inicializando variaveis
      I1      = 0.0d0
      J2      = 0.0d0
      p       = 0.0d0
      q       = 0.0d0
      s       = 0.0d0
      J3      = 0.0d0
      theta   = 0.0d0
      sine    = 0.0d0
c     !
c     ! Calculo do I1 (p. 53)
      I1 = stress(1) + stress(2) + stress(3)
c     !
c     ! Calculo do J2 (p. 58)
      J2 = 1/6.0d0*((stress(1)-stress(2))**2+(stress(2)-stress(3))**2+
     &    (stress(3)-stress(1))**2)+
     &    stress(4)**2
c     !
      IF(ncomp.EQ.6)THEN
          J2 = J2 + stress(ncomp-1)**2+stress(ncomp)**2
      ENDIF
c     !
c     ! Calculo do p (p. 57)
      p = 1.0d0/3.0d0*I1
c     !
c     ! Calculo do desviador s (p. 57)
      s(1) = stress(1) - p
      s(2) = stress(2) - p
      s(3) = stress(3) - p
      s(4) = stress(4)
      IF(ncomp.EQ.6)THEN
          s(ncomp-1) = stress(ncomp-1)
          s(ncomp) = stress(ncomp)
      ENDIF
c     !
c     ! Calculo do J3 (p. 58)
      J3 = s(1)*s(2)*s(3)-s(3)*s(4)*s(4) 
      IF(ncomp.EQ.6)THEN
          J3 = J3 -s(1)*s(ncomp-1)*s(ncomp-1)-s(2)*s(ncomp)*s(ncomp)+
     &        2.0d0*s(4)*s(ncomp-1)*s(ncomp)
      ENDIF
c     !
c     ! Calculo do ângulo de Lode (p. 70) e Owen e Hinton (1980, p.229)
      q = DSQRT(3.0d0*J2)
      IF(q < 1.E-7)THEN
          theta = 0.0d0
      ELSE
          sine = -3.0d0*DSQRT(3.0d0)*J3/(2.0d0*DSQRT(J2)**3)
          IF(sine>1.0d0)sine=1.0d0
          IF(sine<-1.0d0)sine=-1.0d0
          theta=DASIN(sine)/3.0d0
      END IF
c     !
      END SUBROUTINE
c     !
      SUBROUTINE g1g2g3(s,ncomp,J2,g1,g2,g3)
c     !**************************************************************************!
c     !** Subrotina: g1g2g3                                                    **!
c     !**                                                                      **!
c     !** Objetivo: calcula as direções do vetor de fluxo. Adaptado de Owen e  **!
c     !**           Hinton (1980, p.231 e 233)                                 **! 
c     !**                                                                      **!      
c     !** Situação: (10-11-2021) OK                                            **!
c     !**                                                                      **!
c     !**************************************************************************!      
      IMPLICIT NONE
      DOUBLE PRECISION s(ncomp)                           ! desviador
      INTEGER          ncomp                              ! numero de componentes 
      DOUBLE PRECISION J2                                 ! segundo invariante do desviador
      DOUBLE PRECISION g1(ncomp), g2(ncomp), g3(ncomp)    ! direções do vetor de fluxo
c     !
c     ! Inicializando variaveis
      g1 = 0.0d0
      g2 = 0.0d0
      g3 = 0.0d0
c     !
c     ! Calculo do g1
      g1(1) = 1.0d0
      g1(2) = 1.0d0
      g1(3) = 1.0d0
c     !
c     ! Calculo do g2
      g2(1) = s(1)
      g2(2) = s(2)
      g2(3) = s(3)
      g2(4) = 2.0d0*s(4)
      IF(ncomp.EQ.6)THEN
          g2(ncomp-1) = 2.0d0*s(ncomp-1)
          g2(ncomp) = 2.0d0*s(ncomp)
      ENDIF
      IF(J2.EQ.0.0d0)THEN
          g2 = 0.0d0
      ELSE
          g2 = 1.0d0/(2.0d0*DSQRT(J2))*g2
      ENDIF
c     !
c     ! Calculo do g3
      g3(1) = s(2)*s(3) + J2/3.0d0
      g3(2) = s(1)*s(3) + J2/3.0d0
      g3(3) = s(1)*s(2) - s(4)**2 + J2/3.0d0
      g3(4) = 2.0d0*(-s(3)*s(4))
      IF(ncomp.EQ.6)THEN
          g3(1) = g3(1) - s(ncomp-1)**2
          g3(2) = g3(2) - s(ncomp)**2 
          g3(4) = g3(4) + 2.0d0*s(ncomp-1)*s(ncomp)
          g3(ncomp-1) = 2.0d0*(s(ncomp)*s(4)-s(1)*s(ncomp-1))
          g3(ncomp) = 2.0d0*(s(4)*s(ncomp-1)-s(2)*s(ncomp)) 
      ENDIF      
c     !
      END SUBROUTINE
c     !
c     !
      SUBROUTINE c1c2c3(J2,theta,superficie,fi,c1,c2,c3)
c     !**************************************************************************!
c     !** Subrotina: c1c2c3                                                    **!
c     !**                                                                      **!
c     !** Objetivo: calcula a magnitude das componentes do vetor de fluxo.     **!
c     !**           Adaptado de Bernaud (1991, p.90, 91)                       **!
c     !**           Adaptado de Owen e Hinton (1980, p.231)                    **!
c     !**                                                                      **!      
c     !** Situação: (10-11-2021) OK                                            **!
c     !**                                                                      **!
c     !**************************************************************************!      
      IMPLICIT NONE
      DOUBLE PRECISION J2                 ! segundo invariante do desviador
      DOUBLE PRECISION theta              ! ângulo de Lode
      DOUBLE PRECISION fi                 ! Ângulo de atrito
      INTEGER          superficie         ! 1-DPI, 2-DPII, 3-DPIII
      DOUBLE PRECISION c1,c2,c3           ! magnitude das componentes do vetor
      DOUBLE PRECISION beta1,beta2,beta3  ! parâmetros do DP
      DOUBLE PRECISION k                  ! coeficiente de empuxo
      DOUBLE PRECISION difflode		  ! diferença do ângulo de lode para +-pi/6 (singularidade)
      DOUBLE PRECISION vPi		  ! Valor de Pi
      PARAMETER	(vPi = 3.14159265358979323846d0)
c     !
c     ! Seleciona o modelo
      SELECT CASE (superficie)
          CASE(1)
c             !    
c             ! DPI
              k = (1.0d0+DSIN(fi))/(1.0d0-DSIN(fi))
              c1 = (k-1.0d0)/3.0d0
              c2 = (k+2.0d0)/DSQRT(3.0d0)
              c3 = 0.0d0
c             ! 
          CASE(2)
c             !    
c             ! DPII
              k = (1.0d0+DSIN(fi))/(1.0d0-DSIN(fi))
              c1 = (k-1.0d0)/3.0d0
              c2 = (2.0d0*k+1.0d0)/DSQRT(3.0d0)
              c3 = 0.0d0
c             !  
          CASE(3)
c             !    
c             ! DPIII - Owen e Hinton (1980, p.231)
              c1 = 2.0d0*DSIN(fi)/(DSQRT(3.0d0)*(3.0d0+DSIN(fi)))
              c2 = 1.0d0
              c3 = 0.0d0
c             !  
          CASE(4)
c             ! 
	      ! MC - Owen e Hinton (1980, p.231)
	      !
	      ! Verificacao do angulo de Lode
	      difflode = DABS(theta)-vPi/6.0d0
	      difflode = DABS(difflode)
	      IF(difflode.GT.0.1d-9)THEN
c                  !
c	           ! O angulo de lode é diferente de +-30
	           c1 = 1.0d0/3.0d0*DSIN(fi)
	           c2 = DCOS(theta)*(1+DTAN(theta)*DTAN(3.0d0*theta) + 
     &			DSIN(fi)*(DTAN(3.0d0*theta)-
     &			DTAN(theta))/DSQRT(3.0d0))
	           c3 = (DSQRT(3.0D0)*DSIN(theta)+
     &			DCOS(theta)*DSIN(fi))/(2.0d0*J2*DCOS(3.0d0*theta))
c                  !  
	      ELSE
c                  !
c		   ! O angulo de lode é igual de +-30
c             	   !
		   IF(DABS(theta+vPi/6.0d0).GT.DABS(theta))THEN
c             	        !
c		        ! O angulo de lode é positivo
c             	        !		   
		        c1 = 1.0d0/3.0d0*DSIN(fi)
		        c2 = 1.0d0/2.0d0*(DSQRT(3.0d0)-DSIN(fi)/DSQRT(3.0d0))
		        c3 = 0.0d0
c             	        !
		   ELSE
c             	        !
c		        ! O angulo de lode é negativo
c             	        !		   
		        c1 = 1.0d0/3.0d0*DSIN(fi)
		        c2 = 1.0d0/2.0d0*(DSQRT(3.0d0)+DSIN(fi)/DSQRT(3.0d0))
		        c3 = 0.0d0
c             	        !
		   ENDIF
	      ENDIF
c	      !
      ENDSELECT
      END SUBROUTINE
c     !
      SUBROUTINE yield(superficie,I1,J2,theta,c,fi,f)
c     !**************************************************************************!
c     !** Subrotina: yield                                                     **!
c     !**                                                                      **!
c     !** Objetivo: calcula o critério de escoamento.                          **!
c     !**           Adaptado de Bernaud (1991, p.90, 91)                       **!
c     !**           Adaptado de Souza Neto,  Peri, Owen (2008, p. 162-167)     **!
c     !**                                                                      **!      
c     !** Situação: (10-11-2021) OK                                            **!
c     !**                                                                      **!
c     !**************************************************************************!      
      IMPLICIT NONE
      INTEGER          superficie         ! 1-DPI, 2-DPII, 3-DPIII
      DOUBLE PRECISION I1                 ! primeiro invariante do tensor de tensões
      DOUBLE PRECISION J2                 ! segundo invariante do desviador
      DOUBLE PRECISION theta              ! ângulo de Lode
      DOUBLE PRECISION c                  ! coesão
      DOUBLE PRECISION fi                 ! Ângulo de atrito
      DOUBLE PRECISION f                  ! função de escoamento
      DOUBLE PRECISION beta1,beta2,beta3  ! Parametros para DP
      DOUBLE PRECISION k                  ! coeficiente de empuxo
c     !
c     ! Seleciona o modelo
      SELECT CASE (superficie)
      CASE(1)
c             !    
c             ! DPI
              k = (1.0d0+DSIN(fi))/(1.0d0-DSIN(fi))
              beta1 = (k-1.0d0)/3.0d0
              beta2 = (k+2.0d0)/DSQRT(3.0d0)
              beta3 = 2.0d0*DSQRT(k)*c
              f = beta1*I1 + beta2*DSQRT(J2)-beta3
c             ! 
          CASE(2)
c             !    
c             ! DPII
              k = (1.0d0+DSIN(fi))/(1.0d0-DSIN(fi))
              beta1 = (k-1.0d0)/3.0d0
              beta2 = (2.0d0*k+1.0d0)/DSQRT(3.0d0)
              beta3 = 2.0d0*DSQRT(k)*c
              f = beta1*I1 + beta2*DSQRT(J2)-beta3
c             ! 
          CASE(3)
c             !    
c             ! DPIII Souza Neto,  Peri, Owen (2008, p. 162-167)
              beta1 = 2.0d0*DSIN(fi)/(DSQRT(3.0d0)*(3.0d0+DSIN(fi)))
              beta2 = 1.0d0
              beta3 = 6.0d0*DCOS(fi)/(DSQRT(3.0d0)*(3.0d0+DSIN(fi)))*c
              f = beta1*I1 + beta2*DSQRT(J2)-beta3                        
c             ! 
          CASE(4)
c             !    
c             ! MC Owen,  Hinton (1980, p. 231) e Souza Neto,  Peri, Owen (2008, p. 164)
	        beta1 = 1.0d0/3.0d0*DSIN(fi)
	        beta2 = DCOS(theta)-DSIN(theta)*DSIN(fi)/DSQRT(3.0d0)
	        beta3 = c*DCOS(fi)
              f = beta1*I1 + beta2*DSQRT(J2)-beta3   
c             ! 
      ENDSELECT
      END SUBROUTINE
c     !
c     !
      SUBROUTINE normatensor(tensor,ncomp,norma)      
c     !**************************************************************************!
c     !** Subrotina: normatensor                                               **!
c     !**                                                                      **!
c     !** Objetivo: calcula a norma de um tensor escrito em notação de Voigt   **!
c     !**                                                                      **!     
c     !** Situação: (10-11-2021) OK                                            **!
c     !**                                                                      **!
c     !**************************************************************************!   
      IMPLICIT NONE
      INTEGER ncomp
      DOUBLE PRECISION tensor(ncomp)
      DOUBLE PRECISION norma
c     !
      IF(ncomp.EQ.6)THEN
      norma = DSQRT(tensor(1)**2 + tensor(2)**2 + tensor(3)**2 + 
     &            2*((tensor(4))**2 + 
     &            (tensor(5))**2 + (tensor(6))**2))
      ELSEIF(ncomp.EQ.4)THEN
      norma = DSQRT(tensor(1)**2 + tensor(2)**2 + tensor(3)**2 + 
     &            2*(tensor(4)**2))
      ELSE
      ENDIF
c     !
      END SUBROUTINE
c     !
      SUBROUTINE calcula_Czao(superficie,fi,Czao)
c     !**************************************************************************!
c     !** Subrotina: Czao                                                      **!
c     !**                                                                      **!
c     !** Objetivo: calcula o C utilizado no calculo da deformação plástica    **!
c     !**           efetiva. Adaptado de Chen e Han (1988, p. 257-259).        **!
c     !**                                                                      **!      
c     !** Situação: (10-11-2021) OK                                            **!
c     !**                                                                      **!
c     !**************************************************************************!           
      IMPLICIT NONE
      INTEGER             superficie          ! 1-DPI, 2-DPII, 3-DPIII
      DOUBLE PRECISION    fi                  ! angulo de atrito
      DOUBLE PRECISION    Czao                ! constante para o calculo da deformação plástica efetiva
      DOUBLE PRECISION    beta                ! constante referente a pressão hidrostática
c     !
c     ! Seleciona o modelo
      SELECT CASE (superficie)
          CASE(1)
c             !    
c             ! DPI
              beta = 2.0d0*DSIN(fi)/(DSQRT(3.0d0)*(3.0d0-DSIN(fi)))
c             ! 
              Czao = (beta+1.0d0/DSQRT(3.0d0))/
     &            (DSQRT(3.0d0*beta**2+1.0d0/2.0d0)) 
          CASE(2)
c             !    
c             ! DPII
              beta = 2.0d0*DSIN(fi)/(DSQRT(3.0d0)*(3.0d0+DSIN(fi)))
c             ! 
              Czao = (beta+1.0d0/DSQRT(3.0d0))/
     &            (DSQRT(3.0d0*beta**2+1.0d0/2.0d0))  
          CASE(3)
c             !    
c             ! DPIII
              beta = 2.0d0*DSIN(fi)/(DSQRT(3.0d0)*(3.0d0+DSIN(fi)))                       
c             ! 
              Czao = (beta+1.0d0/DSQRT(3.0d0))/
     &            (DSQRT(3.0d0*beta**2+1.0d0/2.0d0))  
          CASE(4)                         
c             ! 
c             ! MC (de Souza Neto, 2008, p. 184)
              Czao = 2.0d0*DCOS(fi)
      ENDSELECT
c     !     
      END SUBROUTINE
c     !
      SUBROUTINE calcula_Xi(superficie,fi,Xi)
c     !**************************************************************************!
c     !** Subrotina: calcula_Xi                                                **!
c     !**                                                                      **!
c     !** Objetivo: calcula Xi                                                 **!
c     !**           Adaptado de Potts e Zdravkovic (1999, p. 158)              **!
c     !**                                                                      **!
c     !**                                                                      **!      
c     !** Situação: (10-11-2021) OK                                            **!
c     !**                                                                      **!
c     !**************************************************************************! 
      IMPLICIT NONE
      INTEGER             superficie          ! 1-DPI, 2-DPII, 3-DPIII
      DOUBLE PRECISION    fi                  ! angulo de atrito
      DOUBLE PRECISION    Xi                  ! derivada de f em relação a c
      DOUBLE PRECISION    k                   ! coeficiente de empuxo
      !
      SELECT CASE(superficie)
      CASE(1)
          k = (1.0d0+DSIN(fi))/(1.0d0-DSIN(fi)) 
          Xi = 2.0d0*DSQRT(k)
      CASE(2)
          k = (1.0d0+DSIN(fi))/(1.0d0-DSIN(fi)) 
          Xi = 2.0d0*DSQRT(k)
      CASE(3)
          k = (1.0d0+DSIN(fi))/(1.0d0-DSIN(fi))
          Xi = 6.0d0*DCOS(fi)/(DSQRT(3.0d0)*(3.0d0+DSIN(fi)))
      CASE(4)
	    ! Aqui q = beta3 = X*c(epspeq) 
          Xi = DCOS(fi)
      END SELECT
      END SUBROUTINE
c     !
      SUBROUTINE calcula_dcde(ci,cp,cr,eps1,eps2,eps3,epsPleq,
     & dcde)
c     !**************************************************************************!
c     !** Subrotina: calcula_dcde                                              **!
c     !**                                                                      **!
c     !** Objetivo: calcula dc/de                                              **!
c     !**           Adaptado de Potts e Zdravkovic (1999, p. 158)              **!
c     !**                                                                      **!    
c     !** Situação: (10-11-2021) OK                                            **!
c     !**                                                                      **!
c     !**************************************************************************! 
      IMPLICIT NONE
      DOUBLE PRECISION    ci                  ! coesão inicial
      DOUBLE PRECISION    cp                  ! coesão no pico
      DOUBLE PRECISION    cr                  ! coesão residual
      DOUBLE PRECISION    eps1                ! deformação plastica equivalente 1
      DOUBLE PRECISION    eps2                ! deformação plastica equivalente 2 
      DOUBLE PRECISION    eps3                ! deformação plastica equivalente 3
      DOUBLE PRECISION    epsPleq             ! deformação plástica equivalente
      DOUBLE PRECISION    dcde                ! dc/depsPleq
c     !
      IF(epsPleq.LT.eps1)THEN
          dcde = (cp-ci)/(eps1)
      ELSEIF((epsPleq.GE.eps1).AND.(epsPleq.LE.eps2))THEN
          dcde = 0.0d0
      ELSEIF((epsPleq.GT.eps2).AND.(epsPleq.LT.eps3))THEN
          dcde = (cr-cp)/(eps3-eps2)
      ELSEIF(epsPleq.GE.eps3)THEN
          dcde = 0.0d0
      ENDIF
c     !    
      END SUBROUTINE
c     !      
*deck,usermat3d    USERDISTRIB  parallel                                gal
      subroutine usermat3d_vm_ansys(
     &                   matId, elemId,kDomIntPt, kLayer, kSectPt,
     &                   ldstep,isubst,keycut,
     &                   nDirect,nShear,ncomp,nStatev,nProp,
     &                   Time,dTime,Temp,dTemp,
     &                   stress,ustatev,dsdePl,sedEl,sedPl,epseq,
     &                   Strain,dStrain, epsPl, prop, coords, 
     &                   var0, defGrad_t, defGrad,
     &                   tsstif, epsZZ, cutFactor, 
     &                   var1, var2, var3, var4, var5,
     &                   var6, var7)
c*************************************************************************
c     *** primary function ***
c
c           user defined material constitutive model
c
c      Attention:
c           User must define material constitutive law properly
c           according to the stress state such as 3D, plane strain
c           and axisymmetry, plane stress and beam.
c
c           a 3D material constitutive model can use for
c           plane strain and axisymmetry cases.
c
c           When using shell elements, a plane stress algorithm
c           must be use.
c
c                                             gal July, 1999
c
c       The following demonstrates a USERMAT subroutine for
c       a plasticity model of 3D solid elements or plane elements
c       in plane strain or axisymmetric stress state. The plasticity
c       model is the same as TB, BISO.
c       See "ANSYS user material subroutine USERMAT" for detailed
c       description of how to write a USERMAT routine.
c
c*************************************************************************
c
c     input arguments
c     ===============
c      matId     (int,sc,i)               material #
c      elemId    (int,sc,i)               element #
c      kDomIntPt (int,sc,i)               "k"th domain integration point
c      kLayer    (int,sc,i)               "k"th layer
c      kSectPt   (int,sc,i)               "k"th Section point
c      ldstep    (int,sc,i)               load step number
c      isubst    (int,sc,i)               substep number
c      nDirect   (int,sc,in)              # of direct components
c      nShear    (int,sc,in)              # of shear components
c      ncomp     (int,sc,in)              nDirect + nShear
c      nstatev   (int,sc,l)               Number of state variables
c      nProp     (int,sc,l)               Number of material ocnstants
c
c      Temp      (dp,sc,in)               temperature at beginning of
c                                         time increment
c      dTemp     (dp,sc,in)               temperature increment 
c      Time      (dp,sc,in)               time at beginning of increment (t)
c      dTime     (dp,sc,in)               current time increment (dt)
c
c      Strain   (dp,ar(ncomp),i)          Strain at beginning of time increment
c      dStrain  (dp,ar(ncomp),i)          Strain increment
c      prop     (dp,ar(nprop),i)          Material constants defined by TB,USER
c      coords   (dp,ar(3),i)              current coordinates
c      defGrad_t(dp,ar(3,3),i)            Deformation gradient at time t
c      defGrad  (dp,ar(3,3),i)            Deformation gradient at time t+dt
c
c     input output arguments              
c     ======================             
c      stress   (dp,ar(nTesn),io)         stress
c      ustatev   (dp,ar(nstatev),io)      user state variable
c            ustatev(1)                     - equivalent plastic strain
c            ustatev(2) - statev(1+ncomp)   - plastic strain vector
c            ustatev(nStatev)               - von-Mises stress
c      sedEl    (dp,sc,io)                elastic work
c      sedPl    (dp,sc,io)                plastic work
c      epseq    (dp,sc,io)                equivalent plastic strain
c      tsstif   (dp,ar(2),io)             transverse shear stiffness
c                                         tsstif(1) - Gxz
c                                         tsstif(2) - Gyz
c                                         tsstif(1) is also used to calculate hourglass
c                                         stiffness, this value must be defined when low
c                                         order element, such as 181, 182, 185 with uniform 
c                                         integration is used.
c      var?     (dp,sc,io)                not used, they are reserved arguments 
c                                         for further development
c
c     output arguments
c     ================
c      keycut   (int,sc,io)               loading bisect/cut control
c                                         0 - no bisect/cut
c                                         1 - bisect/cut 
c                                         (factor will be determined by ANSYS solution control)
c      dsdePl   (dp,ar(ncomp,ncomp),io)   material jacobian matrix
c      epsZZ    (dp,sc,o)                 strain epsZZ for plane stress,
c                                         define it when accounting for thickness change 
c                                         in shell and plane stress states
c      cutFactor(dp,sc,o)                 time step size cut-back factor 
c                                         define it if a smaller step size is wished
c                                         recommended value is 0~1
c
c*************************************************************************
c
c      ncomp   6   for 3D  (nshear=3)
c      ncomp   4   for plane strain or axisymmetric (nShear = 1)
c      ncomp   3   for plane stress (nShear = 1)
c      ncomp   3   for 3d beam      (nShear = 2)
c      ncomp   1   for 1D (nShear = 0)
c
c      stresss and strains, plastic strain vectors
c          11, 22, 33, 12, 23, 13    for 3D
c          11, 22, 33, 12            for plane strain or axisymmetry
c          11, 22, 12                for plane stress
c          11, 13, 12                for 3d beam
c          11                        for 1D
c
c      material jacobian matrix
c        3D
c           dsdePl    |  1111   1122   1133   1112   1123   1113 |
c           dsdePl    |  2211   2222   2233   2212   2223   2213 |
c           dsdePl    |  3311   3322   3333   3312   3323   3313 |
c           dsdePl    |  1211   1222   1233   1212   1223   1213 |
c           dsdePl    |  2311   2322   2333   2312   2323   2313 |
c           dsdePl    |  1311   1322   1333   1312   1323   1313 |
c        plane strain or axisymmetric (11, 22, 33, 12)
c           dsdePl    |  1111   1122   1133   1112 |
c           dsdePl    |  2211   2222   2233   2212 |
c           dsdePl    |  3311   3322   3333   3312 |
c           dsdePl    |  1211   1222   1233   1212 |
c        plane stress (11, 22, 12)
c           dsdePl    |  1111   1122   1112 |
c           dsdePl    |  2211   2222   2212 |
c           dsdePl    |  1211   1222   1212 |
c        3d beam (11, 13, 12)
c           dsdePl    |  1111   1113   1112 |
c           dsdePl    |  1311   1313   1312 |
c           dsdePl    |  1211   1213   1212 |
c        1d
c           dsdePl    |  1111 |
c
c*************************************************************************
#include "impcom.inc"
c
      INTEGER          
     &                 matId, elemId,
     &                 kDomIntPt, kLayer, kSectPt,
     &                 ldstep,isubst,keycut,
     &                 nDirect,nShear,ncomp,nStatev,nProp
      DOUBLE PRECISION 
     &                 Time,    dTime,   Temp,    dTemp,
     &                 sedEl,   sedPl,   epseq,   epsZZ,   cutFactor
      DOUBLE PRECISION 
     &                 stress  (ncomp  ), ustatev (nStatev),
     &                 dsdePl  (ncomp,ncomp),
     &                 Strain  (ncomp  ), dStrain (ncomp  ), 
     &                 epsPl   (ncomp  ), prop    (nProp  ), 
     &                 coords  (3),
     &                 defGrad (3,3),     defGrad_t(3,3),
     &                 tsstif  (2)
c
c***************** User defined part *************************************
c
c --- parameters
c
      INTEGER          mcomp
      DOUBLE PRECISION HALF, THIRD, ONE, TWO, SMALL, ONEHALF,
     &                 ZERO, TWOTHIRD, ONEDM02, ONEDM05, sqTiny
      PARAMETER       (ZERO       = 0.d0,
     &                 HALF       = 0.5d0,
     &                 THIRD      = 1.d0/3.d0,
     &                 ONE        = 1.d0,
     &                 TWO        = 2.d0,
     &                 SMALL      = 1.d-08,
     &                 sqTiny     = 1.d-20,
     &                 ONEDM02    = 1.d-02,
     &                 ONEDM05    = 1.d-05,
     &                 ONEHALF    = 1.5d0,
     &                 TWOTHIRD   = 2.0d0/3.0d0,
     &                 mcomp      = 6
     &                 )
c
c --- local variables
c
c      sigElp   (dp,ar(6  ),l)            trial stress
c      dsdeEl   (dp,ar(6,6),l)            elastic moduli
c      sigDev   (dp,ar(6  ),l)            deviatoric stress tensor
c      dfds     (dp,ar(6  ),l)            derivative of the yield function 
c      JM       (dp,ar(6,6),l)            2D matrix for a 4 order tensor
c      pEl      (dp,sc     ,l)            hydrostatic pressure stress
c      qEl      (dp,sc     ,l)            von-mises stress
c      pleq_t   (dp,sc     ,l)            equivalent plastic strain at beginnig of time increment
c      pleq     (dp,sc     ,l)            equivalent plastic strain at end of time increment
c      dpleq    (dp,sc     ,l)            incremental equivalent plastic strain
c      sigy_t   (dp,sc     ,l)            yield stress at beginnig of time increments
c      sigy     (dp,sc     ,l)            yield stress at end of time increment
c      young    (dp,sc     ,l)            Young's modulus
c      posn     (dp,sc     ,l)            Poiss's ratio
c      sigy0    (dp,sc     ,l)            initial yield stress
c      dsigdep  (dp,sc     ,l)            plastic slop
c      twoG     (dp,sc     ,l)            two time of shear moduli
c      threeG   (dp,sc     ,l)            three time of shear moduli
c
c --- temperary variables for solution purpose
c      i, j
c      threeOv2qEl, oneOv3G, qElOv3G, con1, con2, fratio
c
      EXTERNAL         vzero, vmove, get_ElmData, get_ElmInfo
      DOUBLE PRECISION sigElp(mcomp), dsdeEl(mcomp,mcomp), G(mcomp),
     &                 sigDev(mcomp), JM    (mcomp,mcomp), dfds(mcomp),
     &                 sigi  (mcomp), strainEl(mcomp)

      DOUBLE PRECISION var0, var1, var2, var3, var4, var5,
     &                 var6, var7

      DATA G/1.0D0,1.0D0,1.0D0,0.0D0,0.0D0,0.0D0/
c
      INTEGER          i, j, ncompgt
      DOUBLE PRECISION pEl,   qEl,     pleq_t,  sigy_t , sigy,
     &                 dpleq, pleq, 
     &                 young, posn,    sigy0,   dsigdep, 
     &                 elast1,elast2,
     &                 twoG,  threeG,  oneOv3G, qElOv3G, threeOv2qEl, 
     &                 fratio,  con1,    con2, dperr(3)
c*************************************************************************
c
      keycut   = 0
      cutFactor = 0.d0
      dsigdep  = ZERO 
      pleq_t   = ustatev(1)
      pleq     = pleq_t
c *** get Young's modulus and Poisson's ratio, initial yield stress and others
      young    = prop(2)
      posn     = prop(3)
      sigy0    = prop(4)
c *** plastic strain tensor
      call vmove(ustatev(2), epsPl(1), ncomp)
c *** calculate plastic slope
      dsigdep  = young*prop(5)/(young-prop(5))
      twoG     = young / (ONE+posn)
      threeG   = ONEHALF * twoG
      elast1=young*posn/((1.0D0+posn)*(1.0D0-TWO*posn))
      elast2=HALF*twoG
c *** define tsstif(1) since it is used for calculation of hourglass stiffness
      tsstif(1) = elast2
c
c *** calculate elastic stiffness matrix (3d)
c
      dsdeEl(1,1)=(elast1+TWO*elast2)*G(1)*G(1)
      dsdeEl(1,2)=elast1*G(1)*G(2)+elast2*TWO*G(4)*G(4)
      dsdeEl(1,3)=elast1*G(1)*G(3)+elast2*TWO*G(5)*G(5)
      dsdeEl(1,4)=elast1*G(1)*G(4)+elast2*TWO*G(1)*G(4)
      dsdeEl(1,5)=elast1*G(1)*G(5)+elast2*TWO*G(1)*G(5)
      dsdeEl(1,6)=elast1*G(1)*G(6)+elast2*TWO*G(4)*G(5)
      dsdeEl(2,2)=(elast1+TWO*elast2)*G(2)*G(2)
      dsdeEl(2,3)=elast1*G(2)*G(3)+elast2*TWO*G(6)*G(6)
      dsdeEl(2,4)=elast1*G(2)*G(4)+elast2*TWO*G(1)*G(4)
      dsdeEl(2,5)=elast1*G(2)*G(5)+elast2*TWO*G(1)*G(5)
      dsdeEl(2,6)=elast1*G(2)*G(6)+elast2*TWO*G(2)*G(6)
      dsdeEl(3,3)=(elast1+TWO*elast2)*G(3)*G(3)
      dsdeEl(3,4)=elast1*G(3)*G(4)+elast2*TWO*G(5)*G(6)
      dsdeEl(3,5)=elast1*G(3)*G(5)+elast2*TWO*G(5)*G(3)
      dsdeEl(3,6)=elast1*G(3)*G(6)+elast2*TWO*G(6)*G(3)
      dsdeEl(4,4)=elast1*G(4)*G(4)+elast2*(G(1)*G(2)+G(4)*G(4))
      dsdeEl(4,5)=elast1*G(4)*G(5)+elast2*(G(1)*G(6)+G(5)*G(4))
      dsdeEl(4,6)=elast1*G(4)*G(6)+elast2*(G(4)*G(6)+G(5)*G(2))
      dsdeEl(5,5)=elast1*G(5)*G(5)+elast2*(G(1)*G(3)+G(5)*G(5))
      dsdeEl(5,6)=elast1*G(5)*G(6)+elast2*(G(4)*G(3)+G(5)*G(6))
      dsdeEl(6,6)=elast1*G(6)*G(6)+elast2*(G(2)*G(3)+G(6)*G(6))
      do i=1,ncomp-1
        do j=i+1,ncomp
          dsdeEl(j,i)=dsdeEl(i,j)
        end do
      end do
c
c
c *** get initial stress
      call get_ElmInfo('NCOMP', ncompgt)
      call vzero(sigi(1),ncompgt)
      call get_ElmData ('ISIG', elemId,kDomIntPt, ncompgt, sigi)
c
c *** calculate the trial stress and
c     copy elastic moduli dsdeEl to material Jacobian matrix
      do i=1,ncomp
         strainEl(i) = Strain(i) + dStrain(i) - epsPl(i)
      end do
      call vzero(sigElp, 6)
      do i=1,ncomp
         do j=1,ncomp
            dsdePl(j,i) = dsdeEl(j,i)
            sigElp(i) = sigElp(i)+dsdeEl(j,i)*strainEl(j)
         end do
         sigElp(i) = sigElp(i) + sigi(i)
      end do

c *** hydrostatic pressure stress
      pEl = -THIRD * (sigElp(1) + sigElp(2) + sigElp(3))
c *** compute the deviatoric stress tensor
      sigDev(1) = sigElp(1) + pEl
      sigDev(2) = sigElp(2) + pEl
      sigDev(3) = sigElp(3) + pEl
      sigDev(4) = sigElp(4)
      sigDev(5) = sigElp(5)
      sigDev(6) = sigElp(6)
c *** compute von-mises stress
      qEl = 
     &  sigDev(1) * sigDev(1)+sigDev(2) * sigDev(2)+
     &  sigDev(3) * sigDev(3)+
     &  TWO*(sigDev(4) * sigDev(4)+ sigDev(5) * sigDev(5)+ 
     &  sigDev(6) * sigDev(6))
      qEl = sqrt( ONEHALF * qEl)
c *** compute current yield stress
      sigy    = sigy0 + dsigdep * pleq
c
      fratio = qEl / sigy - ONE
c *** check for yielding
      IF (sigy .LE. ZERO.or.fratio .LE. -SMALL) GO TO 500
c
      sigy_t = sigy
      threeOv2qEl = ONEHALF / qEl
c *** compute derivative of the yield function
      DO i=1, ncomp
         dfds(i) = threeOv2qEl * sigDev(i)
      END DO
      oneOv3G  = ONE / (threeG + dsigdep)
      qElOv3G  = qEl * oneOv3G
c *** initial guess of incremental equivalent plastic strain   
      dpleq    = qElOv3G - sigy * oneOv3G
      pleq     = pleq_t + dpleq
      sigy     = sigy0 + dsigdep * pleq
c
c ***  update stresses
      DO i = 1 , ncomp
         stress(i) =  sigElp(i) - TWOTHIRD * (qEl-sigy) * dfds(i)
      END DO
c
c ***  update plastic strains
      DO i = 1 , nDirect
         epsPl(i) = epsPl(i) + dfds(i) * dpleq
      END DO
      DO i = nDirect + 1 , ncomp
         epsPl(i) = epsPl(i) + TWO * dfds(i) * dpleq
      END DO
      epseq  = pleq
c *** Update state variables
      ustatev(1) = pleq
      do i=1,ncomp
         ustatev(i+1) = epsPl(i)
      end do
c *** Update plastic work
      sedPl = sedPl + HALF * (sigy_t+sigy)*dpleq
c
c *** Material Jcobian matrix
c
      IF (qEl.LT.sqTiny) THEN
         con1 = ZERO
      ELSE
         con1 = threeG * dpleq / qEl
      END IF
      con2 = threeG/(threeG+dsigdep) - con1
      con2 = TWOTHIRD * con2
      DO i=1,ncomp
         DO j=1,ncomp
            JM(j,i) = ZERO
         END DO
      END DO
      DO i=1,nDirect
         DO j=1,nDirect
            JM(i,j) = -THIRD
         END DO
         JM(i,i) = JM(i,i) + ONE
      END DO
      DO i=nDirect + 1,ncomp
         JM(i,i) = HALF
      END DO
      DO i=1,ncomp
         DO j=1,ncomp
            dsdePl(i,j) =    dsdeEl(i,j) - twoG
     &           * (  con2 * dfds(i) * dfds(j) + con1 * JM(i,j) )
         END DO
      END DO
c
      goto 600
  500 continue

c *** Update stress in case of elastic/unloading
      do i=1,ncomp
         stress(i) = sigElp(i)
      end do

  600 continue
      sedEl = ZERO
      DO i = 1 , ncomp
         sedEl = sedEl + stress(i)*(Strain(i)+dStrain(i)-epsPl(i))
      END DO
      sedEl    = sedEl * HALF
      ustatev(nStatev) = sigy
c
!      cutFactor = 0.5d0
      return
      end

*deck,usermat3d    USERDISTRIB  parallel                                gal
      subroutine usermat3d_VE_CONCRETO(
     &                   matId, elemId,kDomIntPt, kLayer, kSectPt,
     &                   ldstep,isubst,keycut,
     &                   nDirect,nShear,ncomp,nStatev,nProp,
     &                   Time,dTime,Temp,dTemp,
     &                   stress,ustatev,dsdePl,sedEl,sedPl,epseq,
     &                   Strain,dStrain, epsPl, prop, coords, 
     &                   var0, defGrad_t, defGrad,
     &                   tsstif, epsZZ, cutFactor, 
     &                   var1, var2, var3, var4, var5,
     &                   var6, var7)
c
c     input arguments
c     ===============
c      matId     (int,sc,i)               material #
c      elemId    (int,sc,i)               element #
c      kDomIntPt (int,sc,i)               "k"th domain integration point
c      kLayer    (int,sc,i)               "k"th layer
c      kSectPt   (int,sc,i)               "k"th Section point
c      ldstep    (int,sc,i)               load step number
c      isubst    (int,sc,i)               substep number
c      nDirect   (int,sc,in)              # of direct components
c      nShear    (int,sc,in)              # of shear components
c      ncomp     (int,sc,in)              nDirect + nShear
c      nstatev   (int,sc,l)               Number of state variables
c      nProp     (int,sc,l)               Number of material ocnstants
c
c      Temp      (dp,sc,in)               temperature at beginning of
c                                         time increment
c      dTemp     (dp,sc,in)               temperature increment 
c      Time      (dp,sc,in)               time at beginning of increment (t)
c      dTime     (dp,sc,in)               current time increment (dt)
c
c      Strain   (dp,ar(ncomp),i)          Strain at beginning of time increment
c      dStrain  (dp,ar(ncomp),i)          Strain increment
c      prop     (dp,ar(nprop),i)          Material constants defined by TB,USER
c      coords   (dp,ar(3),i)              current coordinates
c      defGrad_t(dp,ar(3,3),i)            Deformation gradient at time t
c      defGrad  (dp,ar(3,3),i)            Deformation gradient at time t+dt
c
c     input output arguments              
c     ======================             
c      stress   (dp,ar(nTesn),io)         stress
c      ustatev   (dp,ar(nstatev),io)      user state variable
c            ustatev(1)                     - equivalent plastic strain
c            ustatev(2) - statev(1+ncomp)   - plastic strain vector
c            ustatev(nStatev)               - von-Mises stress
c      sedEl    (dp,sc,io)                elastic work
c      sedPl    (dp,sc,io)                plastic work
c      epseq    (dp,sc,io)                equivalent plastic strain
c      tsstif   (dp,ar(2),io)             transverse shear stiffness
c                                         tsstif(1) - Gxz
c                                         tsstif(2) - Gyz
c                                         tsstif(1) is also used to calculate
c                                          hourglass
c                                         stiffness, this value must be defined when 
c                                          low
c                                         order element, such as 181, 182, 185 with 
c                                          uniform 
c                                         integration is used.
c      var?     (dp,sc,io)                not used, they are reserved arguments 
c                                         for further development
c
c
c
c     output arguments
c     ================
c      keycut   (int,sc,io)               loading bisect/cut control
c                                         0 - no bisect/cut
c                                         1 - bisect/cut 
c                                         (factor will be determined by ANSYS solution 
c                                          control)
c      dsdePl   (dp,ar(ncomp,ncomp),io)   material jacobian matrix
c      epsZZ    (dp,sc,o)                 strain epsZZ for plane stress,
c                                         define it when accounting for thickness 
c                                          change 
c                                         in shell and plane stress states
c      cutFactor(dp,sc,o)                 time step size cut-back factor 
c                                         define it if a smaller step size is wished
c                                         recommended value is 0~1
c
c*************************************************************************
c
c      ncomp   6   for 3D  (nshear=3)
c      ncomp   4   for plane strain or axisymmetric (nShear = 1)
c      ncomp   3   for plane stress (nShear = 1)
c      ncomp   3   for 3d beam      (nShear = 2)
c      ncomp   1   for 1D (nShear = 0)
c
c      stresss and strains, plastic strain vectors
c          11, 22, 33, 12, 23, 13    for 3D
c          11, 22, 33, 12            for plane strain or axisymmetry
c
c      material jacobian matrix
c        3D
c           dsdePl    |  1111   1122   1133   1112   1123   1113 |
c           dsdePl    |  2211   2222   2233   2212   2223   2213 |
c           dsdePl    |  3311   3322   3333   3312   3323   3313 |
c           dsdePl    |  1211   1222   1233   1212   1223   1213 |
c           dsdePl    |  2311   2322   2333   2312   2323   2313 |
c           dsdePl    |  1311   1322   1333   1312   1323   1313 |
c        plane strain or axisymmetric (11, 22, 33, 12)
c           dsdePl    |  1111   1122   1133   1112 |
c           dsdePl    |  2211   2222   2233   2212 |
c           dsdePl    |  3311   3322   3333   3312 |
c           dsdePl    |  1211   1222   1233   1212 |
c
c*************************************************************************
#include "impcom.inc"
c
      INTEGER          
     &                 matId, elemId,
     &                 kDomIntPt, kLayer, kSectPt,
     &                 ldstep,isubst,keycut,
     &                 nDirect,nShear,ncomp,nStatev,nProp
      DOUBLE PRECISION 
     &                 Time,    dTime,   Temp,    dTemp,
     &                 sedEl,   sedPl,   epseq,   epsZZ,   cutFactor
      DOUBLE PRECISION 
     &                 stress  (ncomp  ), ustatev (nStatev),
     &                 dsdePl  (ncomp,ncomp),
     &                 Strain  (ncomp  ), dStrain (ncomp  ), 
     &                 epsPl   (ncomp  ), prop    (nProp  ), 
     &                 coords  (3),
     &                 defGrad (3,3),     defGrad_t(3,3),
     &                 tsstif  (2)
c
c***************** User defined part *************************************
c
c --- parameters
c
      INTEGER          mcomp
      DOUBLE PRECISION HALF, THIRD, ONE, TWO, SMALL, ONEHALF,
     &                 ZERO, TWOTHIRD, ONEDM02, ONEDM05, sqTiny
      PARAMETER       (ZERO       = 0.d0,
     &                 HALF       = 0.5d0,
     &                 THIRD      = 1.d0/3.d0,
     &                 ONE        = 1.d0,
     &                 TWO        = 2.d0,
     &                 SMALL      = 1.d-08,
     &                 sqTiny     = 1.d-20,
     &                 ONEDM02    = 1.d-02,
     &                 ONEDM05    = 1.d-05,
     &                 ONEHALF    = 1.5d0,
     &                 TWOTHIRD   = 2.0d0/3.0d0,
     &                 mcomp      = 6
     &                 )
c
c --- local variables
c
c      sigElp   (dp,ar(6  ),l)            trial stress
c      dsdeEl   (dp,ar(6,6),l)            elastic moduli
c      sigDev   (dp,ar(6  ),l)            deviatoric stress tensor
c      dfds     (dp,ar(6  ),l)            derivative of the yield function 
c      JM       (dp,ar(6,6),l)            2D matrix for a 4 order tensor
c      pEl      (dp,sc     ,l)            hydrostatic pressure stress
c      qEl      (dp,sc     ,l)            von-Mises stress
c      pleq_t   (dp,sc     ,l)            equivalent plastic strain at beginnig of time increment
c      pleq     (dp,sc     ,l)            equivalent plastic strain at end of time increment
c      dpleq    (dp,sc     ,l)            incremental equivalent plastic strain
c      sigy_t   (dp,sc     ,l)            yield stress at beginnig of time increments
c      sigy     (dp,sc     ,l)            yield stress at end of time increment
c      young    (dp,sc     ,l)            Young's modulus
c      posn     (dp,sc     ,l)            Poiss's ratio
c      sigy0    (dp,sc     ,l)            initial yield stress
c      dsigdep  (dp,sc     ,l)            plastic slop
c      twoG     (dp,sc     ,l)            two time of shear moduli
c      threeG   (dp,sc     ,l)            three time of shear moduli
c
c --- temperary variables for solution purpose
c      i, j
c      threeOv2qEl, oneOv3G, qElOv3G, con1, con2, fratio
c
      EXTERNAL         vzero, vmove, get_ElmData
      DOUBLE PRECISION sigElp(ncomp), dsdeEl(ncomp,ncomp), G(mcomp),
     &                 sigDev(ncomp), JM    (ncomp,ncomp), dfds(ncomp),
     &                 sigi  (ncomp), strainEl(ncomp)
      DOUBLE PRECISION var0, var1, var2, var3, var4, var5,
     &                 var6, var7
      DATA G/1.0D0,1.0D0,1.0D0,0.0D0,0.0D0,0.0D0/
      INTEGER          i, j, k
      DOUBLE PRECISION pEl,   qEl,     pleq_t,  sigy_t , sigy,
     &                 dpleq, pleq, 
     &                 young, posn,    sigy0,   dsigdep, 
     &                 elast1,elast2,
     &                 twoG,  threeG,  oneOv3G, qElOv3G, threeOv2qEl, 
     &                 fratio,  con1,    con2, dperr(3)
c
c --- variaveis locais do usuario necessárias ao cálculo da fluência e retração do 
c concreto
c    
      ! Variaveis de entrada do usuario TBDATA: relacionadas aos dados do concreto
      !
      ! fck [kN/cm²] resistencia caracteristica do concreto 
      ! s [adm] coef. que depende do tipo de concreto 
      ! ti [dias] tempo da analise apartir da qual o concreto iniciou 
      ! rh [%] umidade relativa do ambiente 
      ! hf [cm] espessura ficticia 
      ! ts [dias] idade do concreto no inicio da secagem 
      ! t0 [dias] idade do concreto no inicio do carregamento
      ! tinf [dias] tempo final da análise
      ! betasc [adm] coeficiente que depende do tipo de cimento 
      ! alpha [adm] efeito do tipo de cimento durante a cura 
      ! ndec [pontos por decada] No. de pontos para discretização
      ! ligafluencia 0 - desliga a fluência, 1 - liga fluência
      ! ligaretracao 0 - desliga a retração, 1 - liga a retração
      ! ktime [dias] identificacao do dia na saida de dados
      ! kelemid [un] identificacao do elemento na saida de dados
      ! kkDomIntPt [un] identificacao do ponto de integracao na saida de dados
      !
c
c
c
      ! Variaveis calculadas no interior da USERMAT
      !
      ! tmat  [dias] idade do material durante a análise (time-ti)
      ! fcm28 [kN/cm²] resistência média do concreto aos 28 dias 
      ! sigmalim_CEB90 [kN/cm²] limite de tensão para validade da viscoelasticidade do concreto
      ! Ec28 [kN/cm²] módulo de elasticidade do concreto aos 28 dias
      ! mkelvin [un] no. máximo de elementos de Kelvin
      ! ndt [un] No. de pontos para calcular os parâmetros da cadeia de Kelvin 
      ! nkelvin [un] No. de camadas da cadeia de Kelvin (DIAS,2013: N da eq3.3, p44) 
      ! tau [cm²/(kN*dia)] tempos de retardação dos elementos da cadeia de Kelvin 
      ! Emu [kN/cm²] módulos de elasticidade dos elementos da cadeia de Kelvin
      ! tmeio [dias] idade do material somada meio incremento de tempo (tmat+dtime/2)
      ! tmatadj [dias] idade do material durante a análise corrigida com a temperatura
      ! fi0 [adm] coeficiente de fluência que depende do tempo t0
      ! V [adm] volume solidificado
      ! dsdeElinv [cm²/kN] matriz de rigidez inversa
      ! epsloncf1 [adm] primeira parcela deform. fluência de uma unidade de Kelvin 
      ! epsloncf2 [adm] segunda parcela deform. por fluência de uma unidade de Kelvin
      ! epsloncf3 [adm] deformação por fluência da unidade i 
      ! deltay [adm] parametro do modelo do Bazant & Prasannan
      ! lbd [adm] parametro do modelo do Bazant & Prasannan
      ! tensor_stress(3,3) [kN/cm²] tensor das tensoes
      ! stressp(3) [kN/cm²] vetor com as tensoes principais
      ! ev(3,3) [kN/cm²] matriz com as direcoes principais
      ! nrot [un] numero de rotacoes do metodo que encontra as tensoes principais
      ! saida 0 - nao faz saida de dados, 1 - faz saida de dados
      ! 
      ! Outras variaveis
      !
      ! iott, wrinqr variaveis que guardam o numero da output window do Ansys
      !
      ! Variaveis de estado
      !
      ! ustatev(1)    primeirarodada    ! 9999 – indica primeira rodada
      ! ustatev(2)    fcm28                                       
      ! ustatev(3)    Ec28                                        
      ! ustatev(4)    nkelvin                                     
      ! ustatev(5)    t0  
      ! ustatev(6)    tmat         
      ! ustatev(7)    stressp(1)   
      ! ustatev(8)    stressp(2)
      ! ustatev(9)    stressp(3)
      ! ustatev(10)   FV = 0.4*fcm28/stressp(3)
      ! ustatev(11..) Emu                                         
      ! ustatev(21..) tau                                         
      ! ustatev(31..) epsloncsant                                
      ! ustatev(41..) epsloncs                                   
      ! ustatev(51..) depsloncs                                   
      ! ustatev(101..) epsloncfantmu                              
      !        (111..) epsloncfantmu
      !        (121..) epsloncfantmu
      !        (130..) epsloncfantmu
      !        (140..) epsloncfantmu
      !        (150..) epsloncfantmu
      !        (160..) epsloncfantmu
      ! ustatev(201..) epsloncfmu                                
      !        (211..) epsloncfmu
      !        (221..) epsloncfmu
      !        (230..) epsloncfmu
      !        (240..) epsloncfmu
      !        (250..) epsloncfmu
      !        (260..) epsloncfmu
      ! ustatev(301..) depsloncf                                  
      ! ustatev(401..) dstress
      !
      DOUBLE PRECISION fck,s,ti,rh,hf,ts,t0,tinf,betasc,alpha                                                                                                             
      INTEGER          ndec,ligafluencia,ligaretracao
      INTEGER          kelemId,kkDomIntPt
      DOUBLE PRECISION ktime
      DOUBLE PRECISION tmat,fcm28,Ec28
      INTEGER          mkelvin,ndt,nkelvin
      PARAMETER        (mkelvin=7)
      DOUBLE PRECISION tau(mkelvin),EMU(mkelvin),tmeio,tmatadj,fi0,V,
     &                 dsdeElinv(ncomp,ncomp),epsloncf1(ncomp),
     &                 epsloncf2(ncomp),epsloncf3(ncomp),
     &                 deltay(mkelvin),lbd(mkelvin)
      EXTERNAL         wrinqr
      INTEGER          iott,wrinqr                                  
      DOUBLE PRECISION wr_output
      DOUBLE PRECISION tensor_stress(3,3)
      DOUBLE PRECISION stressp(3)
      DOUBLE PRECISION ev(3,3)
      INTEGER          nrot
      INTEGER          saida
      DOUBLE PRECISION CEB90_fcm
      DOUBLE PRECISION CEB90_Ec
      DOUBLE PRECISION CEB90_epsloncs
      DOUBLE PRECISION CEB90_tadj
      DOUBLE PRECISION CEB90_tT
      DOUBLE PRECISION CEB90_fi0
c
c*************************************************************************c
      !
      !*************************************************************************!
      ! PASSO1) Entrada de dados do script                                      !
      !*************************************************************************!
      ligafluencia    = prop(2)
      ligaretracao    = prop(3)
      ti              = prop(4)
      ts              = prop(5)
      t0              = prop(6)
      tinf            = prop(7)
      fck             = prop(8)
      posn            = prop(9)
      s               = prop(10)
      rh              = prop(11)
      hf              = prop(12)
      betasc          = prop(13)
      alpha           = prop(14)
      ndec            = prop(15)
      ktime           = prop(16)
      kelemid         = prop(17)
      kkDomIntPt      = prop(18)
      iott            = wrinqr(WR_OUTPUT)
      !
      !*************************************************************************!
      ! PASSO2) Preparando arquivo de saida com os valores do vetor ustatev     !
      !*************************************************************************!
      saida = 0
      if (kelemId.EQ.elemId.
     & AND.kkDomIntPt.EQ.kDomIntPt.
     & AND.ktime.EQ.time) THEN 
          saida = 1
      endif
      !
      if (saida.EQ.1) then
          open(1,file='ustatev.txt',access='sequential',
     & form="formatted",status="unknown",
     & position="append")
          write(1,*)'----------------------------------------------'
          write(1,*)'SAIDA DE DADOS DO VETOR USTATEV'
          write(1,*)'----------------------------------------------'      
          write(1,*)'ID: time,elemId,kDomIntPt:'
          write(1,*) time,elemId,kDomIntPt     
          write(1,*)'ldstep,isubst'
          write(1,*) ldstep,isubst 
      endif
      !
      !*************************************************************************!
      ! PASSO3) Obtendo parametros do modelo de Kelvin                          !
      !*************************************************************************!
      !
      ! Calcula os parâmetros do modelo de Kelvin apenas uma vez por ponto de integração
      if (ustatev(1).NE.9999) then
          !
          ! Calculos iniciais
          fcm28 = CEB90_fcm(fck,28.0d0,20.0d0,s)
          Ec28 = CEB90_Ec(fck,s,28.0d0,20.0d0)
          !
          ! Calculando numero de elementos de Kelvin e o numero de pontos do ajuste
          call KELPAR(t0,tinf,ndec,nkelvin,ndt) 
          !
          ! Calculando os tempos de retardação e módulos do ajuste
          call KELVIN_betactt0(nkelvin,t0,tinf,ndec,ndt,
     & tau,Emu,temp,rh,hf)
          !
          ! Guardando os parâmetros
          ustatev(2) = fcm28
          ustatev(3) = Ec28
          ustatev(4) = nkelvin
          ustatev(5) = t0
          !
          do i=1,nkelvin
              ustatev(10+i)=Emu(i)
              ustatev(20+i)=tau(i)
          enddo
          !
          ! Definindo variavel que indica o fim da primeira rodada
          ustatev(1) = 9999
          !
      else
          ! Recupera os parâmetros
          fcm28 = ustatev(2)
          Ec28 = ustatev(3)
          nkelvin = ustatev(4)
          t0 = ustatev(5)
          do i=1,nkelvin
              Emu(i) = ustatev(10+i)
              tau(i) = ustatev(20+i)
          enddo           
      endif
      !    
      !*************************************************************************!
      ! PASSO4) Calculo da idade do material                                    !
      !*************************************************************************!
      !
      if (time.GT.ti) then
          tmat = time-ti
      else
          tmat = 0.0d0
      endif
      ustatev(6) = tmat
      !
      !*************************************************************************!
      ! PASSO5) Calculo do incremento de deformacao por retracao                !
      !*************************************************************************!
      !
      if (time.GE.ti) then
          !
          ! Calcula o coeficiente de retração para o próximo passo de tempo (tmat+dtime)
          do i=1,3
              ustatev(40+i) = 
     & CEB90_epsloncs(tmat+dtime,ts,fcm28,betasc,rh,hf,temp)
          enddo
          !
          ! Calcula o incremento de deformação por retração (apenas nas três direções principais)
          do i=1,3
              ustatev(50+i) = 
     & ustatev(40+i)-ustatev(30+i)
          enddo
      endif
      !
      !*************************************************************************!
      ! PASSO6) Calculo do incremento de deformacao por fluencia                !
      !*************************************************************************!
      !
      !  Calcula apenas quando a idade da peça atinge a idade em que entra em carga
      if (tmat.GT.t0) then  
          !
          ! Guardando deformação por fluência do ultimo passo que convergiu
          do i=1,nkelvin
              do j=1,ncomp
                  ustatev(100+(i-1)*10+j) = ustatev(200+(i-1)*10+j)
              enddo
          enddo             
          !
          ! Calculando o fator do envelhecimento (com a idade da peça em carga (tmat-t0))
          tmatadj = CEB90_tadj(tmat-t0,alpha,temp,tmat)
          tmeio = tmatadj+dtime/2.0d0
          fi0 = CEB90_fi0(tmeio,rh,hf,fcm28,temp)
          V = Ec28/fi0
          !
          ! Inicializando o incremento de deformação por fluência
          do i =1,ncomp
              ustatev(300+i) = 0.0d0
          enddo
          !
          ! Calculo do incremento de deformação por fluência
          do i=1,nkelvin
              !
              ! Calculo da Matriz Dmu
              deltay(i) = dtime/tau(i)
              lbd(i) = (1.0d0-dexp(-deltay(i)))/deltay(i)
              young = (Emu(i)*V)/(lbd(i))
              call MatrizD(young,posn,ncomp,dsdeEl)                   
              call matinv(ncomp,dsdeEl,dsdeElinv)
              !
              ! Calculo da primeira parcela da deformação por fluência de uma unidade
              epsloncf1=0.0d0
              do j=1,ncomp
                  do k=1,ncomp
                      epsloncf1(j) = epsloncf1(j)+
     & dsdeElinv(j,k)*ustatev(400+k)
                  enddo
              enddo
              !
              ! Calculo da segunda parcela da deformação por fluência de uma unidade 
              do j =1,ncomp
                  epsloncf2(j) = 
     & ustatev(100+(i-1)*10+j)*dexp(-deltay(i))
              enddo
              !
              ! Calculo da deformação por fluência da unidade i
              do j=1,ncomp
                  ustatev(200+(i-1)*10+j) =
     & epsloncf1(j)+epsloncf2(j)
              enddo
              !                
              ! Calculo do incremento de deformação por fluência de todas unidades
              do j =1,ncomp
                  ustatev(300+j) =
     & ustatev(300+j)+
     & ustatev(200+(i-1)*10+j)*(1-dexp(-deltay(i)))
              enddo
              !                                    
          enddo
          !
      endif
      !
      !*************************************************************************!
      ! PASSO7) Calculo do incremento de deformacao elastica                    !
      !*************************************************************************!
      !
      ! calculo do deltay
      deltay = 0.0d0
      do i = 1,nkelvin
          deltay(i) = dtime/tau(i)
      enddo
      !
      ! calculo do lbd
      lbd = 0.0d0
      do i = 1,nkelvin
          lbd(i) = (1.0d0-dexp(-deltay(i)))/deltay(i)
      enddo
      !
      ! calculo do v
      tmatadj = CEB90_tadj(tmat-t0,alpha,temp,tmat)
      tmeio = tmatadj+dtime/2.0d0
      fi0 = CEB90_fi0(tmeio,rh,hf,fcm28,temp)
      V = Ec28/fi0
      !
      ! calculo do modulo de Young corrigido
      young = 0.0d0
      do i=1,nkelvin
          young = young + (1.0d0-lbd(i))/(Emu(i)*V)*ligafluencia  
      enddo
      young = young + 1.0d0/CEB90_Ec(fck,s,tmeio,temp)
      young = 1.0d0/young
      !
      ! Calculando a matriz de rigidez elástica
      call MatrizD(young,posn,ncomp,dsdeEl)
      !
      ! Descontando o incremento de deformação por fluência e retração do incremento de deformação 
c total (Equação 5.60)
      do i=1,ncomp
          dstrain(i) = dstrain(i)
     & -ustatev(300+i)*ligafluencia 
     & -ustatev(50+i)*ligaretracao    
      end do
      !
      !*************************************************************************!
      ! PASSO8) Calculo do incremento de tensão                                 !
      !*************************************************************************!
      !     
      sigElp = 0.0d0
      do i=1,ncomp
          do j=1,ncomp
              sigElp(i) = sigElp(i)+dsdeEl(i,j)*(dstrain(j))
          end do
      end do 
      !
      !
      !*************************************************************************!
      ! PASSO9) Atualizando a tensão                                            !
      !*************************************************************************!
      !      
      do i=1,ncomp
         stress(i) = stress(i)+sigElp(i)
      end do 
      !
      !*************************************************************************!
      ! PASSO10) Atualizando a matriz Jacobiana                                 !
      !*************************************************************************!
      !
      do i=1,ncomp
          do j=1,ncomp
              dsdePl(j,i) = dsdeEl(j,i)               
          end do
      end do 
      !
      !*************************************************************************!
      ! PASSO11) Guardando a tensão incremento de tensao e deformação retração  !
      !*************************************************************************!
      !
      do i=1,ncomp
          ustatev(400+i) = sigElp(i)
      enddo
      !
      do i=1,ncomp
          ustatev(30+i) = ustatev(40+i)     
      enddo
      !
      !*************************************************************************!
      ! PASSO12) Calculando o fator de validação                                !
      !*************************************************************************!
      !
      ! Encontrando as tensões e direções principais
      call jacobi(stress,3,3,stressp,ev,nrot)
      !
      ! Ordenando as tensões e direções principais
      call eigsrt(stressp,ev,3,3)
      !
      ustatev(7) = stressp(1)
      ustatev(8) = stressp(2)
      ustatev(9) = stressp(3)
      ustatev(10) = abs(0.4d0*ustatev(2)/ustatev(9))
      !
      !*************************************************************************!
      ! PASSO13) Escrevendo o vetor ustatev na saida de dados                   !
      !*************************************************************************!
      if (saida.EQ.1) then
          do i=1,nStatev
              write(1,*)i, ustatev(i)
          enddo
          close(1,STATUS='KEEP') 
      endif
      !
      return
      End
      SUBROUTINE matrizD(E,Poisson,ncomp,D)
c     !**************************************************************************!
c     !** Função: matrizD                                                      **!
c     !**                                                                      **!
c     !** Objetivo: calcula a matriz consitutiva do material isotrópico        **!
c     !**           adaptado de Smith, Griffiths e Margetts (2014, p.42-44)    **!
c     !**                                                                      **!
c     !** Situação: (28-09-2016) OK                                            **!
c     !**                                                                      **!
c     !**************************************************************************!
      IMPLICIT NONE
      DOUBLE PRECISION E              ! módulo de elasticidade                  
      DOUBLE PRECISION Poisson        ! coeficiente de Poisson
      INTEGER ncomp                   ! numero de componentes
      DOUBLE PRECISION D(ncomp,ncomp) ! matriz constitutiva elástica isotrópica
c     !
	D=0.0d0
	D(1,1)=(E*(1.0d0-Poisson))/((1.0d0+Poisson)*(1.0d0-2.0d0*Poisson))
	D(1,2)=(E*Poisson)/((1.0d0+Poisson)*(1.0d0-2.0d0*Poisson))
	D(1,3)=D(1,2)
	D(2,1)=D(1,2)
	D(2,2)=D(1,1)
	D(2,3)=D(1,2)
	D(3,1)=D(1,3)
	D(3,2)=D(2,3)
	D(3,3)=D(1,1)
	D(4,4)=(E)/((1.0d0+Poisson)*2.0d0)
c     !
      IF(ncomp.EQ.6)THEN
          D(ncomp-1,ncomp-1)=D(4,4)
	    D(ncomp,ncomp)=D(4,4)
      ENDIF
c     !
      END SUBROUTINE MatrizD
      !
      function CEB90_tT(temp,deltat)
      !**************************************************************************!
      !** Função: CEB90_tT                                                     **!
      !**                                                                      **!
      !** Objetivo: considera o efeito da temperatura na maturidade do         **!
      !**           concreto                                                   **!
      !**                                                                      **!
      !** Referencia: CEB-MC90                                                 **!
      !** Situação: (28-09-2016) OK                                            **!
      !**                                                                      **!
      !**************************************************************************!
      
      DOUBLE PRECISION temp   ! [oC] temperatura       
      DOUBLE PRECISION deltat ! [dias] intervalo em dias em que a temp. prevalece     
      DOUBLE PRECISION CEB90_tT
      !
      CEB90_tT = deltat*dexp(13.65d0-4000.0d0/(273.0d0+temp))
      !
      end
      
      function CEB90_tadj(t,alpha,temp,deltat)
      !**************************************************************************!
      !** Função: CEB90_tadj                                                   **!
      !**                                                                      **!
      !** Objetivo: considera o efeito do tipo de cimento e temperatura de     **!
      !**           cura na idade de carregamento.                             **!
      !**                                                                      **!
      !** Referencia: CEB-MC90                                                 **!
      !** Situação: (28-09-2016) OK                                            **!
      !**                                                                      **!
      !**************************************************************************!
      
      DOUBLE PRECISION t      ! [dias] idade         
      DOUBLE PRECISION alpha  ! [adm] coeficiente que depende do tipo de cimento    
      DOUBLE PRECISION temp   ! [oC] temperatura       
      DOUBLE PRECISION deltat ! [dias] intervalo em dias em que a temp. prevalece 
      DOUBLE PRECISION tT     ! [dias] idade ajustada     
      DOUBLE PRECISION CEB90_tadj
      DOUBLE PRECISION CEB90_tT
      !
      tT = CEB90_tT(temp,deltat)
      CEB90_tadj = tT * (9.0d0 / (2.0d0 + (tT) ** 1.2d0) + 1.0d0) 
     & ** alpha
      If (CEB90_tadj.LE.0.5d0) Then 
          CEB90_tadj = 0.5d0
      endif
      !
      end
      function CEB90_fcm(fck,t,temp,s)
      !**************************************************************************!
      !** Função: CEB90_fcm                                                    **!
      !**                                                                      **!
      !** Objetivo: calcular a resistência média do concreto considerando o    **!
      !**           o tempo t e a temperatura constante temp.                  **!
      !**                                                                      **!
      !** Referencia: CEB-MC90                                                 **!
      !** Situação: (28-09-2016) OK                                            **!
      !**                                                                      **!
      !**************************************************************************!
      
      DOUBLE PRECISION fck     ! [MPa] resistência característica a compressão    
      DOUBLE PRECISION t       ! [dias] idade
      DOUBLE PRECISION s       ! [adm] coeficiente que depende do tipo de cimento
      DOUBLE PRECISION temp    ! [oC] temperatura
      DOUBLE PRECISION Bcc     ! [adm] coeficiente
      DOUBLE PRECISION fcm     ! [MPa] resistência média a compressão
      DOUBLE PRECISION CEB90_fcm
      !
      fcm = fck + 8.0d0 
      Bcc = dexp(s*(1.0d0-dsqrt(28.0d0/t)))  
      fcm = Bcc*fcm
      fcm = fcm*(1.06d0-0.003d0*temp)
      CEB90_fcm = fcm
      !
      End
           
      function CEB90_Ec(fck,s,t,temp)  
      !**************************************************************************!
      !** Função: CEB90_Eci                                                    **!
      !**                                                                      **!
      !** Objetivo: calcular o módulo de elasticidade do concreto considerando **!
      !**           o tempo t e a temperatura constante temp.                  **!
      !**                                                                      **!
      !** Referencia: CEB-MC90                                                 **!
      !** Situação: (28-09-2016) OK                                            **!
      !**                                                                      **!
      !**************************************************************************!
      DOUBLE PRECISION fck        ! [MPa] resistência característica a compressão    
      DOUBLE PRECISION s          ! [adm] coeficiente que depende do tipo de cimento       
      DOUBLE PRECISION t          ! [dias] idade      
      DOUBLE PRECISION temp       ! [oC] temperatura       
      DOUBLE PRECISION Ec0        ! [MPa] módulo de elasticidade de referência  
      DOUBLE PRECISION fcm0       ! [MPa] resistência de referência
      DOUBLE PRECISION Eci        ! [MPa] módulo de elasticidade inicial
      DOUBLE PRECISION Bcc        ! [adm] coeficiente
      DOUBLE PRECISION Be         ! [adm] coeficiente
      DOUBLE PRECISION Ec         ! [MPa] módulo de elasticidade do concreto
      DOUBLE PRECISION CEB90_Ec
      !
      Ec0 = 21500.0d0                        
      fcm0 = 10.0d0            
      Eci = Ec0*((fck+8.0d0)/fcm0)**(1.0d0/3.0d0)                   
      Eci = Eci*(1.06d0-0.003d0*temp)
      Bcc = dexp(s*(1.0d0-dsqrt(28.0d0/t)))               
      Be = SQRT(Bcc)                             
      Ec = Be*Eci 
      !
      CEB90_Ec = Ec
      !
      end 
      function CEB90_fi0(t0,rh,hf,fcm,temp)
      !**************************************************************************!
      !** Função: CEB90_fi0                                                    **!
      !**                                                                      **!
      !** Objetivo: calcular o coeficiente de fluência que depende do tempo t0 **!
      !**                                                                      **!
      !** Referencia: CEB-MC90                                                 **!
      !** Situação: (28-09-2016) OK                                            **!
      !**                                                                      **!
      !**************************************************************************!
      DOUBLE PRECISION t0             ! [dias] idade no instante de aplicação da carga         
      DOUBLE PRECISION rh             ! [%] umidade relativa
      DOUBLE PRECISION hf             ! [m] espessura ficticia
      DOUBLE PRECISION fcm            ! [MPa] resistência média a compressão
      DOUBLE PRECISION temp           ! [oC] temperatura
      DOUBLE PRECISION fcm0           ! [MPa] resistência de referencia
      DOUBLE PRECISION firh           ! [adm] coeficiente
      DOUBLE PRECISION fit            ! [adm] coeficiente
      DOUBLE PRECISION betafcm        ! [adm] coeficiente
      DOUBLE PRECISION betat0         ! [adm] coeficiente
      DOUBLE PRECISION CEB90_fi0
      !
      fcm0 = 10.0d0                                                      
      firh = 1.0d0+(1.0d0-RH/100.0d0)/(0.46d0*(hf*1000.0d0/100.0d0)**
     & (1.0d0/3.0d0))     
      fit = dexp(0.015d0*(temp-20.0d0))
      firh = fit+(firh-1.0d0)*fit**1.2d0
      betafcm = 5.3d0/((fcm/fcm0)**0.5d0)
      betat0 = 1.0d0/(0.1d0+(t0/1.0d0)**0.2d0)
      CEB90_fi0 = firh*betafcm*betat0
      !
      end
      
      function CEB90_betactt0(t,t0,rh,hf,temp)
      !**************************************************************************!
      !** Função: CEB90_betactt0                                               **!
      !**                                                                      **!
      !** Objetivo: calcular o coeficiente de fluência que depende do          **!
      !**           intervalo de tempo de aplicação da carga t-t0              **!      
      !**                                                                      **!
      !** Referencia: CEB-MC90                                                 **!
      !** Situação: (28-09-2016) OK                                            **!
      !**                                                                      **!
      !**************************************************************************!
      DOUBLE PRECISION t                  ! [dias] idade      
      DOUBLE PRECISION t0                 ! [dias] idade na aplicação da carga
      DOUBLE PRECISION rh                 ! [%] umidade relativa
      DOUBLE PRECISION hf                 ! [m] espessura fictícia
      DOUBLE PRECISION temp               ! [oC] temperatura
      DOUBLE PRECISION betah              ! [adm] coeficiente
      DOUBLE PRECISION betat              ! [adm] coeficiente
      DOUBLE PRECISION CEB90_betactt0
      !
      betah = 150.0d0*(1.0d0+(1.2d0*rh/100.0d0)**18.0d0)*(hf*1000.0d0)
     & /100.0d0+250.0d0
      betat = exp(1500.0d0/(273.0d0+temp)-5.12d0)
      betah = betah*betat
      if (betah.GT.1500.0d0) then
          betah = 1500.0d0
      endif
      CEB90_betactt0 = ((t-t0)/(betah+(t-t0)))**0.3d0
      !
      end
      
      function CEB90_epsloncs(t,ts,fcm,betasc,rh,hf,temp)
      !**************************************************************************!
      !** Função: CEB90_epsloncs                                               **!
      !**                                                                      **!
      !** Objetivo: calcular o deformação de retração                          **!    
      !**                                                                      **!
      !** Referencia: CEB-MC90                                                 **!
      !** Situação: (28-09-2016) OK                                            **!
      !**                                                                      **!
      !**************************************************************************!
      DOUBLE PRECISION t           ! [dias] idade    
      DOUBLE PRECISION ts          ! [dias] idade no final da cura
      DOUBLE PRECISION fcm         ! [MPa] resistência média a compressão
      DOUBLE PRECISION betasc      ! [adm] coeficien que depende do tipo de cimento
      DOUBLE PRECISION rh          ! [%] umidade relativa
      DOUBLE PRECISION hf          ! [m] espessura ficticia
      DOUBLE PRECISION temp        ! [oC] temperatura
      DOUBLE PRECISION fcm0        ! [MPa] resistência de referencia
      DOUBLE PRECISION betasrh     ! [adm] coeficiente
      DOUBLE PRECISION betarh      ! [adm] coeficiente
      DOUBLE PRECISION betast      ! [adm] coeficiente
      DOUBLE PRECISION betastts    ! [adm] coeficiente
      DOUBLE PRECISION epsloncsfcm  ! [adm] deformação específica
      DOUBLE PRECISION epsloncs0    ! [adm] deformação específica
      DOUBLE PRECISION CEB90_epsloncs
      !
      if (t.GT.ts) then
          fcm0 = 10.0d0    
          epsloncsfcm = (160.0d0+10.0d0*betasc*(9.0d0-fcm/fcm0))*10.0d0
     % **(-6)
          if (rh.GE.40.0d0.AND.rh.LE.99.0d0) THEN
              betasrh = 1.0d0-(rh/100.0d0)**3
              betarh = -1.55d0*betasrh    
          else
              betarh = 0.25d0
          endif
          betast = 1.0d0+(8.0d0/(103.0d0-rh))*((temp-20.0d0)/40.0d0)
          betarh = betarh*betast
          epsloncs0 = epsloncsfcm*betarh
          betastts = ((t-ts)/(350.0d0*(hf*1000.0d0/100.0d0)**2*
     & exp(-0.06d0*(temp-20.0d0))+(t-ts)))**0.5d0
          CEB90_epsloncs = epsloncs0*betastts
      else
          CEB90_epsloncs = 0.0d0
      endif 
      !
      end
      
      subroutine KELPAR(t0,tinf,ndec,nkelvin,ndt)
      !**************************************************************************!
      !** Subrotina: KELPAR                                                    **!
      !**                                                                      **!
      !** Objetivo: subrotina para determinar o numero de camadas de kelvin    **!
      !**           e o numero de intervalos de tempo                          **!
      !**                                                                      **!
      !** Referencia: DIAS,M.M. Análise numérica de vigas mistas aço-concreto  **!
      !**             pelo método dos elementos finitos: efeitos de longa      **!
      !**             duração. 2013. Dissertação (Mestrado em Engenharia)      **!
      !**             Programa de Pós Graduação em Engenharia Civil, UFRGS,    **!
      !**             Porto Alegre.                                            **!
      !**                                                                      **!
      !**             BAZANT,Z.P.; PRASANNAN, S. Solidification Theory for     **!
      !**             concrete creep. I: Formulation, Journal of Enginnering   **!
      !**             mechanics, v.115, n.8, p.1691-1703, 1989.                **!
      !**                                                                      **!      
      !**             BAZANT,Z.P.; PRASANNAN, S. Solidification Theory for     **!
      !**             concrete creep. II: verification and application.        **!
      !**             Journal of Enginnering Mechanics, v.115, n.8,            **!
      !**             p.1704-1725, 1989.                                       **!
      !**                                                                      **!
      !** Situação: (28-09-2016) OK                                            **!
      !**                                                                      **!
      !**************************************************************************!
      DOUBLE PRECISION t0             ! [dias] idade inicial para o ajuste      
      DOUBLE PRECISION tinf           ! [dias] idade final para o ajuste
      INTEGER          ndec           ! [un] numero de pontos por decada no ajuste
      INTEGER          nkelvin        ! [un] numero de elementos de Kelvin
      INTEGER          ndt            ! [un] total de pontos do ajuste     
      DOUBLE PRECISION d4             ! auxiliar  
      DOUBLE PRECISION d2             ! auxiliar
      !
      ! numero de camadas do modelo de Kelvin Generalizado
      nkelvin=0
	do
		nkelvin=nkelvin+1
		d4=(10.0d0**(nkelvin-1))*(0.01d0*t0)
		if(d4>=(tinf/2.0d0)) then
			exit
		end if
	end do
      if(nkelvin>=7) then
		nkelvin=6
      end if
      !
      ! numero de tempos discretos
	ndt=0
	d2=(t0)*0.1d0
	do 
		ndt=ndt+1
		d2=(10.0d0**(1.0d0/ndec))*d2
		if(d2>=tinf-t0) then
			exit
		end if
      end do
      !
      end
           
      subroutine KELVIN_betactt0(nkelvin,t0,tinf,ndec,ndt,
     & tau,Emu,temp,rh,hf)
      !**************************************************************************!
      !** Subrotina: Kelvin_Generalizado                                       **!
      !**                                                                      **!
      !** Objetivo: calcula os parâmetros do modelo de Kelvin-Generalizado     **!
      !**                                                                      **!
      !** Referencia: DIAS,M.M. Análise numérica de vigas mistas aço-concreto  **!
      !**             pelo método dos elementos finitos: efeitos de longa      **!
      !**             duração. 2013. Dissertação (Mestrado em Engenharia)      **!
      !**             Programa de Pós Graduação em Engenharia Civil, UFRGS,    **!
      !**             Porto Alegre.                                            **!
      !**             Porto Alegre.                                            **!
      !**                                                                      **!
      !**             BAZANT,Z.P.; PRASANNAN, S. Solidification Theory for     **!
      !**             concrete creep. I: Formulation, Journal of Enginnering   **!
      !**             mechanics, v.115, n.8, p.1691-1703, 1989.                **!
      !**                                                                      **!      
      !**             BAZANT,Z.P.; PRASANNAN, S. Solidification Theory for     **!
      !**             concrete creep. II: verification and application.        **!
      !**             Journal of Enginnering Mechanics, v.115, n.8,            **!
      !**             p.1704-1725, 1989.                                       **!
      !**                                                                      **! 
      !**             CEB MODEL CODE 1990                                      **!
      !**                                                                      **!
      !** Situação: (29-09-2016) TESTE                                         **!
      !**                                                                      **!
      !**************************************************************************!
      INTEGER          nkelvin        ! [un] numero de elementos de Kelvin           
      DOUBLE PRECISION t0             ! [dias] idade inicial para o ajuste               
      DOUBLE PRECISION tinf           ! [dias] idade final para o ajuste             
      INTEGER          ndec           ! [un] numero de pontos por decada no ajuste          
      INTEGER          ndt            ! [un] total de pontos do ajuste             
      DOUBLE PRECISION tau(nkelvin)   ! [1/(MPa*dia)] tempos de retardação da cadeia    
      DOUBLE PRECISION Emu(nkelvin)   ! [MPa] modulos de elasticidade da cadeia
      DOUBLE PRECISION temp           ! [oC] temperatura
      DOUBLE PRECISION rh             ! [%] umidade relativa
      DOUBLE PRECISION hf             ! [cm] espessura ficticia           
      !
      DOUBLE PRECISION dti(ndt)       ! [dias] intervalos de tempo          
      DOUBLE PRECISION fit            ! [adm] guarda o coeficiente que será ajustado
      DOUBLE PRECISION C(nkelvin,nkelvin) ! matriz de coeficiente 
      DOUBLE PRECISION b(nkelvin)     ! vetor de termos independentes
      DOUBLE PRECISION x(nkelvin)     ! vetor de incognitas
      INTEGER          ntau           ! auxiliar
      INTEGER          ndti           ! auxiliar
      INTEGER          ndt0i          ! auxiliar
      INTEGER          i,j,k          ! contador
      DOUBLE PRECISION a1,a2,aa       ! auxiliar
      INTEGER          er             ! variavel que indica erro na solução do sistema
      DOUBLE PRECISION CEB90_betactt0
      !
      ! Inicializa a variavel
      tau = 0.0d0
      dti = 0.0d0
      !
      ! Zerando a matriz C e o vetor b
      C = 0.0d0
      b = 0.0d0
      x = 0.0d0
      !
      ! Calcula os intervalos de tempo de aplicação de carga 
      dti(1)=0.1d0*t0
      DO ndti=2,ndt
          dti(ndti)=(10.0d0**(1.0d0/ndec))*dti(ndti-1)
      ENDDO
      dti(ndt)=tinf-t0
      !
      ! Calcula os tempos de retaração
      tau(1) = 0.01d0*t0          
      DO ntau=2,nkelvin
          tau(ntau)=(10.0d0**(ntau-1))*tau(1)
      ENDDO
      !
      ! Calculo da matriz C
      DO i=1,nkelvin
          DO j=1,nkelvin
              DO k=1,ndt
                  a1=1.0d0-DEXP(-dti(k)/tau(i))
                  a2=1.0d0-DEXP(-dti(k)/tau(j))
                  aa=a1*a2
                  c(i,j)=c(i,j)+aa
              ENDDO
          ENDDO
      ENDDO
      !
      DO i=1,nkelvin
          DO k=1,ndt
              a1=1.0d0-DEXP(-dti(k)/tau(i))
              fit = CEB90_betactt0(dti(k),0.0d0,rh,hf,temp)
              a2= fit
              aa=a1*a2
              b(i)=b(i)+aa
          ENDDO
      ENDDO
      !
      !
      ! Resolução do sistema
      call gauss_parcial(C,b,nkelvin,x,1d-20,er)
      !
      ! Módulos de elasticidade do modelo de Kelvin-Generalizado
      DO i=1,nkelvin
          Emu(i) = 1.0d0/x(i)      
      ENDDO
      !
      END     
                 
      subroutine gauss_parcial(a,b,n,x,tol,er)
      !**************************************************************************!
      !** Subrotina: gauss_parcial                                             **!
      !**                                                                      **!
      !** Objetivo: resolve sistema de equações pelo metodo de Gauss.          **!
      !**                                                                      **!
      !** Referencia: CHAPRA, S. C.; CANALE, R. P. Métodos numéricos para      **!
      !**             engenharia. 5.ed, São Paulo: McGraw-Hill, 2008.          **!      
      !**                                                                      **!
      !** Situação: (26-10-2016) OK                                            **!
      !**                                                                      **!
      !**************************************************************************!    
      DOUBLE PRECISION a(n,n)     ! matriz dos coeficientes
      DOUBLE PRECISION b(n)       ! vetor de termos independentes
      INTEGER          n          ! dimensão do sistema
      DOUBLE PRECISION x(n)       ! vetor solução
      DOUBLE PRECISION tol        ! tolerância
      INTEGER          er         ! -1, indica que houve erro
      DOUBLE PRECISION s(n)       ! vetor que guarda o maior valor da linha
      INTEGER          i,j        ! contador
      !
      er = 0
      !
      ! Identifica o maior valor da linha
      DO i=1,n
          s(i) = abs(a(i,1))
          DO j=2,n
              IF (abs(a(i,j)).GT.s(i)) THEN
                  s(i) = abs(a(i,j))
              ENDIF
          ENDDO
      ENDDO
      !
      ! Inicia a eliminação de Gauss
      CALL eliminate(a,s,n,b,tol,er)
      !
      ! Faz a retrosubstituição
      IF (er.NE.-1) THEN
          call substitute(a,n,b,x)
      ENDIF
      !
      end
      
      subroutine eliminate(a,s,n,b,tol,er)
      !**************************************************************************!
      !** Subrotina: eliminate                                                 **!
      !**                                                                      **!
      !** Objetivo: faz a eliminação do sistema de Gauss.                      **!
      !**                                                                      **!
      !** Referencia: CHAPRA, S. C.; CANALE, R. P. Métodos numéricos para      **!
      !**             engenharia. 5.ed, São Paulo: McGraw-Hill, 2008.          **!      
      !**                                                                      **!
      !** Situação: (26-10-2016) OK                                            **!
      !**                                                                      **!
      !**************************************************************************!
      DOUBLE PRECISION a(n,n) ! matriz dos coeficientes
      DOUBLE PRECISION s(n)   ! vetor que guarda o maior valor da linha
      INTEGER          n      ! dimensão do sistema
      DOUBLE PRECISION b(n)   ! vetor de termos independentes  
      DOUBLE PRECISION x(n)   ! vetor solução
      DOUBLE PRECISION tol    ! tolerância
      INTEGER          er     ! -1, indica que houve erro
      INTEGER          i,j,k  ! contador
      DOUBLE PRECISION fator
      !
      ! Iniciando a eliminação
      DO k=1,n-1
          !
          ! Verificação do pivot
          call pivot(a,b,s,n,k)
          !
          ! Testando pivot zero ou próximo de zero
          if (abs(a(k,k)/s(k)).LT.tol) then
              er = -1
              return
          endif
          !
          ! Divide a linha pelo fator
          do i=k+1,n
              fator = a(i,k)/a(k,k)
              do j=k+1,n
                  a(i,j) = a(i,j)-fator*a(k,j)
              enddo
              b(i) = b(i)-fator*b(k)
          enddo
      enddo
      !
      ! Testando pivot zero ou próximo de zero
      if (abs(a(k,k)/s(k)).LT.tol) then
          er=-1
      endif
      
      end
      
      subroutine pivot(a,b,s,n,k)
      !**************************************************************************!
      !** Subrotina: pivot                                                     **!
      !**                                                                      **!
      !** Objetivo: faz a troca de linhas para evitar pivot negativo ou zero   **!
      !**                                                                      **!
      !** Referencia: CHAPRA, S. C.; CANALE, R. P. Métodos numéricos para      **!
      !**             engenharia. 5.ed, São Paulo: McGraw-Hill, 2008.          **!      
      !**                                                                      **!
      !** Situação: (26-10-2016) OK                                            **!
      !**                                                                      **!
      !**************************************************************************!      
      DOUBLE PRECISION a(n,n) ! matriz dos coeficientes
      DOUBLE PRECISION b(n)   ! vetor de termos independentes  
      DOUBLE PRECISION x(n)   ! vetor solução
      DOUBLE PRECISION s(n)   ! vetor que guarda o maior valor da linha 
      INTEGER          n      ! dimensão do sistema
      INTEGER          k,p    ! auxiliar
      INTEGER          ii,jj  ! contador
      DOUBLE PRECISION dummy  ! auxiliar
      DOUBLE PRECISION maior  ! auxiliar
      !
      ! Identificando o maior da linha
      p=k
      maior = abs(a(k,k)/s(k))
      DO ii=k+1,n
          dummy = abs(a(ii,k)/s(ii))
          if (dummy.GT.maior) then
              maior = dummy
              p=ii
          endif
      enddo
      !
      ! Trocando a linha para ter o maior pivot
      if (p.NE.k) then
          do jj=k,n
              dummy = a(p,jj)
              a(p,jj) = a(k,jj)
              a(k,jj) = dummy
          enddo
          dummy = b(p)
          b(p)=b(k)
          b(k) = dummy
          dummy = s(p)
          s(p) = s(k)
          s(k) = dummy
      endif
      !
      End
      
      subroutine substitute(a,n,b,x)
      !**************************************************************************!
      !** Subrotina: substitute                                                **!
      !**                                                                      **!
      !** Objetivo: faz a retrosubstituição do método de Gauss                 **!
      !**                                                                      **!
      !** Referencia: CHAPRA, S. C.; CANALE, R. P. Métodos numéricos para      **!
      !**             engenharia. 5.ed, São Paulo: McGraw-Hill, 2008.          **!      
      !**                                                                      **!
      !** Situação: (26-10-2016) OK                                            **!
      !**                                                                      **!
      !**************************************************************************!           
      DOUBLE PRECISION a(n,n) ! matriz dos coeficientes
      INTEGER          n      ! dimensão do sistema
      DOUBLE PRECISION b(n)   ! vetor de termos independentes  
      DOUBLE PRECISION x(n)   ! vetor solução
      INTEGER          i,j    ! contador
      DOUBLE PRECISION soma   ! auxiliar
      !
      ! Fazendo retrosubstituicao
      x(n) = b(n)/a(n,n)
      do i=n-1,1,-1
          soma = 0.0d0
          do j = i+1,n
              soma = soma+a(i,j)*x(j)
          enddo
          x(i) = (b(i)-soma)/a(i,i)
      enddo
      !
      end
      
      subroutine matinv(n,a,ainv)
      !**************************************************************************!
      !** Subrotina: matinv                                                    **!
      !**                                                                      **!
      !** Objetivo: inverte uma matriz pela técnica de pivotamento             **!
      !**                                                                      **!
      !** Situação: (26-10-2016) OK                                            **!
      !**                                                                      **!
      !**************************************************************************!           
      INTEGER          n          ! dimensão do sistema
      DOUBLE PRECISION a(n,n)     ! matriz dos coeficientes
      DOUBLE PRECISION ainv(n,n)  ! matriz inversa  
      DOUBLE PRECISION b(n,2*n)   ! matriz aumentada
      DOUBLE PRECISION pivot      ! pivô
      DOUBLE PRECISION xnum       ! auxiliar
      INTEGER          i,j,k      ! contador
      !
      ! Fazer matriz aumentada
      do i=1,n
          do j=1,n
              b(i,j) = 0.0d0
              b(i,j+n) = 0.0d0
              b(i,j)=a(i,j)
              if(i.eq.j)then
                  b(i,j+n)=1.0d0
              endif
          enddo
      enddo
      !
      do i=1,n
          ! Escolher o elemento não nulo mais a esquerda como pivot
          do j=1,n
              if (dabs(b(i,j)).gt.0.0d0)then
                  pivot=b(i,j)
                  exit
              endif
          enddo
          !
          ! Passo 1: alterar o pivo escolhido para 1 dividindo a linha do pivo pelo valor do pivo
          do j=1,2*n
              b(i,j)=b(i,j)/pivot
          enddo
          pivot=b(i,i)
          !
          ! Passo 2: mudando o restante da coluno do pivo para 0, 
c adicionando a cada linha um multiplo adequado do pivot
          do k=1,n
              if(k.ne.i)then
                  xnum=b(k,i)/pivot
                  do j=1,2*n
                      b(k,j)=b(k,j)-xnum*b(i,j)
                  enddo
              endif
          enddo
      enddo
      !
      ! Prepara a matriz inversa final
      do i=1,n
          do j=1,n
              ainv(i,j)=b(i,j+n)
          enddo
      enddo
      return        
      end
    
      subroutine jacobi(vect,n,np,d,v,nrot)
      !**************************************************************************!
      !** Subrotina: jacobi                                                    **!
      !**                                                                      **!
      !** Objetivo: encontra os autovalores e autovetores de uma matriz Anxn   **!
      !**           simétrica Anxn através do método de Jacobi                 **!
      !**                                                                      **!
      !** Referencia: PRESS, W.H.; TEUKOLSKY, S.A.; VETTERLING, W.T.; FLANNERY **!
      !**             B.P. Numerical Recipes in Fortran 77. 2ed. V1. 1997.     **!      
      !**                                                                      **!
      !** Situação: (08-01-2017) OK                                            **!
      !**                                                                      **!
      !**************************************************************************!
      !
      INTEGER          n                              ! tamanho da matriz
      INTEGER          np                             ! tamanho do array que armazena a matriz
      INTEGER          nrot                           ! numero de rotações
      INTEGER          nmax                           ! tamanho máximo da matriz
      PARAMETER        (nmax = 500)                   ! define tamanho máximo 500
      DOUBLE PRECISION vect(6)                        ! vetor com as componentes de tensao
      DOUBLE PRECISION a(np,np)                       ! matriz
      DOUBLE PRECISION d(np)                          ! vetor contendo os autovalores da matriz a
      DOUBLE PRECISION v(np,np)                       ! matriz contendo os autovetores da matriz a
      INTEGER          i,ip,iq,j                      ! contadores
      DOUBLE PRECISION c,g,h,s,sm,t,tau,theta,tresh   ! auxiliares
      DOUBLE PRECISION b(nmax),z(nmax)                ! vetores auxiliares
      !
      ! montando a matriz
      a(1,1) = vect(1)
      a(2,2) = vect(2)
      a(3,3) = vect(3)
      a(1,2) = vect(4)
      a(1,3) = vect(5)
      a(2,3) = vect(6)
      a(2,1) = a(1,2)
      a(3,1) = a(1,3)
      a(3,2) = a(2,3)
      !
      ! Inicializando para a matriz identidade
      do ip=1,n
          do iq=1,n
              v(ip,iq)=0d0
          enddo
          v(ip,ip)=1
      enddo
      !
      ! Inicializando b e d para a diagonal de a
      do ip=1,n
          b(ip)=a(ip,ip)
          d(ip)=b(ip)
          z(ip)=0d0
      enddo
      !
      nrot=0
      !
      do i=1,50
          !
          ! Soma dos elementos fora da diagonal
          sm=0
          do ip=1,n-1
              do iq=ip+1,n
                  sm=sm+abs(a(ip,iq))
              enddo
          enddo
          !
          if (sm.eq.0d0) then 
              return
          endif
          !
          if (i.LT.4) then
              tresh = 0.2*sm/n**2
          else
              tresh=0d0
          endif
          !
          do ip=1,n-1
              do iq=ip+1,n
                  g=100d0*abs(a(ip,iq))
                  !
                  ! Após quatro varreduras, pula a rotação se o elemento fora da diagonal é pequeno
                  if((i.GT.4).AND.(abs(d(ip))+g.EQ.abs(d(ip))
     & .AND.(abs(d(iq))+g.EQ.abs(d(iq))))) then
                      a(ip,iq)=0d0
                  else if(abs(a(ip,iq)).GT.tresh) then
                      h=d(iq)-d(ip)
                      if (abs(h)+g.eq.abs(h)) then
                          t=a(ip,iq)/h
                      else
                          theta=0.5*h/a(ip,iq)
                          t=1d0/(abs(theta)+sqrt(1d0+theta**2))
                          if (theta.LT.0d0) t=-t
                      endif
                      c=1d0/sqrt(1+t**2)
                      s=t*c
                      tau=s/(1d0+c)
                      h=t*a(ip,iq)
                      z(ip)=z(ip)-h
                      z(iq)=z(iq)+h
                      d(ip)=d(ip)-h
                      d(iq)=d(iq)+h
                      a(ip,iq)=0d0
                      do j=1,ip-1
                          g=a(j,ip)
                          h=a(j,iq)
                          a(j,ip)=g-s*(h+g*tau)
                          a(j,iq)=h+s*(g-h*tau)
                      enddo
                      do j=ip+1,iq-1
                          g=a(ip,j)
                          h=a(j,iq)
                          a(ip,j)=g-s*(h+g*tau)
                          a(j,iq)=h+s*(g-h*tau)
                      enddo
                      do j=iq+1,n
                          g=a(ip,j)
                          h=a(iq,j)
                          a(ip,j)=g-s*(h+g*tau)
                          a(iq,j)=h+s*(g-h*tau)
                      enddo
                      do j=1,n
                          g=v(j,ip)
                          h=v(j,iq)
                          v(j,ip)=g-s*(h+g*tau)
                          v(j,iq)=h+s*(g-h*tau)
                      enddo                  
                      nrot=nrot+1
                  endif
              enddo
          enddo
          do ip=1,n
              b(ip)=b(ip)+z(ip)
              d(ip)=b(ip)
              z(ip)=0d0
          enddo
      enddo
      return
      !
      end subroutine
               
      subroutine eigsrt(d,v,n,np)
      !**************************************************************************!
      !** Subrotina: eigsrt                                                    **!
      !**                                                                      **!
      !** Objetivo: ordena os autovalores e autovetores                        **!
      !**                                                                      **!
      !** Referencia: PRESS, W.H.; TEUKOLSKY, S.A.; VETTERLING, W.T.; FLANNERY **!
      !**             B.P. Numerical Recipes in Fortran 77. 2ed. V1. 1997.     **!
      !**                                                                      **!
      !** Situação: (08-01-2017) OK                                            **!
      !**                                                                      **!
      !**************************************************************************!
      !      
      INTEGER          n,np       ! dimensão da matriz
      DOUBLE PRECISION d(np)      ! vetor contendo os autovalores
      DOUBLE PRECISION v(np,np)   ! matriz contendo os autovetores
      INTEGER          i,j,k      ! contador
      DOUBLE PRECISION p          ! auxiliar
      !
      do i=1,n-1
          k=i
          p=d(i)
          do j=i+1,n
              if(d(j).GE.p) then
                  k=j
                  p=d(j)
              endif
          enddo
          if(k.NE.i)then
              d(k)=d(i)
              d(i)=p
              do j=1,n
                  p=v(j,i)
                  v(j,i)=v(j,k)
                  v(j,k)=p
              enddo
          endif
      enddo
      return
      end subroutine     