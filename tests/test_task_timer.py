import pytest
from datetime import timedelta

from task_timer import TaskTimer, ParseTimeExpressionError


@pytest.fixture()
def parse():
    return TaskTimer.parse_friendly_timedelta


class TestParseNiceTimeFormat:

    @pytest.mark.parametrize("time_str, seconds",
    [
        ('0s', 0), ('0m', 0), ('0h', 0), 
        ('1h', 3600), ('1m', 60),('1s', 1),
        ('1h1s', 3601), ('1m1s', 61),('1h1m', 3660),
        ('1h1m1s', 3661), ('1m34s', 94),('1m61s', 121)
    ])
    def test_parse_valid_formats(self, time_str, seconds, parse):
        assert parse(time_str) == seconds

    @pytest.mark.parametrize("invalid_str", ('', '45', '300m0', 'f', '-10s', '1me10s'))
    def test_invalid_formats(self, invalid_str, parse):
        try:
            parse(invalid_str)
        except ParseTimeExpressionError as e:
            assert str(e) == f"Could not parse time expression {invalid_str}. "
        

class TestCustomExceptions:
    def test_parse_time_expression_error(self):
        try:
            raise ParseTimeExpressionError('4xm50s')
        except ParseTimeExpressionError as e:
            assert str(e) == f"Could not parse time expression 4xm50s. "
        
        try:
            raise ParseTimeExpressionError('4xm50s', "custom")
        except ParseTimeExpressionError as e:
            assert str(e) == f"Could not parse time expression 4xm50s. custom"


class TestGetNiceTimeFormat:
    def test_seconds(self):
        expected = '00s'
        actual = TaskTimer.pprint_timedelta(timedelta(seconds=0))
        assert expected == actual

        expected = '29s'
        actual = TaskTimer.pprint_timedelta(timedelta(seconds=29))
        assert expected == actual

        expected = '59s'
        actual = TaskTimer.pprint_timedelta(timedelta(seconds=59))
        assert expected == actual

    def test_minutes(self):
        expected = '01m 00s'
        actual_seconds = 1*60
        actual = TaskTimer.pprint_timedelta(timedelta(seconds=actual_seconds))
        assert expected == actual

        expected = '01m 45s'
        actual_seconds = 1*60 + 45
        actual = TaskTimer.pprint_timedelta(timedelta(seconds=actual_seconds))
        assert expected == actual

        expected = '59m 59s'
        actual_seconds = 59*60 + 59
        actual = TaskTimer.pprint_timedelta(timedelta(seconds=actual_seconds))
        assert expected == actual
    
    def test_hours(self):
        expected = '1h 00m 00s'
        actual_seconds = 60*60
        actual = TaskTimer.pprint_timedelta(timedelta(seconds=actual_seconds))
        assert expected == actual

        expected = '4h 29m 37s'
        actual_seconds = 4*60*60 + 29*60 + 37
        actual = TaskTimer.pprint_timedelta(timedelta(seconds=actual_seconds))
        assert expected == actual