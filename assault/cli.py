import click
import json
import sys
from typing import TextIO

from .http import assault
from .stats import Results


@click.command()
@click.option("--requests", "-r", default=500, help="Number of requests")
@click.option("--concurrency", "-c", default=1, help="Number of concurrent requests")
@click.option("--json-file", "-j", default=None, help="Path to output JSON file")
@click.argument("url")
def cli(requests, concurrency, json_file, url):
    output_file = None
    if json_file:
        try:
            output_file = open(json_file, "w")
        except:
            print("Could not open file: {json_file}")
            sys.exit(1)

    total_time, request_dicts = assault(url, requests, concurrency)
    result = Results(total_time, request_dicts)
    display(result, output_file)


def display(result: Results, json_file: TextIO):
    if json_file:
        # Writing to JSON file
        print("Writing to a JSON file...")
        json.dump(
            {
                "successful_requests": result.successful_requests(),
                "slowest": result.slowest(),
                "fastest": result.fastest(),
                "average": result.average_time(),
                "total_time": result.total_time,
                "requests_per_minute": result.requests_per_minute(),
                "requests_per_second": result.requests_per_second(),
            },
            json_file,
        )
        json_file.close()
        print("... Done!")
    else:
        # Printing to terminal
        print(
            f"... Done!\n"
            + f"--- Results ---\n"
            + f"Successful requests\t{result.successful_requests()}\n"
            + f"Slowest            \t{result.slowest()}\n"
            + f"Fastest            \t{result.fastest()}\n"
            + f"Average            \t{result.average_time()}\n"
            + f"Total time         \t{result.total_time}\n"
            + f"Requests Per Minute\t{result.requests_per_minute()}\n"
            + f"Requests Per Second\t{result.requests_per_second()}\n"
        )
