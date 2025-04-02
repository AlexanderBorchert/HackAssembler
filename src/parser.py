from pathlib import Path
from typing import TextIO, Optional, Type

from src.commands import Dest, Comp, Jump, CCommand, ACommand, Command, LCommand


class Parser:
    def __init__(self, file_path: Path):
        self.__file: TextIO = open(file_path, "r")
        self.__current_command: Command
        self.__current_command_number: int = -1
        file_contains_command = self.move_to_next_command()
        if not file_contains_command:
            raise NoCommandsFoundError(file_path)

    def get_current_command(self) -> Command:
        return self.__current_command
    
    def get_current_command_number(self) -> str:
        return str(self.__current_command_number)

    def move_to_next_command(self) -> bool:
        next_line = self.__file.readline()
        while next_line != "":
            command = self.__create_command(next_line)
            if command is not None:
                self.__current_command = command
                self.__current_command_number += 1
                return True
            next_line = self.__file.readline()
        return False
    
    def move_to_first_command(self) -> None:
        self.__file.seek(0)
        self.move_to_next_command()
        self.__current_command_number = 0

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
    def __create_c_command(command: str) -> CCommand | None:
        dest: Dest
        comp: Comp
        jump: Jump
        if ";" in command and "=" not in command:
            dest = Dest.Null
            comp = Comp(command.split(";")[0])
            jump = Jump(command.split(";")[1])
            return CCommand(dest, comp, jump)
        elif ";" not in command and "=" in command:
            dest = Dest(command.split("=")[0])
            comp = Comp(command.split("=")[1])
            jump = Jump.Null
            return CCommand(dest, comp, jump)
        elif ";" in command and "=" in command:
            dest = Dest(command.split("=")[0])
            string_after_equal_sign = command.split("=")[1]
            comp = Comp(string_after_equal_sign.split(";")[0])
            jump = Jump(string_after_equal_sign.split(";")[1])
            return CCommand(dest, comp, jump)
        else:
            return None

    @staticmethod
    def __create_a_command(command: str) -> ACommand | None:
        if command.startswith("@"):
            if command[1:].isdigit():
                raw_address: str = command[1:]
                return ACommand(raw_address=raw_address)
            else:
                symblic_address: str = command[1:]
                return ACommand(symbol_address=symblic_address)
        else:
            return None

    @staticmethod
    def __create_l_command(command: str) -> LCommand | None:
        if command.startswith('(') and command.endswith(')'):
            label: str = command[1:-1]
            return LCommand(label)
        else:
            return None

    @staticmethod
    def __delete_comments_and_spaces(raw_string: str) -> str:
        string_without_comments = raw_string.split('//', 1)[0]
        cleaned_string = string_without_comments.replace(" ", "").strip()
        return cleaned_string
    
    def __enter__(self) -> "Parser":
        return self
    
    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[object]
    ) -> Optional[bool]:
        return None


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
