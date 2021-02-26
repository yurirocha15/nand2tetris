// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

//     @0
//     D=A
//     @END
//     R1;JEQ
// (LOOP)
//     D=D+R0
//     R1=R1-1
//     @LOOP
//     R1;JGT
// (END)
//     R2=D

// Put your code here.
    @1
    D=M
    @i
    M=D // i = R1
    @0
    D=A
    @2
    M=D // Initialize R2 = 0
    @1
    D=M // Load R1
    @END
    D;JEQ // END if R1 == 0
(LOOP)
    @0
    D=M // Load R0
    @2
    M=D+M // R2 = D + R2
    @i
    MD=M-1 // D = i = i - 1
    @LOOP
    D;JGT // While i > 0
(END)