        !COMPILER-GENERATED INTERFACE MODULE: Fri Sep 29 17:56:22 2023
        ! This source file is for reference only and may not completely
        ! represent the generated interface used by the compiler.
        MODULE JACOBI__genmod
          INTERFACE 
            SUBROUTINE JACOBI(VECT,N,NP,D,V,NROT)
              INTEGER(KIND=4) :: NP
              REAL(KIND=8) :: VECT(6)
              INTEGER(KIND=4) :: N
              REAL(KIND=8) :: D(NP)
              REAL(KIND=8) :: V(NP,NP)
              INTEGER(KIND=4) :: NROT
            END SUBROUTINE JACOBI
          END INTERFACE 
        END MODULE JACOBI__genmod
