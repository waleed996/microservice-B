# microservice-B (Audio Receiver)
Receive audio file from microservice-A in parts and combine it.

    Explanation: I have implemented a simplified version of the requirements because of time constraints. The idea I have
    implemented is that, in this microservice-B AudioSpeechDetectorThread consumes 500 messages from the rabbitmq
    queue called 'audio-parts'. When 500 parts are recieved 'pydub' library is used to combine the parts into an
    audio .wav file. This file was supposed to be processed for speech but I am not able to do that part. Instead to
    just simulate that the speech exists or not in the combined parts, I have just generated a random number and mod it
    by 2 to get a bool 0 or 1 and sent this value in 'contains-speech-ack' queue to the microservice-A.

Note: Because of limited time my priority was to create a working project, so there are improvements that can be done
related to project structure, scalability,env variables, encapsulation, method/variable names, logging and documentation etc.

# How to Run
You can conveniently run this service by cloning it in the same directory as microservice-A and using the
docker-compose file in microservice-A repository.
