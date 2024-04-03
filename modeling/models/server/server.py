import datetime
import random

from models.server.server_callback import ServerCallback
from models.request.request import Request

class Server:
    def __init__(self, speed: float, safety: float, total_time: datetime.timedelta) -> None:
        self.requests: list[Request] = []
        self.solved_requests: list[Request] = []
        self.unsolved_requests: list[Request] = []
        
        self.speed: float = speed
        self.safety: float = safety
        self.active: bool = True
        self.overtime: bool = False

        self.total_time: datetime.timedelta = total_time
    
    def __str__(self) -> str:
        res = "Solved:\n"
        for request in self.solved_requests:
            res += "\t" + str(request) + "\n"
        res += "Unsolved:\n"
        for request in self.unsolved_requests:
            res += "\t" + str(request) + "\n"
        return res

    def add_request(self, req: Request) -> None:
        self.requests.append(req)

    def process_requests(self) -> ServerCallback:
        if len(self.requests) == 0:
            return
        sorted_requests = sorted(self.requests, key=lambda x: x.start_time)

        start_time: datetime.datetime = sorted_requests[0].start_time.replace()
        current_time: datetime.datetime = sorted_requests[0].start_time.replace()
        for request in sorted_requests:
            if random.random() > self.safety:
                self.active = False

            if self.total_time < current_time - start_time:
                self.overtime = True

            if not self.active and not self.overtime:
                request.cancel()
                self.unsolved_requests.append(request)
            elif not self.overtime:
                request.wait(current_time - request.start_time)
                request.solve(self.speed)
                self.solved_requests.append(request)
            else:
                request.ignore()
                self.unsolved_requests.append(request)

            current_time = request.end_time.replace()
        
        if self.solved_requests:
            if self.solved_requests[-1].end_time > start_time + self.total_time:
                self.solved_requests[-1].cancel()
                self.unsolved_requests.append(self.solved_requests.pop())

        return ServerCallback(self.solved_requests, self.unsolved_requests, self.total_time)
