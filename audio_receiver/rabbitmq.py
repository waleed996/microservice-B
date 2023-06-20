import os

import rabbitpy


class QueueHelper:
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
    rabbitmq_port = os.getenv('RABBITMQ_PORT', 5672)

    @staticmethod
    def send_to_speech_ack_queue(data: str, queue_name='contains-speech-ack') -> None:
        """
        Send data to contains-speech-ack queue

        :param data: string data that needs to be sent to the queue
        :param queue_name: name of the queue to send data to
        """

        with rabbitpy.Connection(f'amqp://{QueueHelper.rabbitmq_host}:{QueueHelper.rabbitmq_port}/') as conn:
            with conn.channel() as channel:
                rabbitpy.Queue(channel, queue_name)
                message = rabbitpy.Message(channel, data)

                # Send to queue
                message.publish('', queue_name)

