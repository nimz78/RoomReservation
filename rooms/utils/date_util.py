import random
from datetime import datetime
from itertools import chain


def parse_date(date):
    return datetime.strptime(
        (date), '%Y-%m-%d').date()


def is_overlapped(ranges):
    sorted_ranges = sorted(ranges, key=lambda begin_end: begin_end[0])
    return list(chain(*sorted_ranges)) != sorted(chain(*sorted_ranges))
