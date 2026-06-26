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

