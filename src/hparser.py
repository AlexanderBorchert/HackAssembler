from io import TextIOWrapper
from pathlib import Path
from src.commandType import CommandType


class Parser:
    def __init__(self, file_path: Path):
        self.__file: TextIOWrapper = open(file_path, 'r')
        #the components of the current command where the file cursor is currently
        self.__command_type: CommandType = None
        self.__symbol: str = None
        self.__dest: str = None
        self.__comp: str = None
        self.__jump: str = None
        self.advance()

    def get_command_type(self)->CommandType:
        return self.__command_type

    def get_symbol(self)-> str:
        return self.__symbol

    def get_dest(self)-> str:
        return self.__dest

    def get_comp(self)-> str:
        return self.__comp

    def get_jump(self)-> str:
        return self.__jump

    def has_more_commands(self)-> bool:

        current_position = self.__file.tell()
        next_line = self.__file.readline()
        return bool(next_line)

    def advance(self):
        current_line: str = self.__file.readline()
        while current_line == "" or current_line.isspace() or current_line.startswith("//"):
            current_line = self.__file.readline()
        current_command = current_line.split("//")[0].strip()
        self.__command_type = self.__determine_command_type(current_command)
        if self.__command_type == CommandType.C_COMMAND:
            if ';' in current_command and '=' not in current_command:
                self.__dest = None
                self.__comp = current_command.split(';')[0]
                self.__jump = current_command.split(';')[1]
            elif ';' not in current_command and '=' in current_command:
                self.__dest = current_command.split('=')[0]
                self.__comp = current_command.split('=')[1]
                self.__jump = None
            elif ';' in current_command and '=' in current_command:
                self.__dest = current_command.split('=')[0]
                string_after_equal_sign = current_command.split('=')[1]
                self.__comp = string_after_equal_sign.split(';')[0]
                self.__jump = string_after_equal_sign.split(';')[1]

    def __determine_command_type(self, s: str):
        if s.startswith('@') and s[1:].isdigit():
            return CommandType.A_COMMAND
        elif s.startswith('('):
            return CommandType.A_COMMAND
        else:
            return CommandType.C_COMMAND







