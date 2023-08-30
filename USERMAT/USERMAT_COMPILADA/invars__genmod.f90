        !COMPILER-GENERATED INTERFACE MODULE: Sun Aug 27 22:54:56 2023
        ! This source file is for reference only and may not completely
        ! represent the generated interface used by the compiler.
        MODULE INVARS__genmod
          INTERFACE 
            SUBROUTINE INVARS(STRESS,NCOMP,I1,J2,J3,THETA,S)
              INTEGER(KIND=4) :: NCOMP
              REAL(KIND=8) :: STRESS(NCOMP)
              REAL(KIND=8) :: I1
              REAL(KIND=8) :: J2
              REAL(KIND=8) :: J3
              REAL(KIND=8) :: THETA
              REAL(KIND=8) :: S(6)
            END SUBROUTINE INVARS
          END INTERFACE 
        END MODULE INVARS__genmod
