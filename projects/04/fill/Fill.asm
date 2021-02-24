// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(LOOP)
    @24576 // Keyboard input
    D=M
    @BLACK
    D;JGT
(WHITE)
    @0
    M=A // R0 = 0
(WHITELOOP)
    @0
    D=M
    @16384 // screen start memory
    A=A+D // A = A + R0
    D=0 // set every bit to 0
    M=D
    @0
    MD=M+1
    @8192 // 32 (words per line) * 256 lines
    D=A-D
    @WHITELOOP
    D;JNE
    @LOOP
    0;JMP
(BLACK)
    @0
    M=A // R0 = 0
(BLACKLOOP)
    @0 
    D=M
    @16384
    A=A+D // A = A + R0
    D=-1 // set every bit to 1
    M=D
    @0
    MD=M+1
    @8192 // 32 (words per line) * 256 lines
    D=A-D
    @BLACKLOOP
    D;JNE
    @LOOP
    0;JMP