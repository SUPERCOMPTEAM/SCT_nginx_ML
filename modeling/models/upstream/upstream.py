import datetime
import random
from models.request.request import Request
from models.server.server import Server


class Upstream:
    def __init__(self, server_count: int, request_count: int, time_interval: datetime.timedelta) -> None:

        solve_times = [
            datetime.timedelta(seconds=random.randint(1, 3)),
            datetime.timedelta(seconds=random.randint(1, 3)),
            datetime.timedelta(seconds=random.randint(1, 3)),
            datetime.timedelta(seconds=random.randint(1, 3))
        ]
        
        unsorted_request_list = [
            Request(
                datetime.datetime.now() - datetime.timedelta(seconds=random.randint(0, time_interval.total_seconds())), 
                random.choice(solve_times)
            ) for _ in range(request_count)
        ]
        self.request_list = sorted(unsorted_request_list, key=lambda x: x.start_time)

        self.server_list: list[Server] = [
            Server(
                random.uniform(0.75, 1.25),
                random.uniform(0.99, 1),
                time_interval
            ) for _ in range(server_count)
        ]

        self.complete_factors: list[float] = []
        self.overload_factors: list[float] = []
        self.downtime_factors: list[float] = []


    def start_round_robin(self, weight_list: list[int]) -> None:
        server_idx_list = []
        for i in range(len(self.server_list)):
            for _ in range(weight_list[i]):
                server_idx_list.append(i)
        random.shuffle(server_idx_list)

        for i, request in enumerate(self.request_list):
            self.server_list[server_idx_list[i % len(server_idx_list)]].add_request(request)
        
        for i, server in enumerate(self.server_list):
            callback = server.process_requests()
            self.complete_factors.append(callback.complete_factor)
            self.overload_factors.append(callback.overload_factor)
            self.downtime_factors.append(callback.downtime_factor)
    
    def __str__(self) -> str:
        return f"complete_factors: {self.complete_factors}\noverload_factors: {self.overload_factors}\ndowntime_factors: {self.downtime_factors}"
