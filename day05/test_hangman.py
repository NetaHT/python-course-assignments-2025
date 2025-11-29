# test_hangman.py

import pytest
from hangman_BL import (
    is_one_english_letter,
    check_valid_input,
    show_hidden_word,
    check_win
)

# -----------------------------
# Tests for is_one_english_letter
# -----------------------------

def test_single_valid_letter():
    assert is_one_english_letter("a") is True

def test_capital_letter():
    assert is_one_english_letter("Z") is True

def test_multiple_letters_invalid():
    assert is_one_english_letter("ab") is False

def test_non_letter_invalid():
    assert is_one_english_letter("3") is False

def test_empty_string_invalid():
    assert is_one_english_letter("") is False


# -----------------------------
# Tests for check_valid_input
# -----------------------------

def test_valid_input_appends_letter():
    old = []
    assert check_valid_input("a", old) is True
    assert old == ["a"]

def test_duplicate_letter_invalid():
    old = ["a"]
    assert check_valid_input("a", old) is False
    assert old == ["a"]  # unchanged

def test_case_insensitivity():
    old = []
    check_valid_input("A", old)
    assert old == ["a"]


# -----------------------------
# Tests for show_hidden_word
# -----------------------------

def test_show_hidden_word_reveals_correctly(capsys):
    chosen = "genotype"
    guessed = ["g", "p"]
    expected = "g_ _ _ _ _ p_"

    result = show_hidden_word(chosen, guessed)
    captured = capsys.readouterr().out.strip()

    assert expected == captured


# -----------------------------
# Tests for check_win
# -----------------------------

def test_check_win_true():
    assert check_win("dog", ["d", "o", "g"]) is True

def test_check_win_false_missing_letters():
    assert check_win("dog", ["d", "o"]) is False

def test_check_win_case_insensitive():
    assert check_win("Dog", ["d", "o", "g"]) is True
