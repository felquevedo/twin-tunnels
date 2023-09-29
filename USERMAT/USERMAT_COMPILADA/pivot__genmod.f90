        !COMPILER-GENERATED INTERFACE MODULE: Mon Sep 25 09:49:25 2023
        ! This source file is for reference only and may not completely
        ! represent the generated interface used by the compiler.
        MODULE PIVOT__genmod
          INTERFACE 
            SUBROUTINE PIVOT(A,B,S,N,K)
              INTEGER(KIND=4) :: N
              REAL(KIND=8) :: A(N,N)
              REAL(KIND=8) :: B(N)
              REAL(KIND=8) :: S(N)
              INTEGER(KIND=4) :: K
            END SUBROUTINE PIVOT
          END INTERFACE 
        END MODULE PIVOT__genmod
