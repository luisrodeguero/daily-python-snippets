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


# --- 2026-06-27 ---
def levenshtein_distance(s1, s2):
    """
    Compute the Levenshtein (edit) distance between two strings.

    The edit distance is the minimum number of single-character operations
    (insertions, deletions, substitutions) required to transform s1 into s2.

    Example:
        levenshtein_distance("kitten", "sitting")  # => 3
        levenshtein_distance("flaw", "lawn")        # => 2
        levenshtein_distance("", "abc")             # => 3
    """
    m, n = len(s1), len(s2)

    # dp[i][j] = edit distance between s1[:i] and s2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: transforming empty string to s2[:j] costs j insertions
    for i in range(m + 1):
        dp[i][0] = i  # delete all chars from s1
    for j in range(n + 1):
        dp[0][j] = j  # insert all chars of s2

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                # Characters match — no extra cost
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Min cost among: substitute, delete from s1, insert from s2
                dp[i][j] = 1 + min(
                    dp[i - 1][j - 1],  # substitution
                    dp[i - 1][j],      # deletion
                    dp[i][j - 1],      # insertion
                )

    return dp[m][n]


# --- 2026-06-28 ---
import time
import functools

def retry(max_attempts=3, delay=1.0, exceptions=(Exception,)):
    """Decorator that retries a function on failure.

    Args:
        max_attempts: Maximum number of times to call the function.
        delay: Seconds to wait between attempts.
        exceptions: Tuple of exception types that trigger a retry.

    Example:
        @retry(max_attempts=5, delay=0.5, exceptions=(ConnectionError,))
        def fetch_data(url):
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    if attempt < max_attempts:
                        time.sleep(delay)  # pause before next attempt
            raise last_exc  # all attempts exhausted — re-raise last error
        return wrapper
    return decorator


# --- 2026-06-28 ---
def deep_merge(base, override):
    """
    Recursively merge two dicts, with override values winning.
    Unlike {**base, **override}, this merges nested dicts instead
    of replacing them wholesale.

    Example:
        base     = {'a': 1, 'b': {'x': 10, 'y': 20}}
        override = {'b': {'y': 99, 'z': 30}, 'c': 3}
        deep_merge(base, override)
        # => {'a': 1, 'b': {'x': 10, 'y': 99, 'z': 30}, 'c': 3}
    """
    result = dict(base)  # shallow copy so we don't mutate the original
    for key, val in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(val, dict):
            # Both sides are dicts — recurse instead of overwriting
            result[key] = deep_merge(result[key], val)
        else:
            result[key] = val  # scalar or new key — just overwrite
    return result


# --- 2026-06-28 ---
def camel_to_snake(name):
    """Convert a camelCase or PascalCase string to snake_case.

    Args:
        name: A camelCase or PascalCase identifier string.

    Returns:
        The snake_case equivalent string.

    Example:
        camel_to_snake('myVariableName')  # => 'my_variable_name'
        camel_to_snake('HTMLParser')      # => 'html_parser'
    """
    import re
    # Insert underscore between a lowercase letter (or digit) followed by an uppercase letter
    s1 = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
    # Insert underscore between consecutive uppercase letters followed by a lowercase letter
    # e.g. 'HTMLParser' -> 'HTML_Parser' before lowercasing
    s2 = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', s1)
    return s2.lower()


# --- 2026-06-28 ---
def retry(times=3, exceptions=(Exception,), delay=0):
    """Decorator that retries a function on failure.

    Args:
        times:      Maximum number of attempts (default 3).
        exceptions: Tuple of exception types to catch (default all).
        delay:      Seconds to wait between retries (default 0).

    Example:
        @retry(times=5, exceptions=(IOError,), delay=1)
        def fetch_data(url):
            ...
    """
    import time
    import functools

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)  # success — return immediately
                except exceptions as exc:
                    last_exc = exc
                    if attempt < times and delay:
                        time.sleep(delay)  # wait before next try
            raise last_exc  # all attempts exhausted — re-raise the last error
        return wrapper
    return decorator


# --- 2026-06-28 ---
def sliding_window(iterable, n):
    """Yield successive overlapping windows of size n from an iterable.

    Args:
        iterable: Any iterable (list, string, generator, …).
        n:        Window size (must be >= 1).

    Yields:
        Tuples of length n representing each consecutive window.

    Example:
        list(sliding_window([1, 2, 3, 4, 5], 3))
        # => [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
    """
    from collections import deque

    window = deque(maxlen=n)  # fixed-size buffer — oldest element is evicted automatically
    for item in iterable:
        window.append(item)
        if len(window) == n:
            yield tuple(window)  # only emit once the window is full

