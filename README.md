
## Project summary

This interactive dashboard collects information about different types of schools in Berlin, number of students across districts and school types and school activities. Schools can be searched via district and type of school and locations are shown on a map. 
The underlying data is publicly available and was explored and analyzed using pandas. Data is mostly from 2019, except for school activities (2016). Coordinates of schools were added using geopy (code adapted from [https://gist.github.com/shakasom](https://gist.github.com/shakasom)). All figures were generated with Plotly, Dash was used to build the web application.

## Tech stack

* Python | Pandas, Geopy, Plotly, Dash
* CSS

## Data sources

* [Senatsverwaltung für Bildung, Jugend und Familie](https://www.berlin.de/sen/bildung/schule/berliner-schulen/schulverzeichnis/ "Schulverzeichnis") 
* [Open Data Berlin](https://daten.berlin.de/kategorie/bildung "Datensätze Bildung")
* [jedeschule.de](https://jedeschule.de/daten/)
* [Berlin boroughs geodata](https://github.com/m-hoerz/berlin-shapes)

## Possible improvements

* Expand dashboard by adding data about school partners, lunch opportunities, languages offered, staff info, etc.
* Add more filter options for school search (e.g. what activities are offered, full-time school (yes/no), etc.)
* Analyze data on neighborhood level 
* Improve maps with mapbox
