        !COMPILER-GENERATED INTERFACE MODULE: Fri Sep 29 17:56:22 2023
        ! This source file is for reference only and may not completely
        ! represent the generated interface used by the compiler.
        MODULE KELVIN_BETACTT0__genmod
          INTERFACE 
            SUBROUTINE KELVIN_BETACTT0(NKELVIN,T0,TINF,NDEC,NDT,TAU,EMU,&
     &TEMP,RH,HF)
              INTEGER(KIND=4) :: NDT
              INTEGER(KIND=4) :: NKELVIN
              REAL(KIND=8) :: T0
              REAL(KIND=8) :: TINF
              INTEGER(KIND=4) :: NDEC
              REAL(KIND=8) :: TAU(NKELVIN)
              REAL(KIND=8) :: EMU(NKELVIN)
              REAL(KIND=8) :: TEMP
              REAL(KIND=8) :: RH
              REAL(KIND=8) :: HF
            END SUBROUTINE KELVIN_BETACTT0
          END INTERFACE 
        END MODULE KELVIN_BETACTT0__genmod
