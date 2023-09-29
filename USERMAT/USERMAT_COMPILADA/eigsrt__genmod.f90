        !COMPILER-GENERATED INTERFACE MODULE: Fri Sep 29 17:56:22 2023
        ! This source file is for reference only and may not completely
        ! represent the generated interface used by the compiler.
        MODULE EIGSRT__genmod
          INTERFACE 
            SUBROUTINE EIGSRT(D,V,N,NP)
              INTEGER(KIND=4) :: NP
              REAL(KIND=8) :: D(NP)
              REAL(KIND=8) :: V(NP,NP)
              INTEGER(KIND=4) :: N
            END SUBROUTINE EIGSRT
          END INTERFACE 
        END MODULE EIGSRT__genmod
