        !COMPILER-GENERATED INTERFACE MODULE: Fri Sep 29 17:56:22 2023
        ! This source file is for reference only and may not completely
        ! represent the generated interface used by the compiler.
        MODULE NORMATENSOR__genmod
          INTERFACE 
            SUBROUTINE NORMATENSOR(TENSOR,NCOMP,NORMA)
              INTEGER(KIND=4) :: NCOMP
              REAL(KIND=8) :: TENSOR(NCOMP)
              REAL(KIND=8) :: NORMA
            END SUBROUTINE NORMATENSOR
          END INTERFACE 
        END MODULE NORMATENSOR__genmod
