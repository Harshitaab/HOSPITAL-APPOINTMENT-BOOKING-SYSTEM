import requests
import json
from appointments.models import Hospital

OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"

# Overpass Query to get hospitals in Tamil Nadu
QUERY = """
[out:json];
area[name="Tamil Nadu"]->.boundaryarea;
(
  node["amenity"="hospital"](area.boundaryarea);
  way["amenity"="hospital"](area.boundaryarea);
  relation["amenity"="hospital"](area.boundaryarea);
);
out center;
"""

def fetch_hospitals_from_osm():
    response = requests.get(OVERPASS_API_URL, params={"data": QUERY})
    data = response.json()

    for element in data["elements"]:
        name = element.get("tags", {}).get("name", "Unknown Hospital")
        location = element.get("tags", {}).get("addr:city", "Unknown City")
        specialty = element.get("tags", {}).get("healthcare:speciality", "General")
        open_hours = element.get("tags", {}).get("opening_hours", "Not Available")

        Hospital.objects.create(
            name=name,
            location=location,
            speciality=specialty,
            open_hours=open_hours
        )

    print("✅ Tamil Nadu hospitals added successfully!")

# Run the function
fetch_hospitals_from_osm()

