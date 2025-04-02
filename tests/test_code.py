# type: ignore

import typing

import pytest

from src.code import translate_command_into_binary_code
from src.commands import Comp, Dest, Jump, CCommand, ACommand, LCommand


@typing.no_type_check
@pytest.mark.parametrize(
    "comp, expected_comp_binary_code",
    [
        (Comp.zero, "0101010"),
        (Comp.one, "0111111"),
        (Comp.minus_one, "0111010"),
        (Comp.d, "0001100"),
        (Comp.a, "0110000"),
        (Comp.not_d, "0001101"),
        (Comp.not_a, "0110001"),
        (Comp.minus_d, "0001111"),
        (Comp.minus_a, "0110011"),
        (Comp.d_plus_1, "0011111"),
        (Comp.a_plus_1, "0110111"),
        (Comp.d_minus_1, "0001110"),
        (Comp.a_minus_1, "0110010"),
        (Comp.d_plus_a, "0000010"),
        (Comp.d_minus_a, "0010011"),
        (Comp.a_minus_d, "0000111"),
        (Comp.d_and_a, "0000000"),
        (Comp.d_or_a, "0010101"),

        (Comp.m, "1110000"),
        (Comp.not_m, "1110001"),
        (Comp.minus_m, "1110011"),
        (Comp.m_plus_1, "1110111"),
        (Comp.m_minus_1, "1110010"),
        (Comp.d_plus_m, "1000010"),
        (Comp.d_minus_m, "1010011"),
        (Comp.m_minus_d, "1000111"),
        (Comp.d_and_m, "1000000"),
        (Comp.d_or_m, "1010101"),
    ]
)
def test_c_command_comp(comp: Comp, expected_comp_binary_code: str) -> None:
    command: CCommand = CCommand(comp=comp, dest=Dest.Null, jump=Jump.Null)
    command_in_binary_code = translate_command_into_binary_code(command)
    expected_binary_code: str = "111" + expected_comp_binary_code + "000" + "000"
    assert command_in_binary_code == expected_binary_code


@typing.no_type_check
@pytest.mark.parametrize(
    "dest, expected_dest_binary_code",
    [
        (Dest.Null, "000"),
        (Dest.Null, "000"),
        (Dest.M, "001"),
        (Dest.D, "010"),
        (Dest.MD, "011"),
        (Dest.A, "100"),
        (Dest.AM, "101"),
        (Dest.AD, "110"),
        (Dest.AMD, "111"),
    ]
)
def test_c_command_dest(dest: Dest, expected_dest_binary_code: str) -> None:
    command: CCommand = CCommand(comp=Comp.zero, dest=dest, jump=Jump.Null)
    command_in_binary_code = translate_command_into_binary_code(command)
    comp_zero_binary_code: str = "0101010"
    expected_binary_code: str = "111" + comp_zero_binary_code + expected_dest_binary_code + "000"
    assert command_in_binary_code == expected_binary_code


@typing.no_type_check
@pytest.mark.parametrize(
    "jump, expected_jump_binary_code",
    [
        (Jump.Null, "000"),
        (Jump.JGT, "001"),
        (Jump.JEQ, "010"),
        (Jump.JGE, "011"),
        (Jump.JLT, "100"),
        (Jump.JNE, "101"),
        (Jump.JLE, "110"),
        (Jump.JMP, "111"),
    ]
)
def test_c_command_jump(jump: Jump, expected_jump_binary_code: str) -> None:
    command: CCommand = CCommand(comp=Comp.zero, dest=Dest.Null, jump=jump)
    command_in_binary_code = translate_command_into_binary_code(command)
    expected_binary_code: str = "111" + "0101010" + "000" + expected_jump_binary_code
    assert command_in_binary_code == expected_binary_code


def test_l_command() -> None:
    command: LCommand = LCommand(label="label")
    command_in_binary_code = translate_command_into_binary_code(command)
    assert command_in_binary_code == ""


def test_a_command_symbol_address() -> None:
    symbol_table = {"Loop": "2", "End": "5"}
    command: ACommand = ACommand(symbol_address="Loop")
    command_in_binary_code = translate_command_into_binary_code(command=command, symbol_table=symbol_table)
    assert command_in_binary_code == "0000000000000010"
    command = ACommand(symbol_address="End")
    command_in_binary_code = translate_command_into_binary_code(command=command, symbol_table=symbol_table)
    assert command_in_binary_code == "0000000000000101"


@typing.no_type_check
@pytest.mark.parametrize(
    "address, expected_binary_code",
    [
        ("0", "0000000000000000"),
        ("1", "0000000000000001"),
        ("2", "0000000000000010"),
        ("3", "0000000000000011"),
        ("4", "0000000000000100"),
        ("0", "0000000000000000"),
        ("32766", "0111111111111110"),
        ("32767", "0111111111111111"),

    ]
)
def test_a_command_raw_address(address: str, expected_binary_code: str) -> None:
    command: ACommand = ACommand(raw_address=address)
    command_in_binary_code = translate_command_into_binary_code(command)
    assert command_in_binary_code == expected_binary_code
