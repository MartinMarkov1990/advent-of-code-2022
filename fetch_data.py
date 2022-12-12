import os

import requests


USER_SESSION = '53616c7465645f5f5168073fd2bf8ec1c7d3a858007ddd92d2ef768a53c5a8' + \
    '527892df2189e7a812917efe690a2c3784592f567cd5551a508b01e95931fbce55'
INPUT_URL_FORMAT = 'https://adventofcode.com/2022/day/{day}/input'
DIRECTORY_FORMAT = 'day_{day}'


def fetch_daily_data(day=1) -> requests.Response:
    URL = INPUT_URL_FORMAT.format(day=day)
    return requests.request('GET', URL, cookies={'session': USER_SESSION})


def save_daily_input(day=1):
    dir = DIRECTORY_FORMAT.format(day=day)
    if not os.path.exists(dir):
        os.makedirs(dir)
    request = fetch_daily_data(day=day)
    if request.ok:
        data = request.text
        filename = os.path.join(dir, 'input.txt')
        with open(filename, 'w+') as f:
            f.write(data)
    else:
        raise ValueError('Invalid response from server.')


def fetch_multiple_inputs(min_day=1, max_day=26):
    for day in range(min_day, max_day + 1):
        save_daily_input(day)


if __name__ == '__main__':
    fetch_multiple_inputs(1, 31)
