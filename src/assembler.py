from pathlib import Path

from src.code import translate_command_into_binary_code
from src.commands import Command
from src.parser import Parser


def assemble(assembler_file_path: str | Path) -> None:
    parser: Parser
    binary_file_path: Path
    parser, binary_file_path = _prepare_assembler_context(assembler_file_path)
    with open(binary_file_path, "w") as binary_file:
        another_command_exists: bool = True  # otherwise parser would have thrown error
        while another_command_exists:
            command: Command = parser.get_current_command()
            machine_code: str = translate_command_into_binary_code(command)
            binary_file.write(machine_code)
            another_command_exists = parser.move_to_next_command()
            if another_command_exists:
                binary_file.write("\n")


def _prepare_assembler_context(file_path: str | Path) -> tuple[Parser, Path]:
    if isinstance(file_path, str):
        file_path = Path(file_path)
    __validate_input(file_path)
    binary_file_path: Path = file_path.with_suffix(".hack")
    binary_file_path.touch(exist_ok=True)
    assembler_file = Parser(file_path)
    return assembler_file, binary_file_path


def __validate_input(assembler_file_path: Path) -> None:
    if not assembler_file_path.exists():
        raise FileNotFoundError(f"File {assembler_file_path} not found")
    if assembler_file_path.suffix != ".asm":
        raise ValueError(f"File {assembler_file_path} is not an assembler file because it doesn't end with .asm")
