// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
    @R0
    D=M
    @R1
    D=D-M       // D = R0 - R1
    @NOSWAP
    D;JLE       // if R0 <= R1 no swap needed

    // swap R0 and R1 using R3 as temp
    @R0
    D=M
    @R3
    M=D         // R3 = R0
    @R1
    D=M
    @R0
    M=D         // R0 = R1
    @R3
    D=M
    @R1
    M=D         // R1 = R3

(NOSWAP)
    // R2 = 0, i = 0
    @R2
    M=0
    @i
    M=0

(LOOP)
    // if i >= R0 goto END
    @i
    D=M
    @R0
    D=D-M       // D = i - R0
    @END
    D;JGE       // if i >= R0 done

    // R2 = R2 + R1
    @R1
    D=M
    @R2
    M=D+M       // R2 += R1

    // i++
    @i
    M=M+1

    @LOOP
    0;JMP

(END)
    @END
    0;JMP