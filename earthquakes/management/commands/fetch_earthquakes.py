from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
import requests 

class Command(BaseCommand):
    def handle(self, *args, **options):
        endtime = datetime.now()
        starttime = datetime.now() - timedelta(days = 30)

        url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

        response = requests.get(url, params={
            "format": "geojson",
            "starttime": starttime.isoformat(),
            "endtime": endtime.isoformat(),
            "minmagnitude": 4.5
        })

        if response.status_code == 200:
            data = response.json()
            self.stdout.write(f"Terremotos encontrados: {len(data['features'])}")
        else:
            raise CommandError(f"Erro ao buscar dados: {response.status_code}")




