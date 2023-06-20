from django.apps import AppConfig

from audio_receiver.threads import AudioSpeechDetectorThread


class AudioReceiverConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "audio_receiver"

    def ready(self):
        AudioSpeechDetectorThread().start()
