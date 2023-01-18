import datetime


__all__ = ['get_today']


def get_today() -> str:
    """Returns now date in format dd.mm.yyyy"""
    date = datetime.datetime.now()
    return f'{date.day}.{date.month:>02}.{date.year}'


def get_diff(date: str) -> list:
    """Returns difference between now date and last date"""
    ...
