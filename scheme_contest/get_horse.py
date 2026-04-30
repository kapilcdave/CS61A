import urllib.request
import re
import xml.etree.ElementTree as ET

url = "https://upload.wikimedia.org/wikipedia/commons/1/14/Animal_silhouette_19.svg"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        svg_data = response.read().decode('utf-8')
    print(svg_data[:500])
except Exception as e:
    print("Error:", e)
