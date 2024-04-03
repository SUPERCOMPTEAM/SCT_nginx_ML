
from models.server.server_callback import ServerCallback


class UpstreamCallback:
    complete_factor_deviation: float = 0
    downtime_factor_deviation: float = 0
    overload_factor_deviation: float = 0

    def __init__(self, server_callbacks: list[ServerCallback]) -> None:
        self.complete_factor_deviation = UpstreamCallback.solve_average_deviation(
            [callback.complete_factor for callback in server_callbacks])
        self.downtime_factor_deviation = UpstreamCallback.solve_average_deviation(
            [callback.downtime_factor for callback in server_callbacks])
        self.overload_factor_deviation = UpstreamCallback.solve_average_deviation(
            [callback.overload_factor for callback in server_callbacks])

    def solve_average_deviation(factors: list[float]) -> float:
        center = 0
        for factor in factors:
            center += factor / len(factors)

        deviation = 0
        for factor in factors:
            deviation += abs(center - factor) / len(factors)

        return deviation

    def __str__(self) -> str:
        return f"complete_factor_deviation: {self.complete_factor_deviation}; downtime_factor_deviation: {self.downtime_factor_deviation}; overload_factor_deviation: {self.overload_factor_deviation}"
