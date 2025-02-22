from pathlib import Path
from typing import TextIO

from src.commands import CommandType, Dest, Comp, Jump


class Parser:
    def __init__(self, file_path: Path):
        self.__file: TextIO = open(file_path, "r")
        # the components of the current command where the file cursor is currently
        self.__command_type: CommandType | None = None
        self.__symbol: str | None = None
        self.__dest: Dest | None = None
        self.__comp: Comp | None = None
        self.__jump: Jump | None = None
        self.read_next_command()

    def get_command_type(self) -> CommandType | None:
        return self.__command_type

    def get_symbol(self) -> str | None:
        return self.__symbol

    def get_dest(self) -> Dest | None:
        return self.__dest

    def get_comp(self) -> Comp | None:
        return self.__comp

    def get_jump(self) -> Jump | None:
        return self.__jump

    def has_more_commands(self) -> bool:
        current_position = self.__file.tell()
        next_line = self.__file.readline()
        next_line_cleaned = next_line.replace(" ", "").strip()
        while next_line != "" and (
            next_line.isspace() or next_line_cleaned.startswith("//")
        ):
            next_line = self.__file.readline()
            next_line_cleaned = next_line.replace(" ", "").strip()
        self.__file.seek(current_position)
        return bool(next_line_cleaned)

    def read_next_command(self) -> None:
        current_line: str = self.__file.readline()
        current_line_cleaned: str = current_line.replace(" ", "").strip()
        while current_line.isspace() or current_line_cleaned.startswith("//"):
            current_line = self.__file.readline()
            current_line_cleaned = current_line.replace(" ", "").strip()
        current_command: str = current_line_cleaned.split("//")[0].strip()
        if current_command == "":
            self.__command_type = None
            self.__symbol = None
            self.__dest = None
            self.__comp = None
            self.__jump = None
            return
        self.__command_type = self.__determine_command_type(command=current_command)
        if self.__command_type == CommandType.C_COMMAND:
            self.__symbol = None
            if ";" in current_command and "=" not in current_command:
                self.__dest = None
                self.__comp = Comp(current_command.split(";")[0])
                self.__jump = Jump(current_command.split(";")[1])
            elif ";" not in current_command and "=" in current_command:
                self.__dest = Dest(current_command.split("=")[0])
                self.__comp = Comp(current_command.split("=")[1])
                self.__jump = None
            elif ";" in current_command and "=" in current_command:
                self.__dest = Dest(current_command.split("=")[0])
                string_after_equal_sign = current_command.split("=")[1]
                self.__comp = Comp(string_after_equal_sign.split(";")[0])
                self.__jump = Jump(string_after_equal_sign.split(";")[1])
        elif self.__command_type == CommandType.A_COMMAND:
            self.__dest = None
            self.__comp = None
            self.__jump = None
            self.__symbol = current_command.replace("@", "")

    @staticmethod
    def __determine_command_type(command: str) -> CommandType:
        if command.startswith("@") and command[1:].isdigit():
            return CommandType.A_COMMAND
        elif command.startswith("("):
            return CommandType.A_COMMAND
        else:
            return CommandType.C_COMMAND
