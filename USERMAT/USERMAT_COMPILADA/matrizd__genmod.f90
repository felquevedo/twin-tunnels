        !COMPILER-GENERATED INTERFACE MODULE: Mon Sep 25 09:49:25 2023
        ! This source file is for reference only and may not completely
        ! represent the generated interface used by the compiler.
        MODULE MATRIZD__genmod
          INTERFACE 
            SUBROUTINE MATRIZD(E,POISSON,NCOMP,D)
              INTEGER(KIND=4) :: NCOMP
              REAL(KIND=8) :: E
              REAL(KIND=8) :: POISSON
              REAL(KIND=8) :: D(NCOMP,NCOMP)
            END SUBROUTINE MATRIZD
          END INTERFACE 
        END MODULE MATRIZD__genmod
