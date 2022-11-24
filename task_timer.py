import time
from datetime import datetime, timedelta
import sys
import os
from math import floor
from typing import Union

import argparse


class ParseTimeExpressionError(Exception):
    
    def __init__(self, time_str, optional_message= ""):
        super().__init__(f"Could not parse time expression {time_str}. {optional_message}")


class TaskTimer:

    SLEEP_TIME = 0.5
    TIME_FORMAT = "%Y-%m-%d %I:%M:%S %p"


    def clear_screen():
        os.system('cls' if os.name=='nt' else 'clear')
    

    def pprint_timedelta(time_delta : Union[timedelta,int]) -> str :
        if type(time_delta) == timedelta:
            time_delta = time_delta.total_seconds()
        time_delta_str = None

        q, r = divmod(time_delta, 60)
        time_delta_str = str(floor(r)).zfill(2) + 's'
        if q != 0:
            q, r = divmod(q, 60)
            time_delta_str = str(floor(r)).zfill(2) + 'm ' + time_delta_str
            if q != 0:
                time_delta_str = str(floor(q)) + 'h ' + time_delta_str

        return time_delta_str
    

    def parse_friendly_timedelta(input_str) -> int :
        """
        Parses strings of the form 50s or 1m40s and returns the total seconds represented by the string
        """
        raise ParseTimeExpressionError(input_str)


    def get_arg_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description='Sets a timer for a particular task with optional checkpoints and optional end time')
        return parser


    def __init__(self, checkpoint_duration : int = 5*60, timer_duration : int = 30*60):
        self.reset_timer()
        self._checkpoint_duration = checkpoint_duration
        self._timer_duration = timer_duration

        self._start_time = datetime.now()
        self._checkpoint_start_time = datetime.now()
    

    def reset_timer(self):
        print('🔁 Resetting timer')
        self._elapsed_time_in_seconds = 0
        self._elapsed_checkpoint_time = 0


    def start_timer(self):
        TaskTimer.clear_screen()
        self.reset_timer()
        self._start_time = datetime.now()

        prev_iteration_time = datetime.now()
        num_checkpoints = self._timer_duration//self._checkpoint_duration
        checkpoints_ctr = 1
        
        print(f"🐣 Starting Timer at {self._start_time.strftime(self.TIME_FORMAT)} "+\
            f"for {TaskTimer.pprint_timedelta(self._timer_duration)} " +\
            f"with Checkpoints every {TaskTimer.pprint_timedelta(self._checkpoint_duration)}")
        print(f"🐣 Number of Checkpoints: {num_checkpoints}")

        while True:
            curr_iteration_time = datetime.now()
            iteration_elapsed_time = (curr_iteration_time - prev_iteration_time).total_seconds()

            self._elapsed_time_in_seconds += iteration_elapsed_time
            self._elapsed_checkpoint_time += iteration_elapsed_time

            prev_iteration_time = curr_iteration_time

            if self._elapsed_time_in_seconds > self._timer_duration:
                print('🏁 Timer Done!')
                return
            else:
                if self._elapsed_checkpoint_time > self._checkpoint_duration:
                    print(f"✅ {checkpoints_ctr}/{num_checkpoints} Checkpoint(s) passed.\
                         {TaskTimer.pprint_timedelta(self._elapsed_time_in_seconds)}")
                    self._elapsed_checkpoint_time = 0
                    checkpoints_ctr += 1

            time.sleep(self.SLEEP_TIME)
            

if __name__ == "__main__":
    task_timer = TaskTimer(checkpoint_duration=5*60, timer_duration=50*60)
    task_timer.start_timer()

    sys.exit(0)
