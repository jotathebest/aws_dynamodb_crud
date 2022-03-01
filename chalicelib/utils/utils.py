from typing import Optional


def get_int(value: any) -> Optional[int]:
    try:
        return int(value)
    except ValueError:
        return None
