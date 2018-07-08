

RUN:

run script directly:
python scrape_air_polution.py

cron command:
* * * * * root python /scripts/scrape_air_polution.py >> /var/log/cron.log 2>&1



APIs:

https://newsapi.org/
API key: de29f14c20ad4e0f8e0ed0738afb54af

https://openweathermap.org/
API key: 01a36ac04b1772f77c02af558e929933

Krakow: 3094802
Poznan: 3088171
Warszawa: 6695624
NYC: 5128638