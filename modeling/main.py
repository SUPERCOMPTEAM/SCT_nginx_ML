import datetime
from models import Upstream

print(Upstream(4, 100, datetime.timedelta(seconds=10)).start_round_robin([1, 1, 1, 1]))


# from models import Request
# from models import Server

# requests = [
#     Request(datetime.datetime(2024, 3, 30, 8, 0, 0), datetime.timedelta(seconds=1)),
#     Request(datetime.datetime(2024, 3, 30, 8, 0, 0), datetime.timedelta(seconds=1)),
#     Request(datetime.datetime(2024, 3, 30, 8, 0, 0), datetime.timedelta(seconds=1)),
#     Request(datetime.datetime(2024, 3, 30, 8, 0, 0), datetime.timedelta(seconds=1)),
#     Request(datetime.datetime(2024, 3, 30, 8, 0, 0), datetime.timedelta(seconds=1)),
# ]

# server = Server(1, 1, datetime.timedelta(seconds=5))

# for request in requests:
#     server.add_request(request)

# print(server.process_requests())
# print(server)
