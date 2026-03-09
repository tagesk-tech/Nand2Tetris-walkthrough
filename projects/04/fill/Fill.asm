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

(MAINLOOP)
    // Check keyboard
    @KBD
    D=M         // D = keyboard value
    @FILL      // fetch adress for Fill
    D;JGT       // if D > 0 (key pressed) goto FILL
    @CLEAR
    0;JMP       // else goto CLEAR

(FILL)
    @SCREEN
    D=A         // D = base address of screen
    @ptr
    M=D         // ptr = SCREEN

(FILLLOOP)
    @ptr
    A=M         // A = current screen address
    M=-1        // blacken 16 pixels

    @ptr
    M=M+1       // ptr++

    @8192
    D=A         // D = 8192
    @SCREEN
    D=D+A       // D = SCREEN + 8192 (end of screen)
    @ptr
    D=D-M       // D = end - ptr
    @FILLLOOP
    D;JGT       // if ptr < end keep looping

    @MAINLOOP
    0;JMP

(CLEAR)
    @SCREEN
    D=A
    @ptr
    M=D         // ptr = SCREEN

(CLEARLOOP)
    @ptr
    A=M         // A = current screen address
    M=0         // clear 16 pixels

    @ptr
    M=M+1       // ptr++

    @8192
    D=A
    @SCREEN
    D=D+A       // D = SCREEN + 8192
    @ptr
    D=D-M
    @CLEARLOOP
    D;JGT       // if ptr < end keep looping

    @MAINLOOP
    0;JMP