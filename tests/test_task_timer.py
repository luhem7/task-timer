from datetime import timedelta

from task_timer import TaskTimer, ParseTimeExpressionError


class TestParseNiceTimeFormat:
    def test_invalid_formats(self):
        parse = TaskTimer.parse_friendly_timedelta

        for invalid_str in ['', '45', '300m0', 'f']:
            try:
                parse(invalid_str)
                assert False
            except ParseTimeExpressionError as e:
                assert str(e) == f"Could not parse time expression {invalid_str}. "
                continue
        

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