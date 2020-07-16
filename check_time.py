import json
import requests
import datetime
from dateutil import tz
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--number-of-persons', dest="number_of_persons", help="How many people to come for the visit")
    parser.add_argument('--city', dest='city', help="Helsinki, Lahti or Turku")
    args = parser.parse_args()
    if args.number_of_persons is None or args.city is None:
        parser.print_help()
        exit()
    headers = {
        'authority': 'migri.vihta.com',
        'accept': 'application/json, text/plain, */*',
        'vihta-session': '0a7c1a71-9796-437b-b9f0-364c51148801',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://migri.vihta.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://migri.vihta.com/public/migri/',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8,uk;q=0.7'
    }

    params = (
        ('end_hours', '24'),
        ('start_hours', '0'),
    )
    city = ""
    number_of_persons = 0

    HELSINKI = '25ee3bce-aec9-41a7-b920-74dc09112dd4'
    TURKU = '074cc6f8-735b-4ea5-ad9a-9e517fef09bb'
    LAHTI = 'a893849c-c0d9-489b-92a3-6dd8a36ef9f9'

    if args.city.lower() == "helsinki":
        city = HELSINKI
    elif args.city.lower() == "turku":
        city = TURKU
    elif args.city.lower() == "lahti":
        city = LAHTI

    PERMANENT_RESIDENCE = '3e03034d-a44b-4771-b1e5-2c4a6f581b7d'

    number_of_persons = int(args.number_of_persons)
    data = {"serviceSelections": [], "extraServices": []}

    while int(number_of_persons) > 0:
        data["serviceSelections"].append({"firstName":"Uno","lastName":"Duoes","values":[PERMANENT_RESIDENCE]})
        number_of_persons -= 1

    year, week, day = datetime.date.today().isocalendar()

    for i in range(week, week+14):
        url = f'https://migri.vihta.com/public/migri/api/scheduling/offices/{HELSINKI}/{year}/w{i}'
        response = requests.post(url, headers=headers, params=params, data=str(data).replace("'", '"'))
        jresp = response.json()
        print(f"Week {i}: ")
        for day in jresp["dailyTimesByOffice"]:
            if len(day) > 0:
                for t in day:
                    _time = datetime.datetime.strptime(t["startTimestamp"], "%Y-%m-%dT%H:%M:%S.000Z") + datetime.timedelta(hours=3)
                    print("\tYou can register at: " + _time.isoformat())
