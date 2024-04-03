import datetime
import random
from models.request.request import Request
from models.server.server import Server
from models.upstream.upstream_callback import UpstreamCallback


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
                random.uniform(0.99, 1.01),
                random.uniform(0.99, 1),
                time_interval
            ) for _ in range(server_count)
        ]

    def start_round_robin(self, weight_list: list[int]) -> UpstreamCallback:
        server_idx_list = []
        for i in range(len(self.server_list)):
            for _ in range(weight_list[i]):
                server_idx_list.append(i)
        random.shuffle(server_idx_list)

        for i, request in enumerate(self.request_list):
            self.server_list[server_idx_list[i % len(server_idx_list)]].add_request(request)
        
        callbacks = []
        for i, server in enumerate(self.server_list):
            callbacks.append(server.process_requests())
        
        return UpstreamCallback(callbacks)
