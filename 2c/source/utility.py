
import unittest


def limit_words_per_line(string: str, max_words_per_line: int):
    result = ''
    for i, w in enumerate(string.split(' ')):
        result += '\n' if i % max_words_per_line == 0 else ' '
        result += w
    return result.strip()


class TestLimitedWordsPerLine(unittest.TestCase):
    def test_limit_long_string(self):
        self.assertEqual(limit_words_per_line('welkom to who am ai', 3),
                         'welkom to who\nam ai')


if __name__ == '__main__':
    unittest.main()