import typing
from pathlib import Path

import pytest
from src.hparser import Parser
from src.commandType import CommandType


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
        
        
        """
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

    parser.advance()
    assert parser.has_more_commands()
    assert parser.get_command_type() == CommandType.C_COMMAND
    assert parser.get_symbol() is None
    assert parser.get_dest() == "M"
    assert parser.get_comp() == "1"
    assert parser.get_jump() is None

    parser.advance()
    assert parser.has_more_commands()
    assert parser.get_command_type() == CommandType.C_COMMAND
    assert parser.get_symbol() is None
    assert parser.get_dest() is None
    assert parser.get_comp() == "0"
    assert parser.get_jump() == "JMP"

    parser.advance()
    assert not parser.has_more_commands()
    assert parser.get_command_type() == CommandType.C_COMMAND
    assert parser.get_symbol() is None
    assert parser.get_dest() == "D"
    assert parser.get_comp() == "M"
    assert parser.get_jump() == "JGT"

    parser.advance()
    assert not parser.has_more_commands()
    assert parser.get_command_type() is None
    assert parser.get_symbol() is None
    assert parser.get_dest() is None
    assert parser.get_comp() is None
    assert parser.get_jump() is None
