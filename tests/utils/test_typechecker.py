from unittest import TestCase

from src.utils.typechecker import parse_time


class TestParseTime(TestCase):
    hours   = 2
    minutes = 10
    seconds = 30

    def test_seconds(self):
        delta = parse_time(f'{self.seconds}')
        self.assertEqual(delta.total_seconds(), self.seconds)


    def test_minutes(self):
        delta = parse_time(f'{self.minutes}:{self.seconds}')
        total_seconds = self.seconds + self.minutes * 60
        self.assertEqual(delta.total_seconds(), total_seconds)


    def test_hours(self):
        delta = parse_time(f'{self.hours}:{self.minutes}:{self.seconds}')
        total_seconds = self.seconds + self.minutes * 60 + self.hours * 60 ** 2
        self.assertEqual(delta.total_seconds(), total_seconds)

    def test_error(self):
        with self.assertRaises(ValueError):
            parse_time(f'{self.hours}-{self.minutes}-{self.seconds}')
