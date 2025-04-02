# type: ignore
from pathlib import Path
from textwrap import dedent

import pytest


@pytest.fixture
def empty_asm_file(tmp_path: Path) -> Path:
    filepath: Path = tmp_path / "test.asm"
    filepath.write_text(
        """
        """
    )
    return filepath


@pytest.fixture
def asm_file_containing_only_whitespace(tmp_path: Path) -> Path:
    filepath: Path = tmp_path / "test.asm"
    filepath.write_text(
        """
        
        """
    )
    return filepath


@pytest.fixture
def asm_file_containing_only_comment(tmp_path: Path) -> Path:
    filepath: Path = tmp_path / "test.asm"
    filepath.write_text(
        """
        //comment
        """
    )
    return filepath


@pytest.fixture
def asm_file_containing_invalid_syntax(tmp_path: Path) -> Path:
    filepath: Path = tmp_path / "test.asm"
    filepath.write_text(
        """
        invalid syntax
        """
    )
    return filepath


@pytest.fixture
def asm_file_containing_a_command(tmp_path: Path) -> Path:
    filepath: Path = tmp_path / "test.asm"
    filepath.write_text(
        """
        @5
        """
    )
    return filepath


@pytest.fixture
def asm_file_containing_c_command(tmp_path: Path) -> Path:
    filepath: Path = tmp_path / "test.asm"
    filepath.write_text(
        """
        D=M;JGT
        """
    )
    return filepath


@pytest.fixture
def asm_file_containing_two_commands(tmp_path: Path) -> Path:
    filepath: Path = tmp_path / "test.asm"
    filepath.write_text(
        """
        @5
        @6
        """
    )
    return filepath


@pytest.fixture
def asm_file_containing_several_commands(tmp_path: Path) -> Path:
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


@pytest.fixture
def asm_file_containing_everything(tmp_path: Path) -> Path:
    filepath: Path = tmp_path / "test.asm"
    filepath.write_text(
        """
        //Adds 1 + ... + 100
                @i
                M=1 //i=1
                @sum
                M=0 //sum=0
        (LOOP)
                @i
                D=M //D=i
                @100
                D=D-A //D=i-100
                @END
                D;JGT // if (i-100) > 0, goto to END
                @i
                D=M //D=i
                @sum
                M=D+M
                @i
                M=M+1
                @LOOP
                0;JMP
        (END)
                @END
                0;JMP // infinite loop
                
        """  # noqa:W293
    )
    return filepath


@pytest.fixture
def expected_output_containing_everything(tmp_path: Path) -> Path:
    filepath: Path = tmp_path / "expected.hack"
    filepath.write_text(
        dedent(
            """
            0000000000010000
            1110111111001000
            0000000000010001
            1110101010001000
            0000000000010000
            1111110000010000
            0000000001100100
            1110010011010000
            0000000000010011
            1110001100000001
            0000000000010000
            1111110000010000
            0000000000010001
            1111000010001000
            0000000000010000
            1111110111001000
            0000000000000100
            1110101010000111
            0000000000010011
            1110101010000111
            """
        ).strip()
    )
    return filepath
