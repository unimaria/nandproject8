
def pushstack():
    return 'D=M\n' \
           '@SP\n' \
           'A=M\n' \
           'M=D\n' \
           '@SP\n' \
           'M=M+1\n'

def popstack(str):
    return '@SP\n' \
           'AM=M-1\n' \
           'D=M\n' \
           '@' + str + '\n' \
           'M=D\n'

def eqstr(i, f):
    if f is None:
        return '@SP\n' \
            'AM = M - 1\n' \
            'D = M\n' \
            '@R13\n' \
            'M = -1\n' \
            '@POS1' + str(i) + '\n' \
            'D;JGT\n' \
            '@R13\n' \
            'M = 0\n' \
            '(POS1' + str(i) + ')\n' \
            '@SP\n' \
            'A = M - 1\n' \
            'D = M\n' \
            '@R14\n' \
            'M = -1\n' \
            '@POS2' + str(i) + '\n' \
            'D;JGT\n' \
            '@R14\n' \
            'M = 0\n' \
            '(POS2' + str(i) + ')\n' \
            '@R14\n' \
            'D = M\n' \
            '@R13\n' \
            'D = M - D\n' \
            '@OVERFLOW' + str(i) + '\n' \
            'D;JNE\n' \
            '@SP\n' \
            'A = M\n' \
            'D = M\n' \
            '@SP\n' \
            'A = M - 1\n' \
            'D = D - M\n' \
            '@TRUE' + str(i) + '\n' \
            'D;JEQ\n' \
            '@SP\n' \
            'A = M - 1\n' \
            'M = 0\n' \
            '@END' + str(i) + '\n' \
            '0;JMP\n' \
            '(TRUE' + str(i) + ')\n' \
            '@SP\n' \
            'A = M - 1\n' \
            'M = -1\n' \
            '@END' + str(i) + '\n' \
            '0;JMP\n' \
            '(OVERFLOW' + str(i) + ')\n' \
            '@SP\n' \
            'A = M - 1\n' \
            'M = 0\n' \
            '(END' + str(i) + ')\n'
    else:
        return '@SP\n' \
            'AM = M - 1\n' \
            'D = M\n' \
            '@R13\n' \
            'M = -1\n' \
            '@' + f + '$POS1' + str(i) + '\n' \
            'D;JGT\n' \
            '@R13\n' \
            'M = 0\n' \
            '(' + f + '$POS1' + str(i) + ')\n' \
            '@SP\n' \
            'A = M - 1\n' \
            'D = M\n' \
            '@R14\n' \
            'M = -1\n' \
            '@' + f + '$POS2' + str(i) + '\n' \
            'D;JGT\n' \
            '@R14\n' \
            'M = 0\n' \
            '(' + f + '$POS2' + str(i) + ')\n' \
            '@R14\n' \
            'D = M\n' \
            '@R13\n' \
            'D = M - D\n' \
            '@' + f + '$OVERFLOW' + str(i) + '\n' \
            'D;JNE\n' \
            '@SP\n' \
            'A = M\n' \
            'D = M\n' \
            '@SP\n' \
            'A = M - 1\n' \
            'D = D - M\n' \
            '@' + f + '$TRUE' + str(i) + '\n' \
            'D;JEQ\n' \
            '@SP\n' \
            'A = M - 1\n' \
            'M = 0\n' \
            '@' + f + '$END' + str(i) + '\n' \
            '0;JMP\n' \
            '(' + f + '$TRUE' + str(i) + ')\n' \
            '@SP\n' \
            'A = M - 1\n' \
            'M = -1\n' \
            '@' + f + '$END' + str(i) + '\n' \
            '0;JMP\n' \
            '(' + f + '$OVERFLOW' + str(i) + ')\n' \
            '@SP\n' \
            'A = M - 1\n' \
            'M = 0\n' \
            '(' + f + '$END' + str(i) + ')\n'

def gtstr(i, f):
    if f is None:
        return '@SP\n' \
            'AM = M-1\n' \
            'D = M\n' \
            '@R13\n' \
            'M=-1\n'\
            '@POS1' + str(i) + '\n' \
            'D;JGT\n' \
            '@R13\n' \
            'M=0\n' \
            '(POS1' + str(i) + ')\n' \
            '@SP\n' \
            'A=M-1\n' \
            'D=M\n' \
            '@R14\n' \
            'M=-1\n' \
            '@POS2' + str(i) + '\n' \
            'D;JGT\n' \
            '@R14\n' \
            'M=0\n' \
            '(POS2'+str(i) +')\n' \
            '@R14\n' \
            'D=M\n' \
            '@R13\n' \
            'D=M-D\n' \
            '@OVERFLOW' + str(i) + '\n'\
            'D;JNE\n' \
            '@SP\n'\
            'A=M\n' \
            'D=M\n' \
            '@SP\n' \
            'A=M-1\n' \
            'D=D-M\n' \
            '@TRUE' + str(i) + '\n'\
            'D;JLT\n' \
            '@SP\n'\
            'A=M-1\n'\
            'M=0\n'\
            '@END' + str(i) + '\n' \
            '0;JMP\n' \
            '(TRUE' + str(i) + ')\n' \
            '@SP\n' \
            'A=M-1\n' \
            'M=-1\n'\
            '@END' + str(i) + '\n' \
            '0;JMP\n' \
            '(OVERFLOW' + str(i) + ')\n' \
            '@R14\n' \
            'D=M\n' \
            '@SP\n' \
            'A=M-1\n'\
            'M=D\n' \
            '(END' + str(i) + ')\n'
    else:
        return '@SP\n' \
            'AM = M-1\n' \
            'D = M\n' \
            '@R13\n' \
            'M=-1\n' \
            '@' + f + '$POS1' + str(i) + '\n' \
            'D;JGT\n' \
            '@R13\n' \
            'M=0\n' \
            '(' + f + '$POS1' + str(i) + ')\n' \
            '@SP\n' \
            'A=M-1\n' \
            'D=M\n' \
            '@R14\n' \
            'M=-1\n' \
            '@' + f + '$POS2' + str(i) + '\n' \
            'D;JGT\n' \
            '@R14\n' \
            'M=0\n' \
            '(' + f + '$POS2'+str(i) +')\n' \
            '@R14\n' \
            'D=M\n' \
            '@R13\n' \
            'D=M-D\n' \
            '@' + f + '$OVERFLOW' + str(i) + '\n' \
            'D;JNE\n' \
            '@SP\n' \
            'A=M\n' \
            'D=M\n' \
            '@SP\n' \
            'A=M-1\n' \
            'D=D-M\n' \
            '@' + f + '$TRUE' + str(i) + '\n' \
            'D;JLT\n' \
            '@SP\n' \
            'A=M-1\n' \
            'M=0\n' \
            '@' + f + '$END' + str(i) + '\n' \
            '0;JMP\n' \
            '(' + f + '$TRUE' + str(i) + ')\n' \
            '@SP\n' \
            'A=M-1\n' \
            'M=-1\n' \
            '@' + f + '$END' + str(i) + '\n' \
            '0;JMP\n' \
            '(' + f + '$OVERFLOW' + str(i) + ')\n' \
            '@R14\n' \
            'D=M\n' \
            '@SP\n' \
            'A=M-1\n' \
            'M=D\n' \
            '(' + f + '$END' + str(i) + ')\n'

def ltstr(i, f):
    if f is None:
        return '@SP\n' \
            'AM = M-1\n' \
            'D = M\n' \
            '@R13\n' \
            'M=-1\n' \
            '@POS1' + str(i) + '\n' \
            'D;JGT\n' \
            '@R13\n' \
            'M=0\n' \
            '(POS1' + str(i) + ')\n' \
            '@SP\n' \
            'A=M-1\n' \
            'D=M\n' \
            '@R14\n' \
            'M=-1\n' \
            '@POS2' + str(i) + '\n' \
            'D;JGT\n' \
            '@R14\n' \
            'M=0\n' \
            '(POS2'+str(i) +')\n' \
            '@R14\n' \
            'D=M\n' \
            '@R13\n' \
            'D=M-D\n' \
            '@OVERFLOW' + str(i) + '\n' \
            'D;JNE\n' \
            '@SP\n' \
            'A=M\n' \
            'D=M\n' \
            '@SP\n' \
            'A=M-1\n' \
            'D=D-M\n' \
            '@TRUE' + str(i) + '\n' \
            'D;JGT\n' \
            '@SP\n' \
            'A=M-1\n' \
            'M=0\n' \
            '@END' + str(i) + '\n' \
            '0;JMP\n' \
            '(TRUE' + str(i) + ')\n' \
            '@SP\n' \
            'A=M-1\n' \
            'M=-1\n' \
            '@END' + str(i) + '\n' \
            '0;JMP\n' \
            '(OVERFLOW' + str(i) + ')\n' \
            '@R13\n' \
            'D=M\n' \
            '@SP\n' \
            'A=M-1\n' \
            'M=D\n' \
            '(END' + str(i) + ')\n'
    else:
        return '@SP\n' \
            'AM = M-1\n' \
            'D = M\n' \
            '@R13\n' \
            'M=-1\n' \
            '@' + f + '$POS1' + str(i) + '\n' \
            'D;JGT\n' \
            '@R13\n' \
            'M=0\n' \
            '(' + f + '$POS1' + str(i) + ')\n' \
            '@SP\n' \
            'A=M-1\n' \
            'D=M\n' \
            '@R14\n' \
            'M=-1\n' \
            '@' + f + '$POS2' + str(i) + '\n' \
            'D;JGT\n' \
            '@R14\n' \
            'M=0\n' \
            '(' + f + '$POS2'+str(i) +')\n' \
            '@R14\n' \
            'D=M\n' \
            '@R13\n' \
            'D=M-D\n' \
            '@' + f + '$OVERFLOW' + str(i) + '\n' \
            'D;JNE\n' \
            '@SP\n' \
            'A=M\n' \
            'D=M\n' \
            '@SP\n' \
            'A=M-1\n' \
            'D=D-M\n' \
            '@' + f + '$TRUE' + str(i) + '\n' \
            'D;JGT\n' \
            '@SP\n' \
            'A=M-1\n' \
            'M=0\n' \
            '@' + f + '$END' + str(i) + '\n' \
            '0;JMP\n' \
            '(' + f + '$TRUE' + str(i) + ')\n' \
            '@SP\n' \
            'A=M-1\n' \
            'M=-1\n' \
            '@' + f + '$END' + str(i) + '\n' \
            '0;JMP\n' \
            '(' + f + '$OVERFLOW' + str(i) + ')\n' \
            '@R13\n' \
            'D=M\n' \
            '@SP\n' \
            'A=M-1\n' \
            'M=D\n' \
            '(' + f + '$END' + str(i) + ')\n'

#todo unchanged code
    # def pushstack():
    #     return 'D=M\n' \
    #            '@SP\n' \
    #            'A=M\n' \
    #            'M=D\n' \
    #            '@SP\n' \
    #            'M=M+1\n'
    #
    # def popstack(str):
    #     return '@SP\n' \
    #            'AM=M-1\n' \
    #            'D=M\n' \
    #            '@' + str + '\n' \
    #            'M=D\n'
    #
    # def eqstr(i):
    #     return '@SP\n' \
    #         'AM = M - 1\n' \
    #         'D = M\n' \
    #         '@R13\n' \
    #         'M = -1\n' \
    #         '@POS1' + str(i) + '\n' \
    #         'D;JGT\n' \
    #         '@R13\n' \
    #         'M = 0\n' \
    #         '(POS1' + str(i) + ')\n' \
    #         '@SP\n' \
    #         'A = M - 1\n' \
    #         'D = M\n' \
    #         '@R14\n' \
    #         'M = -1\n' \
    #         '@POS2' + str(i) + '\n' \
    #         'D;JGT\n' \
    #         '@R14\n' \
    #         'M = 0\n' \
    #         '(POS2' + str(i) + ')\n' \
    #         '@R14\n' \
    #         'D = M\n' \
    #         '@R13\n' \
    #         'D = M - D\n' \
    #         '@OVERFLOW' + str(i) + '\n' \
    #         'D;JNE\n' \
    #         '@SP\n' \
    #         'A = M\n' \
    #         'D = M\n' \
    #         '@SP\n' \
    #         'A = M - 1\n' \
    #         'D = D - M\n' \
    #         '@TRUE' + str(i) + '\n' \
    #         'D;JEQ\n' \
    #         '@SP\n' \
    #         'A = M - 1\n' \
    #         'M = 0\n' \
    #         '@END' + str(i) + '\n' \
    #         '0;JMP\n' \
    #         '(TRUE' + str(i) + ')\n' \
    #         '@SP\n' \
    #         'A = M - 1\n' \
    #         'M = -1\n' \
    #         '@END' + str(i) + '\n' \
    #         '0;JMP\n' \
    #         '(OVERFLOW' + str(i) + ')\n' \
    #         '@SP\n' \
    #         'A = M - 1\n' \
    #         'M = 0\n' \
    #         '(END' + str(i) + ')\n'
    #
    #
    # def gtstr(i):
    #     return '@SP\n' \
    #         'AM = M-1\n' \
    #         'D = M\n' \
    #         '@R13\n' \
    #         'M=-1\n'\
    #         '@POS1' + str(i) + '\n' \
    #         'D;JGT\n' \
    #         '@R13\n' \
    #         'M=0\n' \
    #         '(POS1' + str(i) + ')\n' \
    #         '@SP\n' \
    #         'A=M-1\n' \
    #         'D=M\n' \
    #         '@R14\n' \
    #         'M=-1\n' \
    #         '@POS2' + str(i) + '\n' \
    #         'D;JGT\n' \
    #         '@R14\n' \
    #         'M=0\n' \
    #         '(POS2'+str(i) +')\n' \
    #         '@R14\n' \
    #         'D=M\n' \
    #         '@R13\n' \
    #         'D=M-D\n' \
    #         '@OVERFLOW' + str(i) + '\n'\
    #         'D;JNE\n' \
    #         '@SP\n'\
    #         'A=M\n' \
    #         'D=M\n' \
    #         '@SP\n' \
    #         'A=M-1\n' \
    #         'D=D-M\n' \
    #         '@TRUE' + str(i) + '\n'\
    #         'D;JLT\n' \
    #         '@SP\n'\
    #         'A=M-1\n'\
    #         'M=0\n'\
    #         '@END' + str(i) + '\n' \
    #         '0;JMP\n' \
    #         '(TRUE' + str(i) + ')\n' \
    #         '@SP\n' \
    #         'A=M-1\n' \
    #         'M=-1\n'\
    #         '@END' + str(i) + '\n' \
    #         '0;JMP\n' \
    #         '(OVERFLOW' + str(i) + ')\n' \
    #         '@R14\n' \
    #         'D=M\n' \
    #         '@SP\n' \
    #         'A=M-1\n'\
    #         'M=D\n' \
    #         '(END' + str(i) + ')\n'
    #
    # def ltstr(i):
    #     return '@SP\n' \
    #         'AM = M-1\n' \
    #         'D = M\n' \
    #         '@R13\n' \
    #         'M=-1\n' \
    #         '@POS1' + str(i) + '\n' \
    #         'D;JGT\n' \
    #         '@R13\n' \
    #         'M=0\n' \
    #         '(POS1' + str(i) + ')\n' \
    #         '@SP\n' \
    #         'A=M-1\n' \
    #         'D=M\n' \
    #         '@R14\n' \
    #         'M=-1\n' \
    #         '@POS2' + str(i) + '\n' \
    #         'D;JGT\n' \
    #         '@R14\n' \
    #         'M=0\n' \
    #         '(POS2'+str(i) +')\n' \
    #         '@R14\n' \
    #         'D=M\n' \
    #         '@R13\n' \
    #         'D=M-D\n' \
    #         '@OVERFLOW' + str(i) + '\n' \
    #         'D;JNE\n' \
    #         '@SP\n' \
    #         'A=M\n' \
    #         'D=M\n' \
    #         '@SP\n' \
    #         'A=M-1\n' \
    #         'D=D-M\n' \
    #         '@TRUE' + str(i) + '\n' \
    #         'D;JGT\n' \
    #         '@SP\n' \
    #         'A=M-1\n' \
    #         'M=0\n' \
    #         '@END' + str(i) + '\n' \
    #         '0;JMP\n' \
    #         '(TRUE' + str(i) + ')\n' \
    #         '@SP\n' \
    #         'A=M-1\n' \
    #         'M=-1\n' \
    #         '@END' + str(i) + '\n' \
    #         '0;JMP\n' \
    #         '(OVERFLOW' + str(i) + ')\n' \
    #         '@R13\n' \
    #         'D=M\n' \
    #         '@SP\n' \
    #         'A=M-1\n' \
    #         'M=D\n' \
    #         '(END' + str(i) + ')\n'