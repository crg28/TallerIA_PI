from django.core.management.base import BaseCommand
from movie.models import Movie
import json

class Command(BaseCommand):
    help = 'Modify path of images'

    def handle(self, *args, **kwargs):
        items = Movie.objects.all()
        for item in items:
            #print(item.image.name)
            #print(item.title)
            #item.image.name = f"{item.image.name}{item.title}.png"
            item.image.name = f"movie/images/m_{item.title}.png"
            print(item.image.name)
            item.save()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated with the illustrations of the movies'))