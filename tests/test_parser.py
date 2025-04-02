# type: ignore

from pathlib import Path

import pytest

from src.commands import Command, ACommand, CCommand, Dest, Comp, Jump
from src.parser import Parser, NoCommandsFoundError, InvalidSyntaxError


def test_empty_file_raises_no_commands_found_error(
        empty_asm_file: Path) -> None:
    with pytest.raises(NoCommandsFoundError):
        Parser(empty_asm_file)


def test_only_whitespaces_raises_no_commands_error(
        asm_file_containing_only_whitespace: Path) -> None:
    with pytest.raises(NoCommandsFoundError):
        Parser(asm_file_containing_only_whitespace)


def test_only_comment_raises_no_commands_error(
        asm_file_containing_only_comment: Path) -> None:
    with pytest.raises(NoCommandsFoundError):
        Parser(asm_file_containing_only_comment)


def test_invalid_syntax_raises_error(
        asm_file_containing_invalid_syntax: Path) -> None:
    with pytest.raises(InvalidSyntaxError):
        Parser(asm_file_containing_invalid_syntax)


def test_a_command(
        asm_file_containing_a_command: Path) -> None:
    parser = Parser(asm_file_containing_a_command)
    current_command: Command = parser.get_current_command()
    assert isinstance(current_command, ACommand), f"Expected type ACommand, but got {type(current_command).__name__}"
    expected_address: str = "5"
    assert current_command.raw_address == expected_address, \
        f"Expected address {expected_address}, but got {current_command.raw_address}"


def test_move_to_next_command(
        asm_file_containing_two_commands: Path) -> None:
    parser = Parser(asm_file_containing_two_commands)
    current_command: Command = parser.get_current_command()
    assert isinstance(current_command, ACommand)
    assert current_command.raw_address == "5"
    assert parser.move_to_next_command()  # should be true because there is another command
    current_command = parser.get_current_command()
    assert isinstance(current_command, ACommand)
    assert current_command.raw_address == "6"
    assert not parser.move_to_next_command()  # should be false because we're at the last command
    current_command = parser.get_current_command()
    assert isinstance(current_command, ACommand)
    assert current_command.raw_address == "6"


def test_get_current_command_number(asm_file_containing_two_commands: Path) -> None:
    parser = Parser(asm_file_containing_two_commands)
    assert parser.get_current_command_number() == "0"
    parser.move_to_next_command()
    assert parser.get_current_command_number() == "1"


def test_move_to_first_command(asm_file_containing_two_commands: Path) -> None:
    parser = Parser(asm_file_containing_two_commands)
    parser.move_to_next_command()
    current_command: Command = parser.get_current_command()
    assert isinstance(current_command, ACommand)
    assert current_command.raw_address == "6"
    parser.move_to_first_command()
    current_command = parser.get_current_command()
    assert isinstance(current_command, ACommand)
    assert current_command.raw_address == "5"


def test_c_command(asm_file_containing_c_command: Path) -> None:
    parser = Parser(asm_file_containing_c_command)
    current_command: Command = parser.get_current_command()
    assert isinstance(current_command, CCommand), f"Expected type C_Command, but got {type(current_command).__name__}"
    assert current_command.dest == Dest.D
    assert current_command.comp == Comp.m
    assert current_command.jump == Jump.JGT


def test_complex_file(
        asm_file_containing_several_commands: Path) -> None:
    parser = Parser(asm_file_containing_several_commands)

    current_command: Command = parser.get_current_command()
    assert isinstance(current_command, ACommand), f"Expected type ACommand, but got {type(current_command).__name__}"
    assert current_command.raw_address == "5"

    assert parser.move_to_next_command()
    current_command = parser.get_current_command()
    assert isinstance(current_command, CCommand), f"Expected type C_Command, but got {type(current_command).__name__}"
    assert current_command.dest == Dest.M
    assert current_command.comp == Comp.one
    assert current_command.jump == Jump.Null

    assert parser.move_to_next_command()
    current_command = parser.get_current_command()
    assert isinstance(current_command, CCommand), f"Expected type C_Command, but got {type(current_command).__name__}"
    assert current_command.dest == Dest.Null
    assert current_command.comp == Comp.zero
    assert current_command.jump == Jump.JMP

    assert parser.move_to_next_command()
    current_command = parser.get_current_command()
    assert isinstance(current_command, CCommand), f"Expected type C_Command, but got {type(current_command).__name__}"
    assert current_command.dest == Dest.D
    assert current_command.comp == Comp.m
    assert current_command.jump == Jump.JGT

    assert not parser.move_to_next_command()  # there is no new command
