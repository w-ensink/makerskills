import unittest


class Protocol:
    def encode_text(self, text):
        binary = text.encode('utf-8')
        header = b'txt_'
        message = header + binary
        return message

    def decode_text(self, binary):
        return str(binary)[4:]

    def is_encoded_text(self, binary):
        return binary[:4] == b'txt_'

    def encode_int(self, num):
        binary = b'num_' + str(num).encode('utf-8')
        return len(binary), binary

    def get_header_size(self):
        return 64

    def encode_message_length_header(self, length):
        length = str(length).encode('utf-8')
        length += b' ' * (self.get_header_size() - len(length))
        return length


class ProtocolTest(unittest.TestCase):
    def setUp(self) -> None:
        self.p = Protocol()

    def tearDown(self) -> None:
        pass

    def test_encode_text(self):
        expected = b'txt_hello world'
        expected_size = 15
        size, binary = self.p.encode_text('hello world')
        self.assertEqual(expected, binary)
        self.assertEqual(expected_size, size)

    def test_decode_text(self):
        expected = 'thisisatest'
        result = self.p.decode_text('txt_thisisatest')
        self.assertEqual(result, expected)

    def test_is_encoded_text(self):
        self.assertTrue(self.p.is_encoded_text(b'txt_test'))
        self.assertFalse(self.p.is_encoded_text(b'img_0010100110'))

    def test_encode_number(self):
        expected = b'num_' + str(42).encode()
        expected_size = 6
        size, result = self.p.encode_int(42)
        self.assertEqual(expected, result)
        self.assertEqual(size, expected_size)

    def test_decode_number(self):
        pass


if __name__ == '__main__':
    unittest.main()
