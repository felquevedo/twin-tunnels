        !COMPILER-GENERATED INTERFACE MODULE: Fri Sep 29 17:56:22 2023
        ! This source file is for reference only and may not completely
        ! represent the generated interface used by the compiler.
        MODULE MATINV__genmod
          INTERFACE 
            SUBROUTINE MATINV(N,A,AINV)
              INTEGER(KIND=4) :: N
              REAL(KIND=8) :: A(N,N)
              REAL(KIND=8) :: AINV(N,N)
            END SUBROUTINE MATINV
          END INTERFACE 
        END MODULE MATINV__genmod
