from pathlib import Path

import pytest

from src.commands import Command, A_Command, C_Command, Dest, Comp, Jump
from src.parser import Parser, NoCommandsFoundError, InvalidSyntaxError


def test_empty_file_raises_no_commands_found_error(
        empty_asm_file: Path) -> None:
    with pytest.raises(NoCommandsFoundError):
        parser = Parser(empty_asm_file)


def test_only_whitespaces_raises_no_commands_error(
        asm_file_containing_only_whitespace: Path) -> None:
    with pytest.raises(NoCommandsFoundError):
        parser = Parser(asm_file_containing_only_whitespace)


def test_only_comment_raises_no_commands_error(
        asm_file_containing_only_comment: Path) -> None:
    with pytest.raises(NoCommandsFoundError):
        parser = Parser(asm_file_containing_only_comment)


def test_invalid_syntax_raises_error(
        asm_file_containing_invalid_syntax: Path) -> None:
    with pytest.raises(InvalidSyntaxError):
        parser = Parser(asm_file_containing_invalid_syntax)


def test_A_Command(
        asm_file_containing_A_Command: Path) -> None:
    parser = Parser(asm_file_containing_A_Command)
    current_command: Command = parser.get_current_command()
    assert isinstance(current_command, A_Command), f"Expected type A_Command, but got {type(current_command).__name__}"
    expected_address: str = "5"
    assert current_command.address == expected_address, f"Expected address {expected_address}, but got {current_command.address}"


def test_move_to_next_command(
        asm_file_containing_two_commands: Path) -> None:
    parser = Parser(asm_file_containing_two_commands)
    current_command: Command = parser.get_current_command()
    assert isinstance(current_command, A_Command)
    assert current_command.address == "5"
    assert parser.move_to_next_command()  # should be true because there is another command
    current_command = parser.get_current_command()
    assert isinstance(current_command, A_Command)
    assert current_command.address == "6"
    assert not parser.move_to_next_command()  # should be false because we're at the last command
    current_command = parser.get_current_command()
    assert isinstance(current_command, A_Command)
    assert current_command.address == "6"


def test_C_Command(
        asm_file_containing_C_Command: Path) -> None:
    parser = Parser(asm_file_containing_C_Command)
    current_command: Command = parser.get_current_command()
    assert isinstance(current_command, C_Command), f"Expected type C_Command, but got {type(current_command).__name__}"
    assert current_command.dest == Dest.D
    assert current_command.comp == Comp.m
    assert current_command.jump == Jump.JGT


def test_complex_file(
        asm_file_containing_several_commands: Path) -> None:
    parser = Parser(asm_file_containing_several_commands)

    current_command: Command = parser.get_current_command()
    assert isinstance(current_command, A_Command), f"Expected type A_Command, but got {type(current_command).__name__}"
    assert current_command.address == "5"

    assert parser.move_to_next_command()
    current_command = parser.get_current_command()
    assert isinstance(current_command, C_Command), f"Expected type C_Command, but got {type(current_command).__name__}"
    assert current_command.dest == Dest.M
    assert current_command.comp == Comp.one
    assert current_command.jump == Jump.Null

    assert parser.move_to_next_command()
    current_command = parser.get_current_command()
    assert isinstance(current_command, C_Command), f"Expected type C_Command, but got {type(current_command).__name__}"
    assert current_command.dest == Dest.Null
    assert current_command.comp == Comp.zero
    assert current_command.jump == Jump.JMP

    assert parser.move_to_next_command()
    current_command = parser.get_current_command()
    assert isinstance(current_command, C_Command), f"Expected type C_Command, but got {type(current_command).__name__}"
    assert current_command.dest == Dest.D
    assert current_command.comp == Comp.m
    assert current_command.jump == Jump.JGT

    assert not parser.move_to_next_command()  # there is no new command
