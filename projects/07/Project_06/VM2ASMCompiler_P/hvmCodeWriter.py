"""
hvmCodeWriter.py -- Code Writer class for Hack VM translator
"""

import os
from hvmCommands import *

debug = False

class CodeWriter(object):
    
    def __init__(self, outputName):
        """
        Open 'outputName' and gets ready to write it.
        """
        self.file = open(outputName, 'w')
        self.SetFileName(outputName)

        self.labelNumber = 0
        self.returnLabel = None
        self.callLabel = None
        self.cmpLabels = {}
        self.needHalt = True


    def Debug(self, value):
        """
        Set debug mode.
        Debug mode writes useful comments in the output stream.
        """
        global debug
        debug = value


    def Close(self):
        """
        Write a jmp $ and close the output file.
        """
        if self.needHalt:
            if debug:
                self.file.write('    // <halt>\n')
            label = self._UniqueLabel()
            self._WriteCode('@%s, (%s), 0;JMP' % (label, label))
        self.file.close()


    def SetFileName(self, fileName):
        """
        Sets the current file name to 'fileName'.
        Restarts the local label counter.

        Strips the path and extension.  The resulting name must be a
        legal Hack Assembler identifier.
        """
        if (debug):
            self.file.write('    // File: %s\n' % (fileName))
        self.fileName = os.path.basename(fileName)
        self.fileName = os.path.splitext(self.fileName)[0]
        self.functionName = None


    def Write(self, line):
        """
        Raw write for debug comments.
        """
        self.file.write(line + '\n')

    def _UniqueLabel(self):
        """
        Make a globally unique label.
        The label will be _sn where sn is an incrementing number.
        """
        self.labelNumber += 1
        return '_' + str(self.labelNumber)


    def _LocalLabel(self, name):
        """
        Make a function/module unique name for the label.
        If no function has been entered, the name will be
        FileName$$name. Otherwise it will be FunctionName$name.
        """
        if self.functionName != None:
            return self.functionName + '$' + name
        else:
            return self.fileName + '$$' + name


    def _StaticLabel(self, index):
        """
        Make a name for static variable 'index'.
        The name will be FileName.index
        """
        return self.fileName + '.' + str(index)    


    def _WriteCode(self, code):
        """
        Write the comma separated commands in 'code'.
        """
        code = code.replace(',', '\n').replace(' ', '')
        self.file.write(code + '\n')
        



    def WritePushPop(self, commandType, segment, index):
        """
        Write Hack code for 'commandType' (C_PUSH or C_POP).
        'segment' (string) is the segment name.
        'index' (int) is the offset in the segment.
	To be implemented as part of Project 6
	
	    For push: Pushes the content of segment[index] onto the stack. It is a good idea to move the value to be pushed into a register first, then push the content of the register to the stack.
        For pop: Pops the top of the stack into segment[index]. You may need to use a general purpose register (R13-R15) to store some temporary results.
        Hint: Recall that there are 8 memory segments in the VM model, but only 5 of these exist in the assembly definition. Also, not all 8 VM segments allow to perform both pop and push on them. Chapter 7.3 of the book explains memory segment mapping.
        Hint: Use pen and paper first. Figure out how to compute the address of segment[index] (except for constant). Then figure out how you move the value of segment[index] into a register (by preference D). Then figure out how to push a value from a register onto the stack. 
        Hint: For pop, you already know how to compute the address of segment[index]. Store it in a temporary register (you can use R13 to R15 freely). Then read the value from the top of the stack, adjust the top of the stack, and then store the value at the location stored in the temporary register.
    
    PUSH constant is implemented as an example. Other solutions are possible too.

        """
        if commandType == C_PUSH: #We add something to the stack
            if segment == 'constant':
                code = "@" + index + "," 
                code += "D=A,"
                code += "@SP," # SP is the adrees for 0 in the RAM, so @SP is @0
                code += "A=M,"
                code += "M=D," # we put the value of D in the RAM at the address stored in SP, which is the top of the stack
                code += "@SP,"
                code += "M=M+1" # stack pointer is incremented
                self._WriteCode(code)
            elif segment in ('local', 'argument', 'this', 'that'):
                if segment == 'local':
                    base = 'LCL'
                elif segment == 'argument':
                    base = 'ARG'
                elif segment == 'this':
                    base = 'THIS'
                elif segment == 'that':
                    base = 'THAT'
                code = "@" + index + ","
                code += "D=A,"
                code += "@" + base + ","
                code += "A=M+D,"
                code += "D=M,"
                code += "@SP,"
                code += "A=M,"
                code += "M=D,"
                code += "@SP,"
                code += "M=M+1"
                self._WriteCode(code)
            elif segment == 'temp':
                code = "@" + index + ","
                code += "D=A,"
                code += "@5,"
                code += "A=A+D,"
                code += "D=M,"
                code += "@SP,"
                code += "A=M,"
                code += "M=D,"
                code += "@SP,"
                code += "M=M+1"
                self._WriteCode(code)
            elif segment == 'pointer':
                if index == '0':
                    base = 'THIS'
                elif index == '1':
                    base = 'THAT'
                code = "@" + base + ","
                code += "D=M,"
                code += "@SP,"
                code += "A=M,"
                code += "M=D,"
                code += "@SP,"
                code += "M=M+1"
                self._WriteCode(code)
            elif segment == 'static':
                code = "@" + self._StaticLabel(index) + ","
                code += "D=M,"
                code += "@SP,"
                code += "A=M,"
                code += "M=D,"
                code += "@SP,"
                code += "M=M+1"
                self._WriteCode(code)
        elif commandType == C_POP: #We remove something from the stack
            if segment in ('local', 'argument', 'this', 'that'):
                if segment == 'local':
                    base = 'LCL'
                elif segment == 'argument':
                    base = 'ARG'
                elif segment == 'this':
                    base = 'THIS'
                elif segment == 'that':
                    base = 'THAT'
                code = "@" + index + ","
                code += "D=A,"
                code += "@" + base + ","
                code += "D=M+D,"
                code += "@R13,"
                code += "M=D,"
                code += "@SP,"
                code += "AM=M-1,"
                code += "D=M,"
                code += "@R13,"
                code += "A=M,"
                code += "M=D"
                self._WriteCode(code)
            elif segment == 'temp':
                code = "@" + index + ","
                code += "D=A,"
                code += "@5,"
                code += "D=A+D,"
                code += "@R13,"
                code += "M=D,"
                code += "@SP,"
                code += "AM=M-1,"
                code += "D=M,"
                code += "@R13,"
                code += "A=M,"
                code += "M=D"
                self._WriteCode(code)
            elif segment == 'pointer':
                if index == '0':
                    base = 'THIS'
                elif index == '1':
                    base = 'THAT'
                code = "@SP, AM=M-1, D=M, @" + base + ", M=D"
                self._WriteCode(code)
            elif segment == 'static':
                code = "@SP, AM=M-1, D=M, @" + self._StaticLabel(index) + ", M=D"
                self._WriteCode(code)
            


    def WriteArithmetic(self, command):
        """
        Write Hack code for stack arithmetic 'command' (str).
    To be implemented as part of Project 6
        
        Compiles the arithmetic VM command into the corresponding ASM code. Recall that the operands (one or two, depending on the command) are on the stack and the result of the operation should be placed on the stack.
        The unary and the logical and arithmetic binary operators are simple to compile. 
         The three comparison operators (EQ, LT and GT) do not exist in the assembly language. The corresponding assembly commands are the conditional jumps JEQ, JLT and JGT. You need to implement the VM operations using these conditional jumps. You need two labels, one for the true condition and one for the false condition and you have to put the correct result on the stack.
        """
        
        if command in (T_ADD, T_SUB, T_AND, T_OR):
            if command == T_ADD:
                comp = 'M+D'
            elif command == T_SUB:
                comp = 'M-D'
            elif command == T_AND:
                comp = 'M&D'
            elif command == T_OR:
                comp = 'M|D'
            code = "@SP, AM=M-1, D=M, A=A-1, M=" + comp
            self._WriteCode(code)
        elif command in (T_NEG, T_NOT):
            if command == T_NEG:
                comp = '-M'
            elif command == T_NOT:
                comp = '!M'
            code = "@SP, A=M-1, M=" + comp
            self._WriteCode(code)
        elif command in (T_EQ, T_GT, T_LT):
            if command == T_EQ:
                jump = 'JEQ'
            elif command == T_GT:
                jump = 'JGT'
            elif command == T_LT:
                jump = 'JLT'
            labelTrue = self._UniqueLabel()
            labelEnd = self._UniqueLabel()
            code = "@SP, AM=M-1, D=M, A=A-1, D=M-D, @" + labelTrue + ", D;" + jump + ","
            code += "@SP, A=M-1, M=0, @" + labelEnd + ", 0;JMP,"
            code += "(" + labelTrue + "), @SP, A=M-1, M=-1,"
            code += "(" + labelEnd + ")"
            self._WriteCode(code)
        
            

        
        
    def WriteInit(self, sysinit = True):
        """
        Write the VM initialization code:
    To be implemented as part of Project 7
        """
        if (debug):
            self.file.write('    // Initialization code\n')
        if sysinit:
            code = '@256, D=A, @SP, M=D'
            self._WriteCode(code)
            self.WriteCall('Sys.init', '0')
            

    def WriteLabel(self, label):
        """
        Write Hack code for 'label' VM command.
	To be implemented as part of Project 7

        """
        self._WriteCode('(%s)' % self._LocalLabel(label))

    def WriteGoto(self, label):
        """
        Write Hack code for 'goto' VM command.
	To be implemented as part of Project 7
        """
        self._WriteCode('@%s, 0;JMP' % self._LocalLabel(label))

        

    def WriteIf(self, label):
        """
        Write Hack code for 'if-goto' VM command.
	To be implemented as part of Project 7
        """
        self._WriteCode('@SP, AM=M-1, D=M, @%s, D;JNE' % self._LocalLabel(label))

        

    def WriteFunction(self, functionName, numLocals):
        """
        Write Hack code for 'function' VM command.
	To be implemented as part of Project 7
        """
        self.functionName = functionName
        code = '(%s)' % functionName
        for i in range(int(numLocals)):
            code += ', @0, D=A, @SP, A=M, M=D, @SP, M=M+1'
        self._WriteCode(code)
            
            
    def WriteReturn(self):
        """
        Write Hack code for 'return' VM command.
	To be implemented as part of Project 7
        """
        code = '@LCL, D=M, @R13, M=D,'
    
        # RET = *(FRAME - 5) (store return address in R14)
        code += '@5, A=D-A, D=M, @R14, M=D,'
        
        # *ARG = pop() (put return value at ARG[0])
        code += '@SP, AM=M-1, D=M, @ARG, A=M, M=D,'
        
        # SP = ARG + 1
        code += '@ARG, D=M+1, @SP, M=D,'
        
        # THAT = *(FRAME - 1)
        code += '@R13, AM=M-1, D=M, @THAT, M=D,'
        
        # THIS = *(FRAME - 2)
        code += '@R13, AM=M-1, D=M, @THIS, M=D,'
        
        # ARG = *(FRAME - 3)
        code += '@R13, AM=M-1, D=M, @ARG, M=D,'
        
        # LCL = *(FRAME - 4)
        code += '@R13, AM=M-1, D=M, @LCL, M=D,'
        
        # goto RET
        code += '@R14, A=M, 0;JMP'
    
        self._WriteCode(code)

    def WriteCall(self, functionName, numArgs):
        """
        Write Hack code for 'call' VM command.
	To be implemented as part of Project 7
        """
        returnLabel = self._UniqueLabel()
    
        # Push return address
        code = '@%s, D=A, @SP, A=M, M=D, @SP, M=M+1,' % returnLabel
        
        # Push LCL
        code += '@LCL, D=M, @SP, A=M, M=D, @SP, M=M+1,'
        
        # Push ARG
        code += '@ARG, D=M, @SP, A=M, M=D, @SP, M=M+1,'
        
        # Push THIS
        code += '@THIS, D=M, @SP, A=M, M=D, @SP, M=M+1,'
        
        # Push THAT
        code += '@THAT, D=M, @SP, A=M, M=D, @SP, M=M+1,'
        
        # ARG = SP - numArgs - 5, 5 because we have pushed 5 values onto the stack
        code += '@SP, D=M, @%s, D=D-A, @5, D=D-A, @ARG, M=D,' % numArgs
        
        # LCL = SP
        code += '@SP, D=M, @LCL, M=D,'
        
        # Jump to function
        code += '@%s, 0;JMP,' % functionName
        
        # Declare return label
        code += '(%s)' % returnLabel
        
        self._WriteCode(code)

    
