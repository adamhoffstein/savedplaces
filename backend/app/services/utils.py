def flatten(l: list):
    return [item for sublist in l for item in sublist]


def sort_by_key(l: list, k: str, reverse: bool = True):
    return sorted(l, key=lambda d: d[k], reverse=reverse)
