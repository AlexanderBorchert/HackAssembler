import typing

import pytest

from src.code import translate_command_into_binary_code
from src.commands import Comp, Dest, Jump


@typing.no_type_check
@pytest.mark.parametrize(
    "command, expected_binary_code",
    [
        pytest.param(Comp.zero, "0101010", id="Comp.zero"),
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

        (Dest.Null, "000"),
        (Dest.M, "001"),
        (Dest.D, "010"),
        (Dest.MD, "011"),
        (Dest.A, "100"),
        (Dest.AM, "101"),
        (Dest.AD, "110"),
        (Dest.AMD, "111"),

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
def test_translate_command_into_binary_code(command: Comp, expected_binary_code: str) -> None:
    assert translate_command_into_binary_code(command) == expected_binary_code
