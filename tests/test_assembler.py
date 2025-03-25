# import typing
# from pathlib import Path
# import pytest
# from src.assembler import assemble
# from src.parser import InvalidSyntaxError


# def test_assemble_missing_input_file() -> None:
#     with pytest.raises(FileNotFoundError):
#         invalid_file_path: Path = Path("invalid_file_path")
#         assemble(invalid_file_path)
# 
# 
# @typing.no_type_check
# @pytest.fixture
# def test_file_with_wrong_extension(tmp_path: Path) -> Path:
#     filepath: Path = tmp_path / "test.txt"
#     filepath.write_text(
#         """
#         """  # noqa:W293
#     )
#     return filepath
# 
# 
# def test_assemble_wrong_extension(test_file_with_wrong_extension: Path) -> None:
#     expected_error_type: type[ValueError] = ValueError
#     try:
#         with pytest.raises(expected_error_type):
#             assemble(test_file_with_wrong_extension)
#     except Exception as e:
#         pytest.fail(
#             f"""
#             Unexpected exception type raised:
#             Expected: {expected_error_type.__name__}
#             Actual: {e.__class__.__name__}
#             """
#         )
# 
# 
# @typing.no_type_check
# @pytest.fixture
# def test_file_with_wrong_syntax(tmp_path: Path) -> Path:
#     filepath: Path = tmp_path / "test.asm"
#     filepath.write_text(
#         """
#         wrong syntax
#         """  # noqa:W293
#     )
#     return filepath
# 
# 
# def test_assemble_wrong_syntax(test_file_with_wrong_syntax: Path) -> None:
#     expected_error_type: type[InvalidSyntaxError] = InvalidSyntaxError
#     try:
#         with pytest.raises(expected_error_type):
#             assemble(test_file_with_wrong_syntax)
#     except Exception as e:
#         pytest.fail(
#             f"""
#             Unexpected exception type raised:
#             Expected: {expected_error_type.__name__}
#             Actual: {e.__class__.__name__}
#             """
#         )
# 
# 
# test_cases_simple_files: typing.List[typing.Tuple[str, str]] = [
#     # ("@5", "0000000000000101"),
#     # ("D=A", "1110110000010000"),
#     # ("M=D", "1110001100001000"),
#     # ("0;JMP", "1110101010000111"),
#     ("@5\nD=A", "0000000000000101\n1110110000010000"),
# 
# ]


# @typing.no_type_check
# @pytest.fixture
# @pytest.mark.parametrize("input_asm_code, expected_hack_code", test_cases_simple_files)
# def test_assemble_simple_files(input_asm_code: str, expected_hack_code: str, tmp_path: Path) -> None:
#     filepath_expected_file: Path = tmp_path / "expected.hack"
#     filepath_expected_file.write_text(expected_hack_code)
#     filepath_input_file: Path = tmp_path / "input.asm"
#     filepath_input_file.write_text(input_asm_code)
#     assemble(filepath_input_file)
#     filepath_output_file: Path = filepath_input_file.with_suffix(".hack")
#     assert (open(filepath_expected_file, "r", encoding="utf-8").read() 
#             == open(filepath_output_file, "r", encoding="utf-8").read())


# # @typing.no_type_check
# # @pytest.fixture
# # def test_asm_file(tmp_path: Path) -> Path:
# #     filepath: Path = tmp_path / "test.asm"
# #     filepath.write_text(
# #         """
# #         """  # noqa:W293
# #     )
# #     return filepath
# #
# #
# # def test_assemble(test_asm_file: Path) -> None:
# #     assembler(test_asm_file)
# #     # check that there is a file with path like test_asm_file but just extension has .hack instead of .asm
# #     #     assert parser.has_more_commands()
# 
# 
# # """
# # //comment
# #
# # @5
# # M  =  1 //comment
# # 0;JMP
# #
# # D=M;JGT
# #
# #
# # """  # noqa:W293
# 
# # assert open(file_path_1, "r", encoding="utf-8").read() == open(file_path_2, "r", encoding="utf-8").read()
