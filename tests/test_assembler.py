# type: ignore

import typing
from pathlib import Path
import pytest
from hackassembler.assembler import assemble
from hackassembler.parser import InvalidSyntaxError


def test_assemble_missing_input_file() -> None:
    with pytest.raises(FileNotFoundError):
        invalid_file_path: Path = Path("invalid_file_path")
        assemble(invalid_file_path)


@typing.no_type_check
@pytest.fixture
def test_file_with_wrong_extension(tmp_path: Path) -> Path:
    filepath: Path = tmp_path / "test.txt"
    filepath.write_text(
        """
        """  # noqa:W293
    )
    return filepath


def test_assemble_wrong_extension(test_file_with_wrong_extension: Path) -> None:
    expected_error_type: type[ValueError] = ValueError
    try:
        with pytest.raises(expected_error_type):
            assemble(test_file_with_wrong_extension)
    except Exception as e:
        pytest.fail(
            f"""
            Unexpected exception type raised:
            Expected: {expected_error_type.__name__}
            Actual: {e.__class__.__name__}
            """
        )


@typing.no_type_check
@pytest.fixture
def test_file_with_wrong_syntax(tmp_path: Path) -> Path:
    filepath: Path = tmp_path / "test.asm"
    filepath.write_text(
        """
        wrong syntax
        """  # noqa:W293
    )
    return filepath


def test_assemble_wrong_syntax(test_file_with_wrong_syntax: Path) -> None:
    expected_error_type: type[InvalidSyntaxError] = InvalidSyntaxError
    try:
        with pytest.raises(expected_error_type):
            assemble(test_file_with_wrong_syntax)
    except Exception as e:
        pytest.fail(
            f"""
            Unexpected exception type raised:
            Expected: {expected_error_type.__name__}
            Actual: {e.__class__.__name__}
            """
        )


@typing.no_type_check
@pytest.mark.parametrize(
    "input_asm_code, expected_hack_code", 
    [
        ("@5", "0000000000000101"),
        ("D=A", "1110110000010000"),
        ("M=D", "1110001100001000"),
        ("0;JMP", "1110101010000111"),
        ("@i", "0000000000010000"),
        ("M=1 //i=1", "1110111111001000"),
        ("M=0", "1110101010001000"),
        ("D=M", "1111110000010000"),
        ("@100", "0000000001100100"),
        ("D=D-A", "1110010011010000"),
        ("D;JGT", "1110001100000001"),
        
        
        ("M=D+M", "1111000010001000"),
        ("M=M+1", "1111110111001000"),
        ("0;JMP", "1110101010000111"),
        ("@5\nD=A", "0000000000000101\n1110110000010000"),
    ]
)  # type: ignore
def test_assemble_simple_files(input_asm_code: str, expected_hack_code: str, tmp_path: Path) -> None:
    filepath_expected_file = tmp_path / "expected.hack"
    filepath_expected_file.write_text(expected_hack_code)
    filepath_input_file = tmp_path / "input.asm"
    filepath_input_file.write_text(input_asm_code)
    assemble(filepath_input_file)
    filepath_output_file = filepath_input_file.with_suffix(".hack")
    assert (filepath_expected_file.read_text(encoding="utf-8") 
            == filepath_output_file.read_text(encoding="utf-8"))


def test_assemble_containing_everything(asm_file_containing_everything: Path, 
                                        expected_output_containing_everything: Path) -> None:
    assemble(asm_file_containing_everything)
    filepath_output_file: Path = asm_file_containing_everything.with_suffix(".hack")
    assert (open(expected_output_containing_everything, "r", encoding="utf-8").read() 
            == open(filepath_output_file, "r", encoding="utf-8").read())
