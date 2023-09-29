        !COMPILER-GENERATED INTERFACE MODULE: Mon Sep 25 09:49:25 2023
        ! This source file is for reference only and may not completely
        ! represent the generated interface used by the compiler.
        MODULE ELIMINATE__genmod
          INTERFACE 
            SUBROUTINE ELIMINATE(A,S,N,B,TOL,ER)
              INTEGER(KIND=4) :: N
              REAL(KIND=8) :: A(N,N)
              REAL(KIND=8) :: S(N)
              REAL(KIND=8) :: B(N)
              REAL(KIND=8) :: TOL
              INTEGER(KIND=4) :: ER
            END SUBROUTINE ELIMINATE
          END INTERFACE 
        END MODULE ELIMINATE__genmod
