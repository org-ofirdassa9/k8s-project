"""producer tests"""

import unittest
from unittest.mock import patch
from ..producer import main

# pylint: disable=too-few-public-methods
# Create a mock RabbitMQ server for testing
class MockRabbitMQServer:
    """mock rabbitmq server"""

    def __init__(self):
        # Set up mock connection parameters
        self.hostname = "mock_server"
        self.port = 5672
        self.username = "mock_user"
        self.password = "mock_password"


class TestProducer(unittest.TestCase):
    """producer tests class"""

    def setUp(self):
        """set up mock rabbit mq"""
        self.mock_rabbitmq_server = MockRabbitMQServer()

    def test_main_success(self):
        """success test case"""
        port, server, message, repeat, expected_output = (
            5672,
            "mock_server",
            "Hello",
            30,
            None,
        )
        args = ["-p", str(port), "-s", server, "-m", message, "-r", str(repeat)]
        print(f"expected_output is: {expected_output}")

        # Mock the pika.BlockingConnection class to avoid actual connection attempts
        with patch("pika.BlockingConnection"):
            with patch("sys.argv", ["producer.py"] + args):
                main()

    def test_main_missing_required_args_invalid_value(self):
        """missing required args test case with an invalid value"""
        port, server, message, repeat = ("invalid", "mock_server", "Hello", 30)
        args = ["-p", str(port), "-s", server, "-m", message, "-r", str(repeat)]

        # Mock the pika.BlockingConnection class to avoid actual connection attempts
        with patch("pika.BlockingConnection"):
            with patch("sys.argv", ["producer.py"] + args):
                with self.assertRaises(SystemExit) as excinfo:
                    main()
                self.assertEqual(excinfo.exception.code, 1)

    def test_main_missing_required_args_none_value(self):
        """missing required args test case with a None value"""
        port, server, message, repeat = (5672, None, "Hello", 30)
        args = ["-p", str(port), "-s", server, "-m", message, "-r", str(repeat)]

        # Mock the pika.BlockingConnection class to avoid actual connection attempts
        with patch("pika.BlockingConnection"):
            with patch("sys.argv", ["producer.py"] + args):
                with self.assertRaises(SystemExit) as excinfo:
                    main()
                self.assertEqual(excinfo.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
