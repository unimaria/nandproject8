#######################################################
# Authors: jakedn,
# This is a file that i didnt yet decide what to write here
#######################################################

from os import listdir, getcwd
from os.path import isfile, join, isdir, exists, split
from CodeWriter import CodeWriter
from Parser import Parser
import sys


# This function takes a directory and returns all files in or of that directory
def getfiles(directory):
    cwd = getcwd()
    if not exists(directory):
        if exists(join(cwd, directory)):
            directory = join(cwd, directory)
        else:
            return []
    if isdir(directory):
        return [join(directory, f) for f in listdir(directory)
                if (isfile(join(directory, f)) and '.vm' == f[-3:])]
    if isfile(directory):
        return [directory]

    # if we get here we are not on a file or a directory
    return []


def translateVM(path):
    files = getfiles(path)
    dir_var = None
    if isdir(path):
        dir_var = split(path)[1]
    codewriter = CodeWriter(files[0], dir_var)
    for cur_file in files:
        codewriter.setfilename(cur_file)
        Parser.initialize(cur_file)
        Parser.open_file()
        Parser.advance()
        while Parser.has_more_commands():
            command_type = Parser.command_type()
            if command_type == Parser.C_PUSH or command_type == Parser.C_POP:
                arg1 = Parser.arg1()
                arg2 = Parser.arg2()
                codewriter.writepushpop(command_type, arg1, arg2)
            elif command_type == Parser.C_ARITHMETIC:
                command = Parser.arg1()
                codewriter.writearithmetic(command)
            elif command_type == Parser.C_LABEL:
                label = Parser.arg1()
                codewriter.writelabel(label)
            elif command_type == Parser.C_GOTO:
                label = Parser.arg1()
                codewriter.writegoto(label)
            elif command_type == Parser.C_IF:
                label = Parser.arg1()
                codewriter.writeif(label)
            elif command_type == Parser.C_FUNCTION:
                function_name = Parser.arg1()
                num_locals = Parser.arg2()
                codewriter.writefunction(function_name, num_locals)
            elif command_type == Parser.C_CALL:
                function_name = Parser.arg1()
                num_args = Parser.arg2()
                codewriter.writecall(function_name, num_args)
            elif command_type == Parser.C_RETURN:
                codewriter.writereturn()
            Parser.advance()
    codewriter.close()


if __name__ == '__main__':
    file_or_dir = sys.argv[1]
    translateVM(file_or_dir)
