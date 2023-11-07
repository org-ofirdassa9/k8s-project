"""consumer.py"""

import logging
import sys
import argparse
import os
from argparse import RawTextHelpFormatter
from time import sleep
import pika

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


def on_message(channel, method_frame, header_frame, body):
    """on_message event"""
    LOG.info("Message has been received %s", body)
    LOG.debug("header_frame is %s", header_frame)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


if __name__ == "__main__":
    examples = sys.argv[0] + " -p 5672 -s rabbitmq "
    parser = argparse.ArgumentParser(
        formatter_class=RawTextHelpFormatter,
        description="Run consumer.py",
        epilog=examples,
    )
    parser.add_argument(
        "-p", "--port", action="store", dest="port", help="The port to listen on."
    )
    parser.add_argument(
        "-s", "--server", action="store", dest="server", help="The RabbitMQ server."
    )

    args = parser.parse_args()
    if args.port is None:
        print("Missing required argument: -p/--port")
        sys.exit(1)
    if args.server is None:
        print("Missing required argument: -s/--server")
        sys.exit(1)

    # sleep a few seconds to allow RabbitMQ server to come up
    sleep(5)
    credentials = pika.PlainCredentials(
        os.environ.get("RABBITMQ_USER", "user"),
        os.environ.get("RABBITMQ_PASSWORD", "user"),
    )
    parameters = pika.ConnectionParameters(
        args.server, int(args.port), "/", credentials
    )
    connection = pika.BlockingConnection(parameters)
    rabbitmq_channel = connection.channel()

    rabbitmq_channel.queue_declare("pc")
    rabbitmq_channel.basic_consume(queue="pc", on_message_callback=on_message)

    try:
        rabbitmq_channel.start_consuming()
    except KeyboardInterrupt:
        rabbitmq_channel.stop_consuming()
    connection.close()
