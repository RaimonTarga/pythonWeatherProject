import datetime as dt
import requests
import matplotlib.pyplot as plt
import os
from pylatex import (
    Command,
    Document,
    Figure,
    Section,
    Subsection
)
from pylatex.utils import NoEscape

WEATHER_BASE_URL = "https://api.openweathermap.org/data/3.0/onecall?"

CITY = "Barcelona"
BCN_LONG = "2.159"
BCN_LAT = "41.3888"

file = open("key.txt", "r")
APIKey = file.read()

url = WEATHER_BASE_URL + "lat=" + BCN_LAT + "&lon=" + BCN_LONG +"&exclude=current,hourly,minutely,alerts&units=metric&appid=" + APIKey

response = requests.get(url).json()

#response['main']['temp']

fig, ax = plt.subplots(figsize=(15,10))

ax.set_xlabel("Days", fontsize=12)
ax.set_ylabel("Temperature", fontsize=12)
ax.set_title("Daily temperature forecast")
temps_min = [0] * 7
temps_max = [0] * 7
dates = [""] * 7
for i in range(7):
    temps_min[i] = response['daily'][i]['temp']['min']
    temps_max[i] = response['daily'][i]['temp']['max']
    dates[i] = dt.datetime.fromtimestamp(response['daily'][i]["dt"]).strftime('%Y-%m-%d')

ax.plot(dates, temps_min, linestyle='--', marker='o', color='blue', label="Minimum temperature")
ax.plot(dates, temps_max, linestyle='--', marker='o', color='red', label="Maximum temperature")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid()
ax.legend()
fig.savefig('./weatherForecast.png', transparent=False, dpi=150)

if __name__ == "__main__":
    image_filename = os.path.join(os.path.dirname(__file__), "weatherForecast.png")

    # Basic document
    doc = Document("basic")

    # Document with `\maketitle` command activated
    doc = Document()

    doc.preamble.append(Command("title", "Weather Forecast"))
    doc.preamble.append(Command("author", "Raimon Targa"))
    doc.preamble.append(Command("date", NoEscape(r"\today")))
    doc.append(NoEscape(r"\maketitle"))

    with doc.create(Section("Main section")):
        doc.append("Weather forecast for the next seven days in " + CITY + ", latitude: " + BCN_LAT + ", longitude: " + BCN_LONG)
        doc.append(NoEscape('{'))
        doc.append(Command('centering'))
        with doc.create(Figure(position="h!")) as forecast_pic:
            forecast_pic.add_image(image_filename, width="450px")
        doc.append(Command('par'))
        doc.append(NoEscape('}'))

    doc.generate_pdf("weather forecast", clean_tex=False)
    tex = doc.dumps()  # The document as string in LaTeX syntax