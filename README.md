# Surfer
A minimal load testing script in python with only one dependency. Supports running custom python code for each request.

# Usage:

Start 3 parallel processes that each to 2 requests:

    $ python surfer.py http://localhost:8080 -c3 -n2
    Proc 2, Req 1: http://localhost:8080/ -> OK, 37 ms
    Proc 2, Req 2: http://localhost:8080/ -> OK, 27 ms
    Proc 3, Req 1: http://localhost:8080/ -> OK, 27 ms
    Proc 1, Req 1: http://localhost:8080/ -> OK, 25 ms
    Proc 1, Req 2: http://localhost:8080/ -> OK, 29 ms
    Proc 3, Req 2: http://localhost:8080/ -> OK, 31 ms

Start 3 parallel processes that each to 2 requests, and use --post-hook to call a custom python command for each response:

    $ python surfer.py http://localhost:8080 -c3 -n2 --post-hook fetch_subresources
    Proc 2, Req 1: http://localhost:8080/ -> OK, 37 ms
    Proc 2, Req 1: http://localhost:8080/static/CACHE/css/b9a557deafba.css -> OK, 3 ms
    Proc 2, Req 1: http://localhost:8080/static/CACHE/js/d40fb31a73ac.js -> OK, 2 ms
    Proc 2, Req 2: http://localhost:8080/ -> OK, 27 ms
    Proc 2, Req 2: http://localhost:8080/static/CACHE/css/b9a557deafba.css -> OK, 3 ms
    Proc 2, Req 2: http://localhost:8080/static/CACHE/js/d40fb31a73ac.js -> OK, 3 ms
    Proc 3, Req 1: http://localhost:8080/ -> OK, 27 ms
    Proc 3, Req 1: http://localhost:8080/static/CACHE/css/b9a557deafba.css -> OK, 3 ms
    Proc 3, Req 1: http://localhost:8080/static/CACHE/js/d40fb31a73ac.js -> OK, 2 ms
    Proc 1, Req 1: http://localhost:8080/ -> OK, 25 ms
    Proc 1, Req 1: http://localhost:8080/static/CACHE/css/b9a557deafba.css -> OK, 3 ms
    Proc 1, Req 1: http://localhost:8080/static/CACHE/js/d40fb31a73ac.js -> OK, 2 ms
    Proc 1, Req 2: http://localhost:8080/ -> OK, 29 ms
    Proc 1, Req 2: http://localhost:8080/static/CACHE/css/b9a557deafba.css -> OK, 3 ms
    Proc 1, Req 2: http://localhost:8080/static/CACHE/js/d40fb31a73ac.js -> OK, 2 ms
    Proc 3, Req 2: http://localhost:8080/ -> OK, 31 ms
    Proc 3, Req 2: http://localhost:8080/static/CACHE/css/b9a557deafba.css -> OK, 4 ms
    Proc 3, Req 2: http://localhost:8080/static/CACHE/js/d40fb31a73ac.js -> OK, 2 ms

# Docs

    $ python surfer.py -h
    usage: surfer.py [-h] [-c C] [-n N] [--post-hook POST_HOOK] url

    Surf your own site concurrently

    positional arguments:
      url                   URL to use for testing. Example: http://localhost:8080

    optional arguments:
      -h, --help            show this help message and exit
      -c C                  Number of concurrent processes. Example: -c 10
      -n N                  Number of requests per process. Example: -n 10
      --post-hook POST_HOOK
                            Dotted path to a python module with a method called
                            run that takes the completed response and does
                            something custom. Can optionally return a list of new
                            responses that will then be logged to console the same
                            way normal requests are. Example: --post-hook
                            my_module (where my_module.py is in the same directory
                            and contains "def run(response): ...")
