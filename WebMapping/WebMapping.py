import pandas as pd
import folium

nfl = pd.read_csv("NFL_teams.csv")
lat = list(nfl["latitude"])
long = list(nfl["longitude"])
team = list(nfl["Team"])
conf = list(nfl["Conference"])


def color_producer(conference):
    if conference == "AFC":
        return "red"
    else:
        return "blue"


def num_champs(data):
    champs = data["properties"]["Championships"]
    if champs > 0:
        return {"colorFill": "red"}    
    else:
        return {"colorFill": "green"}


file = open("gz_2010_us_040_00_500k.json", "r", encoding="utf-8-sig")
content = file.read()
my_map = folium.Map(location=[41.54485, -99.36384], zoom_start=5, tiles="Stamen Terrain")

fgt = folium.FeatureGroup(name="Teams")

for lt, ln, team_name, confer in zip(lat, long, team, conf):
    fgt.add_child(folium.Marker(location=[lt, ln], popup=team_name, icon=folium.Icon(color=color_producer(confer))))

fgc = folium.FeatureGroup(name="Championships")

fgc.add_child(folium.GeoJson(data=content, style_function=lambda x: {"fillColor": "red"} if
                             x["properties"]["Championships"] >= 5 else ({"fillColor": "orange"} if
                             x["properties"]["Championships"] >= 1 else {"fillColor": "green"})))

my_map.add_child(fgt)
my_map.add_child(fgc)
my_map.add_child(folium.LayerControl())

my_map.save("Map1.html")