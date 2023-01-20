from datetime import datetime, date, timedelta


__all__ = ['get_today']


def get_today() -> str:
    """Returns now date in format dd.mm.yyyy"""
    date_now = datetime.now()
    return f'{date_now.day:>02}.{date_now.month:>02}.{date_now.year}'


def get_diff(start_date: str, last_date: str) -> list:
    """Returns difference between start date and last date
    don't include start date, include last date"""

    step = timedelta(days=1)
    s_day, s_mounth, s_year = map(int, start_date.split('.'))
    l_day, l_mounth, l_year = map(int, last_date.split('.'))
    s_date = date(s_year, s_mounth, s_day)
    l_date = date(l_year, l_mounth, l_day)
    diff = (l_date - s_date).days

    result = []
    for i in range(diff):
        s_date += step
        result.append(f'{s_date.day:>02}.{s_date.month:>02}.{s_date.year}')
    return result


print(get_diff('20.01.2023', '02.02.2023'))
