# Daily Python Snippets
# One useful function added each day.
# https://github.com/luisrodeguero/daily-python-snippets

# --- 2026-06-26 ---
def chunk_list(lst, size):
    """
    Split a list into chunks of a given size.
    Returns a generator of sub-lists.

    Example:
        list(chunk_list([1,2,3,4,5,6,7], 3))
        # => [[1,2,3],[4,5,6],[7]]
    """
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


# --- 2026-06-26 (2) ---
def flatten(nested, depth=None):
    """
    Recursively flatten a nested list up to an optional depth.

    Example:
        flatten([1, [2, [3, [4]]]])          # => [1, 2, 3, 4]
        flatten([1, [2, [3, [4]]]], depth=1) # => [1, 2, [3, [4]]]
    """
    result = []
    for item in nested:
        # If item is list-like and we haven't hit the depth limit, recurse
        if isinstance(item, list) and (depth is None or depth > 0):
            next_depth = None if depth is None else depth - 1
            result.extend(flatten(item, next_depth))
        else:
            result.append(item)
    return result


# --- 2026-06-27 ---
def retry(max_attempts=3, exceptions=(Exception,), delay=0):
    """
    Decorator that retries a function on failure.

    Args:
        max_attempts: Maximum number of attempts before re-raising.
        exceptions: Tuple of exception types to catch and retry on.
        delay: Seconds to wait between retries (0 = no wait).

    Example:
        @retry(max_attempts=3, exceptions=(ConnectionError,), delay=1)
        def fetch_data(url):
            ...
    """
    import time
    import functools

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    # Wait before next attempt (skip wait on final attempt)
                    if delay > 0 and attempt < max_attempts:
                        time.sleep(delay)
            # All attempts exhausted — re-raise the last exception
            raise last_exc
        return wrapper
    return decorator

