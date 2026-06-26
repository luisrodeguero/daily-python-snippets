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

