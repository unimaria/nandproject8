###################################
# Authors : jakedn, unimaria
# This is the Codewriter module as described in chapter
# 7 off the book
###################################


from Parser import Parser
from os.path import basename
from functions import *


class CodeWriter:

    iteration = 0

    segments = {'argument': 'ARG',
                'local': 'LCL',
                'constant': '-1',
                'pointer': '3', #change from project 7 (from THIS to 3)
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

    def __init__(self, file_path):
        """
        constructor
        :param file_path: file directory path
        """
        self.file_name = basename(file_path)[:-3]
        self.file = open(file_path[0:-3]+'.asm', "w")

    def setfilename(self, file_path):
        """

        :param file_path: file directory path
        """
        CodeWriter.iteration = 0
        self.file_name = basename(file_path)[:-3]
        self.file = open(file_path[0:-3] + '.asm', "w")

    def writearithmetic(self, command):
        """
        writes the next thing in our file given an arithmetic command
        :param command: the given command
        """
        towrite = ''
        if command in CodeWriter.BINOP:
            if command == 'gt':
                towrite = gtstr(CodeWriter.iteration, Parser.current_function) # changed TODO make sure its good
                CodeWriter.iteration += 1
            elif command == 'lt':

                towrite = ltstr(CodeWriter.iteration, Parser.current_function) # changed TODO make sure its good
                CodeWriter.iteration += 1
            elif command == 'eq':
                towrite = eqstr(CodeWriter.iteration, Parser.current_function) # changed TODO make sure its good
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
                towrite = pushstack(self.file_name + '.' + str(index))
                #towrite = '@' + self.file_name + '.' + str(index) + '\n' + pushstack()

            elif seg == 'pointer':
                if index == 0:
                    pushstack('THIS')
                    #towrite = '@THIS\n' + pushstack()

                if index == 1:
                    pushstack('THAT')
                    #towrite = '@THAT\n' + pushstack()

            elif seg == 'temp':
                pushstack(str(5 + index))
                #towrite = '@' + str(5 + index) + '\n' + pushstack()

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
        towrite = "(" + label + ":" + scope + ")" + "\n"
        self.file.write(towrite)

    def writegoto(self, label):
        if Parser.current_function is not None:
            scope = Parser.current_function
        else:
            scope = self.file_name
        towrite = "@" + label + ":" + scope + "\n" \
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
                  "@" + label + ":" + scope + "\n"\
                  "D;JNE\n"  # if true the stack will contain -1
        self.file.write(towrite)

    def writecall(self, functionname, numargs):
        towrite = '@RETURN$' + functionname + '\n' \
                   'D=A\n' \
                   '@SP\n' \
                   'A=M\n' \
                   'M=D\n' \
                   '@SP\n' \
                   'M=M+1\n' +\
                   pushstack('LCL') + \
                   pushstack('ARG') + \
                   pushstack('THIS')+ \
                   pushstack('THAT')+ \
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
        #todo changed code thats in comment need to undo change or remove comment
        towrite = '(' + functionname + ')\n'\
                  '@R13\n'\
                  'M=0\n'\
                  '(LOOP$' + functionname + ')\n'\
                  '@0\n'\
                  'D=A\n' \
                  '@SP\n' \
                  'A=M\n' \
                  'M=D\n' \
                  '@SP\n' \
                  'M=M+1\n'\
                  '@R13\n'\
                  'M=M+1\n'\
                  'D=M\n'\
                  '@' + str(numlocals) + '\n'\
                  'D=M-D\n'\
                  '@LOOP$' + functionname + '\n'\
                  'D;JGT\n'
        self.file.write(towrite)

    def writereturn(self):
        """
        writes return to file
        """
        #todo bug cant use R14 R15 because of nesting replace them with push const
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
                  'A=M\n'\
                  'D=M\n'\
                  '@THAT\n'\
                  'M=D-1\n'\
                  '@THIS\n'\
                  'M=D-2'\
                  '@ARG\n'\
                  'M=D-3\n'\
                  '@LCL\n'\
                  'M=D-4\n'\
                  '@R15\n'\
                  '0;JMP\n'
        self.file.write(towrite)

    def close(self):
        if self.file != None:
            self.file.write('(END)\n@END\n0;JMP')
            self.file.close()

