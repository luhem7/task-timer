from datetime import timedelta

from task_timer import TaskTimer

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