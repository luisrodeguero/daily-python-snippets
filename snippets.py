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


# --- 2026-06-28 ---
def flatten(nested, depth=None):
    """Recursively flatten a nested list (or any iterable) to a single list.

    Args:
        nested: A (possibly nested) iterable to flatten.
        depth:  How many levels deep to flatten. None means fully flatten.

    Returns:
        A flat list of all leaf elements.

    Example:
        flatten([1, [2, [3, [4]]], 5])        # => [1, 2, 3, 4, 5]
        flatten([1, [2, [3, [4]]], 5], depth=1) # => [1, 2, [3, [4]], 5]
    """
    result = []
    for item in nested:
        # Recurse if item is a non-string iterable and depth budget remains
        if hasattr(item, '__iter__') and not isinstance(item, (str, bytes)):
            if depth is None:
                result.extend(flatten(item, depth=None))      # unlimited depth
            elif depth > 0:
                result.extend(flatten(item, depth=depth - 1)) # reduce remaining depth
            else:
                result.append(item)  # depth exhausted — treat as leaf
        else:
            result.append(item)  # scalar or string — always a leaf
    return result


# --- 2026-06-29 (1/4) ---
def camel_to_snake(name):
    """Convert a camelCase or PascalCase string to snake_case.

    Args:
        name: The camelCase or PascalCase string to convert.

    Returns:
        The snake_case equivalent string.

    Example:
        >>> camel_to_snake('myVariableName')
        'my_variable_name'
        >>> camel_to_snake('HTMLParser')
        'h_t_m_l_parser'
    """
    import re
    # Insert underscore before any uppercase letter that follows a lowercase letter or digit
    s1 = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
    # Insert underscore before any uppercase letter that is followed by a lowercase letter
    # (handles runs like 'HTML' -> 'H_T_M_L' edge cases)
    result = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', s1)
    return result.lower()


# --- 2026-06-29 (2/4) ---
def sieve_of_eratosthenes(limit):
    """Return a list of all prime numbers up to and including *limit*.

    Uses the classic Sieve of Eratosthenes algorithm with O(n log log n)
    time complexity and O(n) space complexity.

    Args:
        limit: Upper bound (inclusive) to search for primes. Must be >= 2.

    Returns:
        A sorted list of prime integers <= limit.

    Example:
        >>> sieve_of_eratosthenes(30)
        [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    """
    if limit < 2:
        return []

    # Boolean sieve: index i is True if i is (still) considered prime
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False  # 0 and 1 are not prime

    # Only need to test up to sqrt(limit)
    for start in range(2, int(limit ** 0.5) + 1):
        if is_prime[start]:
            # Mark all multiples of start as composite
            for multiple in range(start * start, limit + 1, start):
                is_prime[multiple] = False

    return [n for n, prime in enumerate(is_prime) if prime]


# --- 2026-06-29 (3/4) ---
import time
import functools

def retry(max_attempts=3, delay=1.0, exceptions=(Exception,)):
    """Decorator that retries a function on failure.

    Args:
        max_attempts: Maximum number of attempts before re-raising (default 3).
        delay:        Seconds to wait between attempts (default 1.0).
        exceptions:   Tuple of exception types to catch (default catches all).

    Returns:
        Decorator that wraps the target function with retry logic.

    Example:
        @retry(max_attempts=5, delay=2.0, exceptions=(ConnectionError,))
        def fetch_data(url):
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)          # success — return immediately
                except exceptions as exc:
                    last_exc = exc
                    if attempt < max_attempts:
                        time.sleep(delay)                 # wait before retrying
            raise last_exc                                # all attempts exhausted
        return wrapper
    return decorator


# --- 2026-06-29 (4/4) ---
def sliding_window(iterable, size, step=1):
    """Yield successive overlapping (or non-overlapping) windows from an iterable.

    Args:
        iterable: Any iterable to slide over.
        size:     Number of elements in each window.
        step:     Number of positions to advance between windows (default 1).

    Yields:
        Tuples of length *size* drawn from the iterable.

    Example:
        >>> list(sliding_window(range(6), size=3))
        [(0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5)]
        >>> list(sliding_window(range(6), size=3, step=2))
        [(0, 1, 2), (2, 3, 4)]
    """
    from collections import deque

    it = iter(iterable)
    window = deque(maxlen=size)

    # Seed the window with the first *size* elements
    for _ in range(size):
        try:
            window.append(next(it))
        except StopIteration:
            return  # iterable shorter than window — yield nothing

    yield tuple(window)

    # Slide forward *step* positions at a time
    advance = 0
    for item in it:
        window.append(item)   # deque auto-discards oldest when maxlen reached
        advance += 1
        if advance == step:
            yield tuple(window)
            advance = 0


# --- 2026-06-30 ---
import time
import functools

def retry_with_backoff(max_retries=3, base_delay=1.0, exceptions=(Exception,)):
    """Decorator that retries a function on failure with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts.
        base_delay: Initial delay in seconds (doubles each retry).
        exceptions: Tuple of exception types that trigger a retry.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        raise  # Re-raise on final attempt
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
            return None
        return wrapper
    return decorator


# --- 2026-06-30 ---
def flatten_dict(d, parent_key='', sep='.'):
    """Flatten a nested dictionary into a single-level dict with dotted keys.

    Args:
        d: The (possibly nested) dictionary to flatten.
        parent_key: Prefix accumulated from parent levels (used in recursion).
        sep: Separator between key levels in the output.

    Example:
        >>> flatten_dict({'a': {'b': 1, 'c': {'d': 2}}, 'e': 3})
        {'a.b': 1, 'a.c.d': 2, 'e': 3}
    """
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k  # Build dotted path
        if isinstance(v, dict):
            items.update(flatten_dict(v, new_key, sep=sep))  # Recurse into nested dicts
        else:
            items[new_key] = v
    return items


# --- 2026-06-30 ---
def chunk_list(lst, size):
    """Split a list into fixed-size chunks (last chunk may be smaller).

    Args:
        lst: The list to split.
        size: Maximum number of elements per chunk.

    Yields:
        Successive sublists of length *size*.

    Example:
        >>> list(chunk_list(range(10), 3))
        [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    """
    if size <= 0:
        raise ValueError("Chunk size must be a positive integer")
    for i in range(0, len(lst), size):
        yield lst[i : i + size]  # Slice out the next chunk

