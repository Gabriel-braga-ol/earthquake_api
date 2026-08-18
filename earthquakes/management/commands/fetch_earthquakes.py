from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta, timezone
from earthquakes.models import Earthquake
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

            for feature in data["features"]:
                magnitude = feature["properties"]["mag"]
                place = feature["properties"]["place"]
                timestamp_ms = feature["properties"]["time"]
                sig = feature["properties"]["sig"]
                external_id = feature["id"]
                longitude = feature["geometry"]["coordinates"][0]
                latitude = feature["geometry"]["coordinates"][1]
                depth = feature["geometry"]["coordinates"][2]  
    
                event_time = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
    
                Earthquake.objects.update_or_create (
                    external_id = external_id,
                    defaults= {
                        "magnitude": magnitude,
                        "place": place,
                        "latitude": latitude,
                        "longitude": longitude,
                        "depth": depth,
                        "time": event_time,
                        "sig": sig,
                    }
                )
        else:
            raise CommandError(f"Erro ao buscar dados: {response.status_code}")           




