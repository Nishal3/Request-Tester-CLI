import asyncio
import time
import os
import requests


def fetch(url):
    started_at = time.monotonic()
    response = requests.get(url)
    request_time = time.monotonic() - started_at
    return {"status_code": response.status_code, "request_time": request_time}


async def worker(name, queue, results):
    loop = asyncio.get_event_loop()
    while True:
        url = await queue.get()
        if os.getenv("DEBUG"):
            print(f"{name} - Fetching {url}")
        future_result = loop.run_in_executor(None, fetch, url)
        result = await future_result
        results.append(result)
        queue.task_done()


async def distribute_work(url, requests, concurrency, results):
    queue = asyncio.Queue()
    # Add an item to the queue for each request we want to make
    for _ in range(requests):
        queue.put_nowait(url)
    # Create workers to match the concurrency
    tasks = []
    for i in range(concurrency):
        task = asyncio.create_task(worker(f"worker-{i+1}", queue, results))
    tasks.append(task)
    started_at = time.monotonic()
    await queue.join()
    total_time = time.monotonic() - started_at
    for task in tasks:
        task.cancel()

    return total_time


def assault(url, requests, concurrency):
    """Entrypoint to making requests"""
    results = []
    total_time = asyncio.run(distribute_work(url, requests, concurrency, results))
    return (total_time, results)
