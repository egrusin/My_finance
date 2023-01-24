from datetime import datetime, date, timedelta


__all__ = ['get_today', 'get_diff']


def get_today() -> str:  # Strong!
    """Returns now date in format dd.mm.yyyy"""
    date_now = datetime.now()
    return f'{date_now.day:>02}.{date_now.month:>02}.{date_now.year}'


def get_diff(start_date: str, stop_date: str) -> list:  # Nice!
    """Returns difference between start (last report) date and stop (today) date
    don't include start date, include stop date"""

    step = timedelta(days=1)
    sp_d, sp_m, sp_y = map(int, stop_date.split('.'))
    st_d, st_m, st_y = map(int, start_date.split('.'))
    stop_datetime = date(sp_y, sp_m, sp_d)
    start_datetime = date(st_y, st_m, st_d)
    diff = (stop_datetime - start_datetime).days

    result = []
    for i in range(diff):
        start_datetime += step
        result.append(f'{start_datetime.day:>02}.{start_datetime.month:>02}.{start_datetime.year}')
    return result
