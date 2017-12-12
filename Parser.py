class Parser:

    ###################################
    # This is the parser of the VM
    ###################################

    COMMENT = "//"
    EMPTY_LINE = "\n"
    EMPTY_LINE_2 = "\r"
    C_ARITHMETIC = 1
    C_PUSH = 2
    C_POP = 3
    C_LABEL = 4
    C_GOTO = 5
    C_IF = 6
    C_FUNCTION = 7
    C_RETURN = 8
    C_CALL = 9
    ARITHMETIC_LIST = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
    PUSH_STR = "push"
    POP_STR = "pop"
    GOTO_STR = "goto"
    LABEL_STR = "label"
    IF_STR = "if-goto"
    FUNCTION_STR = "function"
    CALL_STR = "call"
    RETURN_STR = "return"

    file = None
    opened_file = None
    current_command = None
    current_function = None

    @staticmethod
    def initialize(file_path):
        """
        A method that sets the file the parser is currently working with.
        :param file_path: file path
        """
        Parser.file = file_path
        Parser.current_command = None
        Parser.current_function = None

    @staticmethod
    def open_file():
        """
        Opens current file.
        :return:
        """
        Parser.opened_file = open(Parser.file)

    @staticmethod
    def remove_whitespace(str_to_remove):
        """
        removes whitespace from string
        :param str_to_remove: string
        :return: string without whitespaces
        """
        str_to_remove = str_to_remove.strip()
        return str_to_remove

    @staticmethod
    def remove_comments(str_to_remove):
        """
        removes comments from end of line, they start with "//"
        :param str_to_remove: string to remove
        :return: line without comments
        """
        comment_idx = str_to_remove.find(Parser.COMMENT)
        if comment_idx != -1:
            str_to_remove = str_to_remove[0:comment_idx]
        return str_to_remove

    @staticmethod
    def has_more_commands():
        """
        Checks if there are more commands in file.
        If so, returns True, otherwise, returns False and closes the file.
        :return:
        """
        if Parser.current_command == '':
            Parser.opened_file.close()
            return False
        return True

    @staticmethod
    def advance():
        """
        Advances line of the file to current command line
        """
        Parser.current_command = Parser.opened_file.readline()
        while Parser.current_command.startswith(Parser.EMPTY_LINE) or \
                Parser.remove_whitespace(Parser.current_command).startswith(
                    Parser.COMMENT) or \
                Parser.current_command.startswith(Parser.EMPTY_LINE_2):
            Parser.current_command = Parser.opened_file.readline()
        Parser.current_command = Parser.remove_comments(Parser.current_command)
        Parser.current_command = Parser.remove_whitespace(Parser.current_command)

    @staticmethod
    def command_type():
        if Parser.current_command in Parser.ARITHMETIC_LIST:
            return Parser.C_ARITHMETIC
        elif Parser.current_command.startswith(Parser.PUSH_STR):
            return Parser.C_PUSH
        elif Parser.current_command.startswith(Parser.POP_STR):
            return Parser.C_POP
        elif Parser.current_command.startswith(Parser.GOTO_STR):
            return Parser.C_GOTO
        elif Parser.current_command.startswith(Parser.IF_STR):
            return Parser.C_IF
        elif Parser.current_command.startswith(Parser.CALL_STR):
            return Parser.C_CALL
        elif Parser.current_command.startswith(Parser.RETURN_STR):
            #Parser.current_function = None  # end of current function
            return Parser.C_RETURN
        elif Parser.current_command.startswith(Parser.FUNCTION_STR):
            return Parser.C_FUNCTION
        elif Parser.current_command.startswith(Parser.LABEL_STR):
            return Parser.C_LABEL

    @staticmethod
    def arg1():
        """
        Returns the first argument of the command.
        Changes the current command.
        If the command is arithmetic, returns the command itself.
        Should not be called if command type is C_RETURN.
        """
        arguments = Parser.current_command.split()
        command_type = Parser.command_type()
        if command_type == Parser.C_ARITHMETIC:
            return arguments[0]
        else:
            if command_type == Parser.C_FUNCTION:
                Parser.current_function = arguments[1]  # saves function name
            if command_type == Parser.C_PUSH or command_type == Parser.C_POP or command_type == Parser.C_CALL or\
                    command_type == Parser.C_FUNCTION:
                Parser.current_command = arguments[2]
            return arguments[1]

    @staticmethod
    def arg2():
        """
        Returns the second argument of the command, should be called if the
        the current command is pop, push, call or function.
        """
        return int(Parser.current_command)
