
import datetime
from models.request.request import Request


class ServerCallback:

    complete_factor: float = None
    overload_factor: float = None
    downtime_factor: float = None
    solved_requests: list[Request] = []
    unsolved_request: list[Request] = []

    def __init__(self, solved_requests: list[Request], unsolved_request: list[Request], total_time: datetime.timedelta) -> None:
        self.solved_requests = solved_requests
        self.unsolved_request = unsolved_request
        self.complete_factor = ServerCallback.solve_complete_factor(
            solved_requests, unsolved_request)
        self.overload_factor = ServerCallback.solve_overload_factor(
            solved_requests, total_time)
        self.downtime_factor = ServerCallback.solve_downtime_factor(
            solved_requests, total_time)

    def solve_complete_factor(solved_requests: list[Request], unsolved_request: list[Request]):
        return len(solved_requests) / (len(solved_requests) + len(unsolved_request))

    def solve_downtime_factor(requests: list[Request], total_time: datetime.timedelta):
        if len(requests) == 0:
            return 1

        downtime = datetime.timedelta()
        for i in range(len(requests) - 1):
            downtime += requests[i+1].get_start_solve_time() - \
                requests[i].end_time

        downtime += (requests[0].start_time + total_time) - \
            requests[len(requests) - 1].end_time

        return downtime / total_time

    def solve_overload_factor(requests: list[Request], total_time: datetime.timedelta):
        if not requests:
            return 0

        flat_intervals = []
        for idx, request in enumerate(requests):
            flat_intervals.append((request.start_time, 1, idx))
            flat_intervals.append((request.end_time, -1, idx))

        flat_intervals.sort()

        current_intersections = 0
        total_intersection = datetime.timedelta()
        prev_time = flat_intervals[0][0]
        active_requests = set()

        for time, delta, idx in flat_intervals:
            if delta == 1:
                active_requests.add(idx)
            else:
                active_requests.remove(idx)

            unique_requests_count = len(set(active_requests))
            if unique_requests_count > 0:
                total_intersection += (time - prev_time)
            prev_time = time

        return total_intersection / total_time

    def __str__(self) -> str:
        return f"complete_factor: {self.complete_factor}; overload_factor: {self.overload_factor}; downtime_factor: {self.downtime_factor};"
