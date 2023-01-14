from flusso.option import Some, Nothing

def test_some_case():
    # Test some case
    option_value = Some(5)
    assert option_value.unwrap() == 5
    assert option_value.is_some() == True
    assert option_value.is_none() == False
    assert option_value.map(lambda x: x*2).unwrap() == 10
    assert option_value.filter(lambda x: x > 4).unwrap() == 5
    assert option_value.and_then(lambda x: Some(x*3)).unwrap() == 15
    assert option_value.or_(Nothing).unwrap() == 5
    assert option_value.or_else(lambda: Nothing).unwrap() == 5
    assert option_value.and_(Nothing).is_none() == True
    assert option_value.ok_or("Error") == (True, 5)
    assert option_value.unwrap_or(10) == 5
    assert option_value.unwrap_or_else(lambda: 10) == 5

def test_nothing_case():
    # Test none case
    option_value = Nothing
    try:
        option_value.unwrap()
        assert False, "Should raise ReferenceError"
    except ReferenceError:
        assert True
    assert option_value.is_some() == False
    assert option_value.is_none() == True
    assert option_value.map(lambda x: x*2).is_none() == True
    assert option_value.filter(lambda x: x > 4).is_none() == True
    assert option_value.and_then(lambda x: Some(x*3)).is_none() == True
    assert option_value.or_(Some(5)).unwrap() == 5
    assert option_value.or_else(lambda: Some(5)).unwrap() == 5
    assert option_value.and_(Some(5)).is_some() == True
    assert option_value.ok_or("Error") == (False, "Error")
    assert option_value.unwrap_or(10) == 10
    assert option_value.unwrap_or_else(lambda: 10) == 10
    