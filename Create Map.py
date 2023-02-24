import folium
import json
from folium.plugins import Geocoder
import requests

m = folium.Map(tiles='https://a.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}@2x.png', attr='CartoDB, Voyager', zoom_control=False, zoom_start=7.4,
               location=[56.05,10.84])

with open("10x10/10x10.geojson") as f:
    grid10x10 = json.load(f)
with open("20x20/20x20.geojson") as f:
    grid20x20 = json.load(f)
with open("Municipalities/Municipalities.geojson") as f:
    kommuner = json.load(f)

url_climate = 'https://dmigw.govcloud.dk/v2/climateData/collections/station/items?api-key=3d060a77-29be-41ef-8b31-2c74dce37dbe&'
url_ocean = 'https://dmigw.govcloud.dk/v2/oceanObs/collections/station/items?api-key=06adbad0-8067-4117-8008-2725cf51cc97&'

r = requests.get(url_climate)
json_stat = r.json()

r = requests.get(url_ocean)
json_ocean = r.json()

style_function_20 = {'fillOpacity': '0.1', 'color': '#0066ff', 'weight': '1.5'}
style_function_10 = {'fillOpacity': '0.1', 'color': '#248f8f', 'weight': '1'}
style_function_kom = {'fillOpacity': '0.1', 'color': '#f73f3f', 'weight': '1'}

g20 = folium.GeoJson(grid20x20, name='20x20km', style_function=lambda x:style_function_20)
g20.add_child(folium.features.GeoJsonPopup(fields=['cellId']))
g10 = folium.GeoJson(grid10x10, name='10x10km', style_function=lambda x:style_function_10)
g10.add_child(folium.features.GeoJsonPopup(fields=['cellId']))
kom_feat = folium.GeoJson(kommuner, name='Kommuner', style_function=lambda x:style_function_kom)
kom_feat.add_child(folium.features.GeoJsonPopup(fields=('Name', 'MunicipalityID')))

all_stat = folium.FeatureGroup(name='Climate stations')
temp = folium.FeatureGroup(name='Temperature')
humi = folium.FeatureGroup(name='Humidity')
pressure = folium.FeatureGroup(name='Pressure')
wind = folium.FeatureGroup(name='Wind')
sun = folium.FeatureGroup(name='Sun')
radi = folium.FeatureGroup(name='Radiation')
precip = folium.FeatureGroup(name='Precipitation')
snow = folium.FeatureGroup(name='Snow')
cloud = folium.FeatureGroup(name='Cloud')
all_oce_stat = folium.FeatureGroup(name='Oceanographic Stations')


for feature in json_ocean['features']:
    folium.CircleMarker(location=list(reversed(feature['geometry']['coordinates'])),
                        fill_color='Aquamarine',
                        color='black',
                        weight=1,
                        fill=True,
                        fill_opacity=1,
                        radius=5,
                        border_color='turquoise',
                        popup=feature['properties']['parameterId']
                        ).add_to(all_oce_stat)

for feature in json_stat['features']:
    html = """ 
<html>
  <head>
    <style>
      
      table {{
        font-family: "Roboto", "Helvetica", "Arial", sans-serif;
        height: 81.5%;
        width: 100%;
        
      }}
       
      p {{
        font-family: "Roboto", "Helvetica", "Arial", sans-serif;
        font-size: 1.5em;
        padding: 0;
        font-weight: bold;
       }}
      tr {{
        background-color: #D6EEEE;
        
      }}
      
      tr:hover {{
        background-color: #81caca;
      }}
      
      td {{
        width: 150px;
        padding: 5px;
      }}
       
    </style>
  </head>
  <table>
    <tbody>
      <p>{} {}</p>""".format(feature['properties']['name'], feature['properties']['stationId']) + """
      <tr>
        <td>Operation from</td>
        <td>{}</td>""".format(feature['properties']['operationFrom']) + """
      </tr>
      <tr>
        <td>Operation to</td>
        <td>{}</td>""".format(feature['properties']['operationTo']) + """
      </tr>
      <tr>
        <td>Parameters measured</td>
        <td>{}</td>""".format(feature['properties']['parameterId']) + """
      </tr>
    </tbody>
  </table>
</html>
"""
    iframe = folium.IFrame(html=html, width=400, height=300)
    popup = folium.Popup(iframe)

    folium.CircleMarker(location=list(reversed(feature['geometry']['coordinates'])),
                        fill_color='DarkCyan',
                        color='black',
                        weight=1,
                        fill=True,
                        fill_opacity=1,
                        radius=5,
                        border_color='DarkCyan',
                        popup=popup
                        ).add_to(all_stat)

    if 'mean_temp' in feature['properties']['parameterId']:
        icon_color = 'Green'
        folium.CircleMarker(location=list(reversed(feature['geometry']['coordinates'])),
                            fill_color=icon_color,
                            color='black',
                            weight=1,
                            fill=True,
                            fill_opacity=1,
                            radius=5,
                            border_color=icon_color,
                            popup=feature['properties']['parameterId']
                            ).add_to(temp)
    if 'mean_relative_hum' in feature['properties']['parameterId']:
        icon_color = 'Red'
        folium.CircleMarker(location=list(reversed(feature['geometry']['coordinates'])),
                            fill_color=icon_color,
                            color='black',
                            weight=1,
                            fill=True,
                            fill_opacity=1,
                            radius=5,
                            border_color=icon_color,
                            popup=feature['properties']['parameterId']
                            ).add_to(humi)
    if 'mean_pressure' in feature['properties']['parameterId']:
        icon_color = 'Purple'
        folium.CircleMarker(location=list(reversed(feature['geometry']['coordinates'])),
                            fill_color=icon_color,
                            color='black',
                            weight=1,
                            fill=True,
                            fill_opacity=1,
                            radius=5,
                            border_color=icon_color,
                            popup=feature['properties']['parameterId']
                            ).add_to(pressure)
    if 'mean_wind_speed' in feature['properties']['parameterId']:
        icon_color = 'Black'
        folium.CircleMarker(location=list(reversed(feature['geometry']['coordinates'])),
                            fill_color=icon_color,
                            color='black',
                            weight=1,
                            fill=True,
                            fill_opacity=1,
                            radius=5,
                            border_color=icon_color,
                            popup=feature['properties']['parameterId']
                            ).add_to(wind)
    if 'bright_sunshine' in feature['properties']['parameterId']:
        icon_color = 'Yellow'
        folium.CircleMarker(location=list(reversed(feature['geometry']['coordinates'])),
                            fill_color=icon_color,
                            color='black',
                            weight=1,
                            fill=True,
                            fill_opacity=1,
                            radius=5,
                            border_color=icon_color,
                            popup=feature['properties']['parameterId']
                            ).add_to(sun)
    if 'mean_radiation' in feature['properties']['parameterId']:
        icon_color = 'Grey'
        folium.CircleMarker(location=list(reversed(feature['geometry']['coordinates'])),
                            fill_color=icon_color,
                            color='black',
                            weight=1,
                            fill=True,
                            fill_opacity=1,
                            radius=5,
                            border_color=icon_color,
                            popup=feature['properties']['parameterId']
                            ).add_to(radi)
    if 'acc_precip' in feature['properties']['parameterId']:
        icon_color = 'Blue'
        folium.CircleMarker(location=list(reversed(feature['geometry']['coordinates'])),
                            fill_color=icon_color,
                            color='black',
                            weight=1,
                            fill=True,
                            fill_opacity=1,
                            radius=5,
                            border_color=icon_color,
                            popup=feature['properties']['parameterId']
                            ).add_to(precip)

    if 'snow_depth' in feature['properties']['parameterId']:
        icon_color = 'BlueViolet'
        folium.CircleMarker(location=list(reversed(feature['geometry']['coordinates'])),
                            fill_color=icon_color,
                            color='black',
                            weight=1,
                            fill=True,
                            fill_opacity=1,
                            radius=5,
                            border_color=icon_color,
                            popup=(feature['properties']['parameterId'],feature['properties']['stationId'],feature['properties']['operationFrom'])
                            ).add_to(snow)
    if 'mean_cloud_cover' in feature['properties']['parameterId']:
        icon_color = 'Orange'
        folium.CircleMarker(location=list(reversed(feature['geometry']['coordinates'])),
                            fill_color=icon_color,
                            color='black',
                            weight=1,
                            fill=True,
                            fill_opacity=1,
                            radius=5,
                            border_color=icon_color,
                            popup=feature['properties']['parameterId']
                            ).add_to(cloud)

all_stat.add_to(m)
all_oce_stat.add_to(m).show=False
temp.add_to(m).show=False
humi.add_to(m).show=False
pressure.add_to(m).show=False
wind.add_to(m).show=False
sun.add_to(m).show=False
radi.add_to(m).show=False
precip.add_to(m).show=False
snow.add_to(m).show=False
cloud.add_to(m).show=False
g20.add_to(m).show=False
g10.add_to(m).show=False
kom_feat.add_to(m).show=False
Geocoder(add_marker=True).add_to(m)

lay = folium.LayerControl(collapsed=False)
lay.add_to(m)

m.save('index.html')