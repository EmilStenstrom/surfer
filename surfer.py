import time
import random
import argparse
from multiprocessing import Process
import requests
from surfer_helper import (
    ignore_keyboard_exception, resolve_post_hook, print_result
)

@ignore_keyboard_exception
def main(options):
    url = options["url"]
    num_processes = options["c"]
    num_requests = options["n"]
    response_callback = resolve_post_hook(options["post_hook"])

    processes = []
    for i in range(num_processes):
        p = Process(target=request, args=(i, url, num_requests, response_callback))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

@ignore_keyboard_exception
def request(i, url, num_requests, response_callback):
    for j in range(num_requests):
        time.sleep(2 * random.random())
        response = requests.get(url)
        print_result(i + 1, j + 1, response)

        responses = response_callback(response)
        if responses:
            for r in responses:
                print_result(i + 1, j + 1, r)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Surf your own site concurrently')
    parser.add_argument(
        'url',
        help='URL to use for testing. Example: http://localhost:8080',
    )
    parser.add_argument(
        '-c',
        type=int,
        default=1,
        help='Number of concurrent processes. Example: -c 10',
    )
    parser.add_argument(
        '-n',
        type=int,
        default=1,
        help='Number of requests per process. Example: -n 10',
    )
    parser.add_argument(
        '--post-hook',
        help="""
            Dotted path to a python module with a method called run
            that takes the completed response and does something custom.
            Can optionally return a list of new responses that will then be
            logged to console the same way normal requests are.
            Example: --post-hook my_module
            (where my_module.py is in the same directory and contains
            "def run(response): ...")
        """
    )
    kwargs = parser.parse_args()

    main(vars(kwargs))
