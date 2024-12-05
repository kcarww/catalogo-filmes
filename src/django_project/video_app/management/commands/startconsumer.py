from django.core.management.base import BaseCommand

from core.video.infra.video_converter_rabbitmq_consumer import VideoConvertedRabbitMQConsumer

class Command(BaseCommand):
    help = 'Starts the VideoConverted Consumer'

    def handle(self, *args, **options):
        consumer = VideoConvertedRabbitMQConsumer()
        consumer.start()