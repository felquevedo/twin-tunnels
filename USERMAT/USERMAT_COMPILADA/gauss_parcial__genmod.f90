        !COMPILER-GENERATED INTERFACE MODULE: Sun Aug 27 22:54:56 2023
        ! This source file is for reference only and may not completely
        ! represent the generated interface used by the compiler.
        MODULE GAUSS_PARCIAL__genmod
          INTERFACE 
            SUBROUTINE GAUSS_PARCIAL(A,B,N,X,TOL,ER)
              INTEGER(KIND=4) :: N
              REAL(KIND=8) :: A(N,N)
              REAL(KIND=8) :: B(N)
              REAL(KIND=8) :: X(N)
              REAL(KIND=8) :: TOL
              INTEGER(KIND=4) :: ER
            END SUBROUTINE GAUSS_PARCIAL
          END INTERFACE 
        END MODULE GAUSS_PARCIAL__genmod
