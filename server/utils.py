def assert_expected_keys_list(actual_keys, expected_length, expected_keys):
    '''
    Asserts that the list keys contains the expected strings at the correct location.
    Parameters:
        actual_keys (list): A list of keys to be analyzed
        expected_length (int): Expected length of actual_keys
        expected_keys (list): A list of keys expected to be in the same order as actual_keys
    Returns:
        None
    Raises:
        AssertionError: An expected string was not found at the expected index (message provides information),
            or the length of the provided list is not as expected.
    '''
    assert type(actual_keys) == list
    assert type(expected_length) == int
    assert type(expected_keys) == list

    assertion_error_message = '{} key not found at correct index'
    assert len(actual_keys) == expected_length, 'Unexpected keys list column length'

    for i, expected_key in enumerate(expected_keys):
        assert actual_keys[i] == expected_key, assertion_error_message.format(expected_key)

def get_header_key_indexes(headers, expected_strings_list):
    '''
    Returns a dictionary where keys are expected strings, and corresponding values are the index at which
    the expected string was found.
    Parameters:
        headers (str): A string
        expected_strings_list (list): List of expected strings
    Returns:
        indexes (dict of str -> int): Dictionary with keys expected string and corresponding values the index
            in the string where it is found.
    Raises:
        ValueError: If any of the expected strings are not found in headers.
    '''
    assert type(headers) == str
    assert type(expected_strings_list) == list

    indexes = {}
    for expected_string in expected_strings_list:
        indexes[expected_string] = headers.index(expected_string)
    return indexes