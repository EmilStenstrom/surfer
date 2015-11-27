from functools import wraps

class SurferException(Exception):
    def __init__(self, url, error_str):
        self.url = url
        self.error_str = error_str
        super(SurferException, self).__init__()

def ignore_keyboard_exception(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except KeyboardInterrupt:
            pass  # Supress stacktrace when we kill the process manually
    return inner

def print_result(proc_i, req_i, response):
    print "Proc {proc_i}, Req {req_i}: {url} -> {code}, {elapsed} ms".format(
        proc_i=proc_i,
        req_i=req_i,
        url=response.url,
        code="OK" if response.status_code == 200 else "ERROR",
        elapsed=int(round(response.elapsed.total_seconds() * 1000)),
    )

def resolve_post_hook(post_hook):
    response_callback = lambda response: None
    if post_hook:
        module = __import__(post_hook)
        response_callback = module.run
        assert callable(response_callback), "Run method is not callable"

    return response_callback
