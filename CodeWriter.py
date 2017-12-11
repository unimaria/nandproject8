#!/usr/python
###################################
# Authors : jakedn, unimaria
# This is the Codewriter module as described in chapter
# 7 off the book
###################################


from Parser import Parser
from os.path import basename, dirname, join
from functions import *


class CodeWriter:

    iteration = 0

    segments = {'argument': 'ARG',
                'local': 'LCL',
                'constant': '-1',
                'pointer': 'THIS',
                'this': 'THIS',
                'that': 'THAT',
                'temp': '5'
                }

    BINOP = {"add": '+',
             "sub": '-',
             "eq": '=',
             "gt": '>',
             "lt": '<',
             "and": '&',
             "or": '|',
            }

    UNAOP = {"neg": '-',
             "not": '!'
            }

    SYS_CODE = '@256\n'\
               'D=A\n'\
               '@SP\n'\
               'M=D\n'

    def __init__(self, file_path, directory):
        """
        constructor
        :param file_path: file directory path
        """
        self.file_name = basename(file_path)[:-3]
        # if it is directory the asm file should have the name of the directory
        if directory is not None:
            self.file = open(join(dirname(file_path), directory) + '.asm', "w")
        else:
            self.file = open(file_path[0:-3]+'.asm', "w")
        self.file.write(self.SYS_CODE)
        self.writecall("Sys.init", 0)  # calls Sys.init

    def setfilename(self, file_path):
        """

        :param file_path: file directory path
        """
        CodeWriter.iteration = 0
        self.file_name = basename(file_path)[:-3]
        #self.file = open(file_path[0:-3] + '.asm', "w")

    def writearithmetic(self, command):
        """
        writes the next thing in our file given an arithmetic command
        :param command: the given command
        """
        towrite = ''
        if command in CodeWriter.BINOP:
            if command == 'gt':
                towrite = gtstr(CodeWriter.iteration)
                CodeWriter.iteration += 1

            elif command == 'lt':
                towrite = ltstr(CodeWriter.iteration)
                CodeWriter.iteration += 1
                
            elif command == 'eq':
                towrite = eqstr(CodeWriter.iteration)
                CodeWriter.iteration += 1
            else:
                towrite = '@SP\n' \
                          'AM=M-1\n' \
                          'D=M\n' \
                          'A=A-1\n' \
                          'M=M' + CodeWriter.BINOP[command] + 'D\n'

        if command in CodeWriter.UNAOP:
            towrite = '@SP\n' \
                      'A=M-1\n' \
                      'M=' + CodeWriter.UNAOP[command] + 'M\n'
        self.file.write(towrite)

    def writepushpop(self, command, seg, index):
        """
        writes the next thing in our file given an push/pop command
        :param command: the given command
        :param seg: the given segment
        :param index: the given index
        """
        towrite = ''
        if command == Parser.C_POP:
            if seg == 'static':
                towrite = popstack(self.file_name + '.' + str(index))

            elif seg == 'pointer':
                if index == 0:
                    towrite = popstack('THIS')
                if index == 1:
                    towrite = popstack('THAT')

            elif seg == 'temp':
                towrite = popstack(str(5 + index))

            else:
                # we use R13 here to save the index as a number we add later
                towrite = '@' + str(index) + '\n' \
                          'D=A\n' \
                          '@' + CodeWriter.segments[seg] + '\n' \
                          'D=M+D\n' \
                          '@R13\n' \
                          'M=D\n' \
                          '@SP\n' \
                          'AM=M-1\n' \
                          'D=M\n' \
                          '@R13\n' \
                          'A=M\n' \
                          'M=D\n'

        if command == Parser.C_PUSH:
            if seg == 'constant':
                towrite = '@' + str(index) + '\n' \
                          'D=A\n' \
                          '@SP\n' \
                          'A=M\n' \
                          'M=D\n' \
                          '@SP\n' \
                          'M=M+1\n'

            elif seg == 'static':
                towrite = '@' + self.file_name + '.' + str(index) + '\n' + pushstack()

            elif seg == 'pointer':
                if index == 0:
                    towrite = '@THIS\n' + pushstack()

                if index == 1:
                    towrite = '@THAT\n' + pushstack()

            elif seg == 'temp':
                towrite = '@' + str(5 + index) + '\n' + pushstack()

            else:
                towrite = '@' + str(index) + '\n' \
                          'D=A\n' \
                          '@' + CodeWriter.segments[seg] + '\n' \
                          'A=M+D\n' \
                          'D=M\n' \
                          '@SP\n' \
                          'A=M\n' \
                          'M=D\n' \
                          '@SP\n' \
                          'M=M+1\n'

        self.file.write(towrite)

    def writelabel(self, label):
        """
        writes a label.
        if the label is inside a function the structure is (function_name:label)
        otherwise the structure is (file_name:label)
        """
        # TODO: check if this is the right way to right labels
        if Parser.current_function is not None:  # checks if label inside function
            scope = Parser.current_function
        else:
            scope = self.file_name
        towrite = "(" + label + "$" + scope + ")" + "\n"
        self.file.write(towrite)

    def writegoto(self, label):
        if Parser.current_function is not None:
            scope = Parser.current_function
        else:
            scope = self.file_name
        towrite = "@" + label + "$" + scope + "\n" \
                  "0;JMP\n"
        self.file.write(towrite)

    def writeif(self, label):
        if Parser.current_function is not None:
            scope = Parser.current_function
        else:
            scope = self.file_name
        towrite = "@SP\n"\
                  "AM = M-1\n"\
                  "D=M\n"\
                  "@" + label + "$" + scope + "\n"\
                  "D;JNE\n"  # if true the stack will contain -1
        self.file.write(towrite)

    def writecall(self, functionname, numargs):
        towrite = '@RETURN$' + functionname + '\n' \
                   'D=A\n' \
                   '@SP\n' \
                   'A=M\n' \
                   'M=D\n' \
                   '@SP\n' \
                   'M=M+1\n'\
                   '@LCL\n' + pushstack() + \
                   '@ARG\n' + pushstack() + \
                   '@THIS\n' + pushstack() + \
                   '@THAT\n' + pushstack() + \
                   '@SP\n'\
                   'D=M\n'\
                   '@5\n'\
                   'D=D-A\n'\
                   '@' + str(numargs) + '\n'\
                   'D=D-A\n'\
                   '@ARG\n'\
                   'M=D\n'\
                   '@SP\n'\
                   'D=M\n'\
                   '@LCL\n'\
                   'M=D\n'\
                   '@' + functionname + '\n'\
                   '0;JMP\n'\
                   '(RETURN$' + functionname + ')\n'
        self.file.write(towrite)

    def writefunction(self, functionname, numlocals):
        towrite = '(' + functionname + ')\n'\
                  '@R15\n'\
                  'M=0\n'\
                  '@' + str(numlocals) + '\n'\
                  'D=A\n'\
                  '@END$' + functionname + '\n'\
                  'D;JEQ\n'\
                  '(LOOP$' + functionname + ')\n'\
                  '@0\n'\
                  'D=A\n' \
                  '@SP\n' \
                  'A=M\n' \
                  'M=D\n' \
                  '@SP\n' \
                  'M=M+1\n'\
                  '@R15\n'\
                  'M=M+1\n'\
                  'D=M\n'\
                  '@' + str(numlocals) + '\n'\
                  'D=A-D\n'\
                  '@LOOP$' + functionname + '\n'\
                  'D;JGT\n'\
                  '(END$' + functionname + ')\n'
        self.file.write(towrite)

    def writereturn(self):
        """
        writes return to file
        """
        # R14 is used as endFrame and R15 is used as retAddr
        towrite = '@LCL\n'\
                  'D=M\n'\
                  '@R14\n'\
                  'M=D\n'\
                  '@5\n'\
                  'D=D-A\n'\
                  'A=D\n'\
                  'D=M\n'\
                  '@R15\n'\
                  'M=D\n'\
                  '@SP\n'\
                  'AM=M-1\n'\
                  'D=M\n'\
                  '@ARG\n'\
                  'A=M\n'\
                  'M=D\n'\
                  '@ARG\n'\
                  'D=M\n'\
                  '@SP\n'\
                  'M=D+1\n'\
                  '@R14\n'\
                  'A=M-1\n'\
                  'D=M\n'\
                  '@THAT\n'\
                  'M=D\n'\
                  '@R14\n'\
                  'M=M-1\n'\
                  'A=M-1\n'\
                  'D=M\n'\
                  '@THIS\n'\
                  'M=D\n' \
                  '@R14\n' \
                  'M=M-1\n' \
                  'A=M-1\n' \
                  'D=M\n' \
                  '@ARG\n'\
                  'M=D\n' \
                  '@R14\n' \
                  'M=M-1\n' \
                  'A=M-1\n' \
                  'D=M\n' \
                  '@LCL\n'\
                  'M=D\n'\
                  '@R15\n'\
                  'A=M\n'\
                  '0;JMP\n'
        self.file.write(towrite)

    def close(self):
        if self.file != None:
            self.file.write('(END)\n@END\n0;JMP')
            self.file.close()

