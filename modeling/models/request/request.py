import datetime
from enum import Enum
import random
# TODO: добавить время IObaund


class RequestStatus(Enum):
    SolveRequest = 1
    DontSolveRequest = 3
    BadRequest = 2


class Request:
    def __init__(self, start_time: datetime.datetime, solve_time: datetime.timedelta) -> None:
        self.start_time: datetime.datetime = start_time
        self.solve_time: datetime.timedelta = solve_time
        self.wait_time: datetime.timedelta = datetime.timedelta(seconds=0)
        self.end_time: datetime.datetime = None
        self.status = RequestStatus.DontSolveRequest

    def wait(self, wait_time: datetime.timedelta) -> None:
        if wait_time < datetime.timedelta(seconds=0):
            wait_time = datetime.timedelta(seconds=0)
        self.wait_time += wait_time

    def solve(self, speed: int) -> None:
        self.status = RequestStatus.SolveRequest
        self.end_time = self.start_time + \
            self.wait_time + (self.solve_time / speed)

    def cancel(self):
        self.status = RequestStatus.BadRequest
        self.end_time = self.start_time

    def ignore(self):
        self.status = RequestStatus.DontSolveRequest
        self.end_time = self.start_time

    def get_start_solve_time(self) -> datetime.datetime:
        return self.start_time + self.wait_time

    def __str__(self) -> str:
        end_time_str = str(
            self.end_time) if self.end_time else "Not solved yet"
        return f"{self.status.name} - {self.start_time} - {self.solve_time} - {self.wait_time} - {end_time_str}"
