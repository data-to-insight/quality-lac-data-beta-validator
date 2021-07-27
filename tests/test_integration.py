"""Tests for all configured errors"""
import pytest
from validator903.config import configured_errors, column_names
import pandas as pd
from validator903.types import ErrorDefinition

def test_all_configured_errors():
    codes = []
    for error, _ in configured_errors:
        # Check that all errors are ErrorDefinition
        assert isinstance(error, ErrorDefinition), f'The returned error is not an ErrorDefinition ({error})'

        # Check types of the fields
        assert isinstance(error.code, str), f'The error code {error.code} is not a string!'
        assert isinstance(error.description, str), f'The error description {error.description} is not a string!'
        assert isinstance(error.affected_fields, list), f'The affected fields {error.affected_fields} is not a list!'
        assert all(isinstance(f, str) for f in error.affected_fields), f'Not all fields in affected_fields are strings!'
        
        assert error.code not in codes, f'Error code {error.code} is duplicated!'
        codes.append(error.code)

@pytest.mark.parametrize("data_choice", [
    pytest.param('dummy_empty_input', id='empty input with columns'),
    pytest.param('dummy_input_data', id='input with fake csvs'),
    pytest.param('{}', id='totally empty input'),
])
def test_all_configured_error_functions(data_choice, dummy_empty_input, dummy_input_data):
    dummy_data = eval(data_choice)
    for error_code, error_func in configured_errors:
        result = error_func(dummy_data)

        for table_name, error_list in result.items():
            assert table_name in dummy_data, f'Returned error table name {table_name} not recognized!'
            assert isinstance(error_list, list), f'Returned list of error locations {error_list} is not a list (its a {type(error_list)})!'
            for error_location in error_list:
                assert error_location in dummy_data[table_name].index, f'Location {error_location} not found in {table_name} index - check returned locations!'


