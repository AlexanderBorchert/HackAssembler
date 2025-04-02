from contextlib import contextmanager
from typing import Generator, TextIO
import sys
from pathlib import Path
from hackassembler.code import translate_command_into_binary_code
from hackassembler.commands import Command, PredefinedLabel, LCommand, ACommand
from hackassembler.parser import Parser


def main() -> None:
    if len(sys.argv) != 2:  # Expect exactly one argument
        print("Usage: hackassemble <path-to-asm-file>")
        sys.exit(1)
    assembler_file_path = Path(sys.argv[1])
    try:
        assemble(assembler_file_path)
        print(f"Successfully assembled: {assembler_file_path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
        
        
def assemble(assembler_file_path: str | Path) -> None:
    parser: Parser
    with __prepare_assembler_context(assembler_file_path) as (parser, binary_file):  
        # read with parser from assembler file and write the respective machine code to binary_file
        symbol_table: dict[str, str] = __create_symbol_table(parser)
        parser.move_to_first_command()
        another_command_exists: bool = True  # otherwise parser would have thrown error
        while another_command_exists:
            command: Command = parser.get_current_command()
            machine_code: str = translate_command_into_binary_code(command=command, symbol_table=symbol_table)
            binary_file.write(machine_code)
            another_command_exists = parser.move_to_next_command()
            if another_command_exists and not isinstance(command, LCommand):
                binary_file.write("\n")


@contextmanager
def __prepare_assembler_context(file_path: str | Path) -> Generator[tuple[Parser, TextIO], None, None]:
    if isinstance(file_path, str):
        file_path = Path(file_path)
    __validate_input(file_path)
    binary_file_path: Path = file_path.with_suffix(".hack")

    # Initialize resources: Parser and binary file
    parser = Parser(file_path)
    binary_file = open(binary_file_path, "w")

    try:
        yield parser, binary_file
    finally:
        binary_file.close()
        parser.__exit__(None, None, None)  # Clean up Parser (if it implements __exit__)


def __validate_input(assembler_file_path: Path) -> None:
    if not assembler_file_path.exists():
        raise FileNotFoundError(f"File {assembler_file_path} not found")
    if assembler_file_path.suffix != ".asm":
        raise ValueError(f"File {assembler_file_path} is not an assembler file because it doesn't end with .asm")
    
    
def __create_symbol_table(parser: Parser) -> dict[str, str]:
    symbol_table: dict[str, str] = {label.name: label.value for label in PredefinedLabel}
    parser.move_to_first_command()
    another_command_exists: bool = True  # otherwise parser would have thrown error
    while another_command_exists:
        command: Command = parser.get_current_command()
        if isinstance(command, LCommand):
            symbol_table[command.label] = parser.get_current_command_number()
        another_command_exists = parser.move_to_next_command()
    parser.move_to_first_command()
    another_command_exists = True  # otherwise parser would have thrown error
    while another_command_exists:
        command = parser.get_current_command()
        if isinstance(command, ACommand) and command.symbol_address is not None and \
                command.symbol_address not in symbol_table:
            address: int = 16
            while str(address) in symbol_table.values():
                address += 1
            symbol_table[command.symbol_address] = str(address)
        another_command_exists = parser.move_to_next_command()
    return symbol_table
