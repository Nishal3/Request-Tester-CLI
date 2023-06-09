from typing import List, Dict


class Results:
    """
    Results handles calculating statistics based on a list of requests that are made.
    Here's and example of what that would look like:
    --- Results ---
    Successful requests 3000
    Slowest 0.010s
    Fastest 0.001s
    Average 0.003s
    Total time 2.400s
    Requests Per Minute 90000
    Requests Per Second 1250
    """

    def __init__(self, total_time: float, requests: List[Dict]):
        self.total_time = total_time
        self.requests = sorted(
            requests, key=lambda r: r["request_time"]
        )  # Number that is sorted is the request times, by descending order

    def slowest(self) -> float:
        """
        Returns the slowest request's completion time

        >>> results = Results(10.6, [{
        ...     'status_code': 200,
        ...     'request_time': 3.4,
        ... }, {
        ...     'status_code': 500,
        ...     'request_time': 6.1,
        ... }, {
        ...     'status_code': 200,
        ...     'request_time': 1.04,
        ... }])
        >>> results.slowest()
        6.1
        """
        return self.requests[-1]["request_time"]

    def fastest(self) -> float:
        """
        Returns the fastest request's completion time

        >>> results = Results(10.6, [{
        ...     'status_code': 200,
        ...     'request_time': 3.4,
        ... }, {
        ...     'status_code': 500,
        ...     'request_time': 6.1,
        ... }, {
        ...     'status_code': 200,
        ...     'request_time': 1.04,
        ... }])
        >>> results.fastest()
        1.04
        """
        return self.requests[0]["request_time"]

    def average_time(self) -> float:
        """
        Returns the average request completion time

        >>> results = Results(10.6, [{
        ...     'status_code': 200,
        ...     'request_time': 3.4,
        ... }, {
        ...     'status_code': 500,
        ...     'request_time': 6.1,
        ... }, {
        ...     'status_code': 200,
        ...     'request_time': 1.04,
        ... }])
        >>> results.average_time()
        3.513333333333333
        """
        return sum(
            list(map(lambda requests: requests["request_time"], self.requests))
        ) / len(self.requests)

    def successful_requests(self) -> int:
        """
        Returns the number of successful requests

        >>> results = Results(10.6, [{
        ...     'status_code': 200,
        ...     'request_time': 3.4,
        ... }, {
        ...     'status_code': 500,
        ...     'request_time': 6.1,
        ... }, {
        ...     'status_code': 200,
        ...     'request_time': 1.04,
        ... }])
        >>> results.successful_requests()
        2
        """
        return len([r for r in self.requests if r["status_code"] in range(200, 299)])

    def requests_per_minute(self) -> int:
        """
        Returns the number requests that could be made in a minute

        >>> results = Results(10.6, [{
        ...     'status_code': 200,
        ...     'request_time': 3.4,
        ... }, {
        ...     'status_code': 500,
        ...     'request_time': 6.1,
        ... }, {
        ...     'status_code': 200,
        ...     'request_time': 1.04,
        ... }])
        >>> results.requests_per_minute()
        17
        """

        return round(60 * len(self.requests) / self.total_time)

    def requests_per_second(self) -> int:
        """
        Returns the number requests that could be made in a second

        >>> results = Results(3.5, [{
        ...     'status_code': 200,
        ...     'request_time': 3.4,
        ... }, {
        ...     'status_code': 500,
        ...     'request_time': 2.9,
        ... }, {
        ...     'status_code': 200,
        ...     'request_time': 1.04,
        ... }, {
        ...     'status_code': 200,
        ...     'request_time': 0.4
        ... }])
        >>> results.requests_per_second()
        1
        """

        return round(len(self.requests) / self.total_time)
