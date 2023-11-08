"""tests for consumer"""

from unittest import mock
from ..consumer import on_message


def test_on_message():
    """on message test"""
    # Create mock objects for the required parameters
    channel = mock.Mock()
    method_frame = mock.Mock()
    header_frame = mock.Mock()
    body = b"Test message"

    # Call the function under test
    on_message(channel, method_frame, header_frame, body)

    # Assert that the channel.basic_ack method was called with the correct arguments
    channel.basic_ack.assert_called_with(delivery_tag=method_frame.delivery_tag)


# You can add more test cases as needed
