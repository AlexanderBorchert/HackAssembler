from pathlib import Path

import pytest
from src.hparser import Parser
from src.commandType import CommandType



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
        
        
        """.strip()
    )
    return filepath

def test_parser(test_asm_file: Path) -> None:
    parser = Parser(test_asm_file)

    #get command type should give A command
    assert parser.get_command_type() == CommandType.A_COMMAND
    # symbol should be 5
    #dest should be none
    #comp should be none
    #jump should be none
    #has more commands should be true


