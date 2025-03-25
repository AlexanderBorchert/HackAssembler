# type: ignore
from pathlib import Path

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
def asm_file_containing_A_Command(tmp_path: Path) -> Path:
    filepath: Path = tmp_path / "test.asm"
    filepath.write_text(
        """
        @5
        """
    )
    return filepath


@pytest.fixture
def asm_file_containing_C_Command(tmp_path: Path) -> Path:
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
