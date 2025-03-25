from pathlib import Path
from typing import TextIO

from src.commands import Dest, Comp, Jump, C_Command, A_Command, Command, L_Command, Label


class Parser:
    def __init__(self, file_path: Path):
        self.__file: TextIO = open(file_path, "r")
        self.__current_command: Command
        file_contains_command = self.move_to_next_command()
        if not file_contains_command:
            raise NoCommandsFoundError(file_path)

    def get_current_command(self) -> Command:
        return self.__current_command

    def move_to_next_command(self) -> bool:
        next_line = self.__file.readline()
        while next_line != "":
            command = self.__create_command(next_line)
            if command is not None:
                self.__current_command = command
                return True
            next_line = self.__file.readline()
        return False

    @staticmethod
    def __create_command(line: str) -> Command | None:
        cleaned_line = Parser.__delete_comments_and_spaces(line)
        if cleaned_line == "":
            return None
        command: Command | None = Parser.__create_c_command(cleaned_line)
        if command is None:
            command = Parser.__create_a_command(cleaned_line)
        if command is None:
            command = Parser.__create_l_command(cleaned_line)
        if command is None:
            raise InvalidSyntaxError(line)
        return command

    @staticmethod
    def __create_c_command(command: str) -> C_Command | None:
        dest: Dest
        comp: Comp
        jump: Jump
        if ";" in command and "=" not in command:
            dest = Dest.Null
            comp = Comp(command.split(";")[0])
            jump = Jump(command.split(";")[1])
            return C_Command(dest, comp, jump)
        elif ";" not in command and "=" in command:
            dest = Dest(command.split("=")[0])
            comp = Comp(command.split("=")[1])
            jump = Jump.Null
            return C_Command(dest, comp, jump)
        elif ";" in command and "=" in command:
            dest = Dest(command.split("=")[0])
            string_after_equal_sign = command.split("=")[1]
            comp = Comp(string_after_equal_sign.split(";")[0])
            jump = Jump(string_after_equal_sign.split(";")[1])
            return C_Command(dest, comp, jump)
        else:
            return None

    @staticmethod
    def __create_a_command(command: str) -> A_Command | None:
        if command.startswith("@") and command[1:].isdigit():
            address: str = command.replace("@", "")
            return A_Command(address)
        else:
            return None

    @staticmethod
    def __create_l_command(command: str) -> L_Command | None:
        if command.startswith('(') and command.endswith(')'):
            return L_Command(Label.R0)
        else:
            return None

    @staticmethod
    def __delete_comments_and_spaces(raw_string: str) -> str:
        string_without_comments = raw_string.split('//', 1)[0]
        cleaned_string = string_without_comments.replace(" ", "").strip()
        return cleaned_string


class NoCommandsFoundError(Exception):
    """Raised when the assembler file does not contain any parseable commands."""
    def __init__(self, filepath: Path):
        super().__init__(
            f"""
            No commands found in file: {filepath.name}.
            Full path: {filepath.as_uri()}
            """
        )
        self.filepath = filepath
        

class InvalidSyntaxError(Exception):
    """Raised when the syntax is invalid ."""
    def __init__(self, line: str):
        super().__init__(
            f"""
            Invalid syntax: {line}.
            """
        )
        self.line = line
