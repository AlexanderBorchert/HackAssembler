import typing
from pathlib import Path

import pytest

from src.parser import Parser
from src.commands import CommandType, Dest, Comp, Jump


@typing.no_type_check
@pytest.fixture
def test_asm_file(tmp_path: Path) -> Path:
    filepath: Path = tmp_path / "test.asm"
    filepath.write_text(
        """
        //comment
        
        @5
        M  =  1 //comment
        0;JMP
        
        D=M;JGT
        
        
        """  # noqa:W293
    )
    return filepath


def test_parser(test_asm_file: Path) -> None:
    parser = Parser(test_asm_file)

    assert parser.has_more_commands()
    assert parser.get_command_type() == CommandType.A_COMMAND
    assert parser.get_symbol() == "5"
    assert parser.get_dest() is None
    assert parser.get_comp() is None
    assert parser.get_jump() is None

    parser.read_next_command()
    assert parser.has_more_commands()
    assert parser.get_command_type() == CommandType.C_COMMAND
    assert parser.get_symbol() is None
    assert parser.get_dest() == Dest.M
    assert parser.get_comp() == Comp.one
    assert parser.get_jump() is None

    parser.read_next_command()
    assert parser.has_more_commands()
    assert parser.get_command_type() == CommandType.C_COMMAND
    assert parser.get_symbol() is None
    assert parser.get_dest() is None
    assert parser.get_comp() == Comp.zero
    assert parser.get_jump() == Jump.JMP

    parser.read_next_command()
    assert not parser.has_more_commands()
    assert parser.get_command_type() == CommandType.C_COMMAND
    assert parser.get_symbol() is None
    assert parser.get_dest() == Dest.D
    assert parser.get_comp() == Comp.m
    assert parser.get_jump() == Jump.JGT

    parser.read_next_command()
    assert not parser.has_more_commands()
    assert parser.get_command_type() is None
    assert parser.get_symbol() is None
    assert parser.get_dest() is None
    assert parser.get_comp() is None
    assert parser.get_jump() is None
