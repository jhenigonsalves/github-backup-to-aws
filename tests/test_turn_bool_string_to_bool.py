from main import turn_bool_string_to_bool


def test_turn_bool_string_to_bool():
    assert turn_bool_string_to_bool("false") == False
    assert turn_bool_string_to_bool("fAlse") == False
    assert turn_bool_string_to_bool("FALSE") == False
    assert turn_bool_string_to_bool("true") == True
    assert turn_bool_string_to_bool("tRue") == True
    assert turn_bool_string_to_bool("TRUE") == True
