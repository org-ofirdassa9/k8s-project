"""producer.py"""

import logging
import sys
import argparse
import os
from argparse import RawTextHelpFormatter
from time import sleep
import pika

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


def main():
    """main function"""
    examples = sys.argv[0] + " -p 5672 -s rabbitmq -m 'Hello' "
    parser = argparse.ArgumentParser(
        formatter_class=RawTextHelpFormatter,
        description="Run producer.py",
        epilog=examples,
    )
    parser.add_argument(
        "-p",
        "--port",
        action="store",
        dest="port",
        help="The port to listen on.",
        required=True,
    )
    parser.add_argument(
        "-s",
        "--server",
        action="store",
        dest="server",
        help="The RabbitMQ server.",
        required=True,
    )
    parser.add_argument(
        "-m",
        "--message",
        action="store",
        dest="message",
        help="The message to send",
        required=False,
        default="Hello",
    )
    parser.add_argument(
        "-r",
        "--repeat",
        action="store",
        dest="repeat",
        help="Number of times to repeat the message",
        required=False,
        default="30",
    )

    args = parser.parse_args()

    # Handle missing required arguments
    if args.port is None or args.server is None:
        print("Missing required arguments: -p/--port and -s/--server are required.")
        parser.print_help()
        sys.exit(1)

    # Convert port to integer
    # Handle invalid port argument
    try:
        args.port = int(args.port)
    except ValueError:
        print("Invalid port value. Port must be an integer.")
        sys.exit(1)

    # sleep a few seconds to allow RabbitMQ server to come up
    sleep(5)

    credentials = pika.PlainCredentials(
        os.environ.get("RABBITMQ_USERNAME", "user"),
        os.environ.get("RABBITMQ_PASSWORD", "user"),
    )
    parameters = pika.ConnectionParameters(args.server, args.port, "/", credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    q = channel.queue_declare("pc")
    q_name = q.method.queue

    # Turn on delivery confirmations
    channel.confirm_delivery()
    LOG.info("going to run %s times", int(args.repeat))
    for i in range(0, int(args.repeat)):
        LOG.debug("%s iteration", i)
        channel.basic_publish(exchange="", routing_key=q_name, body=args.message)
        sleep(2)

    connection.close()


if __name__ == "__main__":
    main()
