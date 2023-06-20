import json
import os
import threading
import random
import time

import rabbitpy

from audio_receiver.rabbitmq import QueueHelper


class AudioSpeechDetectorThread(threading.Thread):
    """
    Thread to read messages from 'audio-parts' queue and detect speech. Thread will read 500 parts combine them and then
    process to check for speech.
    """

    def run(self) -> None:
        rabbitmq_host = os.getenv('RABBITMQ_HOST', '127.0.0.1')
        rabbitmq_port = os.getenv('RABBITMQ_PORT', 5672)

        connection = None
        while connection is None:
            try:
                connection = rabbitpy.Connection(f'amqp://{rabbitmq_host}:{rabbitmq_port}/')
            except RuntimeError as err:
                # simplified error handling in case connection fails
                if "Timeout waiting for opening the socket" in str(err):
                    print('Connection to RabbitMQ failed. Retrying in 5 seconds ...')
                    time.sleep(5)
                else:
                    # other runtime errors can be handled here
                    print("Unhandled runtime error")
                    raise err
            except Exception as err:
                print(f'RabbitMQ connection error: {str(err)}')
                raise err

        with connection:
            with connection.channel() as channel:
                queue = rabbitpy.Queue(channel, 'audio-parts')

                # Consume 500 messages from queue
                message_count = 0

                joined_audio_parts = bytearray()
                for message in queue.consume():
                    message_count += 1

                    # Join the bytes from queue message
                    joined_audio_parts += message.body

                    # When 500 messages are read and joined, check for speech in this part of the audio
                    if message_count == 500:

                        # Assume i'm calling a google api or a 3rd party service to check for speech or doing an
                        # algorithm here to detect speech

                        # For now i'm just simulating if speech exists or not by generating a random number
                        # and modding it by 2
                        random_number = random.randint(1, 100) % 2
                        message = {'contains_speech': bool(random_number)}
                        QueueHelper.send_to_speech_ack_queue(data=json.dumps(message))
                        message_count = 0

