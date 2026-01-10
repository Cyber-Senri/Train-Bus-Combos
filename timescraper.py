#timescraper.py
import requests
import json
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta



def fetch_or_cache(url, cache_key):
    """
    Tries live fetch; if it fails, load from cached_data.json.
    cache_key is the key where the response is stored in the cache.
    """
    try:
        resp = requests.post(url, timeout=5)
        resp.raise_for_status()
        print(f"LIVE: {cache_key}")
        data = resp.json()

        # Update cache file with latest data
        try:
            with open("cached_data.json", "r", encoding="utf-8") as f:
                cache = json.load(f)
        except:
            cache = {}

        cache[cache_key] = data
        with open("cached_data.json", "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)

        return data

    except Exception as e:
        print(f"Using CACHE for {cache_key}")
        with open("cached_data.json", "r", encoding="utf-8") as f:
            cache = json.load(f)
        return cache[cache_key]


def get_train_times(place, day):
    """
    Destination area:
    place = 'Koropi' | 'Doukissis'

    Current day:
    day = 'Mon' | 'Tue' | 'Wed' | 'Thu | 'Fri' | 'Sat' | 'Sun'
    """

    if place == 'Doukissis':
        response = requests.get('https://www.athenstransport.com/proastiakos/stathmos-koropi/')
        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.find('div', class_='entry-content clearfix')
    else:
        response = requests.get('https://www.athenstransport.com/proastiakos/stathmos-doukissis-plakentias/')
        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.find('div', class_='td-page-content tagdiv-type')


    results = []
    if content_div:
        for title in content_div.find_all("h3"):
            p = title.find_next(lambda tag: tag.name == "p")
            if p:
                times = re.findall(r'[0-9][0-9]:[0-9][0-9]', p.text.strip())
                results.append((title, times))

    else:
        print('Could not get div')
        exit()

    S_WKdays =[]
    S_WKend = []
    U_WKdays =[]
    U_WKend = []

    if place == 'Doukissis':
        for title, times in results:
            if bool(re.search(r'Κορωπί προς Ά|Κορωπί προς Π|Κορωπί προς Δ', title.text.strip(), flags=re.I)):
                if bool(re.search(r'Μετρό', title.text.strip(), flags=re.I)):
                    if not bool(re.search(r'Σάββατ', title.text.strip(), flags=re.I)):
                        U_WKdays.extend(times)
                    if not bool(re.search(r'Παρασκ', title.text.strip(), flags=re.I)):
                        U_WKend.extend(times)
                else:
                    if not bool(re.search(r'Σάββατ', title.text.strip(), flags=re.I)):
                        S_WKdays.extend(times)
                    if not bool(re.search(r'Παρασκ', title.text.strip(), flags=re.I)):
                        S_WKend.extend(times)
    else:
        for title, times in results:
            if bool(re.search(r'προς Αεροδρόμιο', title.text.strip(), flags=re.I)):
                if bool(re.search(r'Μετρό', title.text.strip(), flags=re.I)):
                    if not bool(re.search(r'Σάββατ', title.text.strip(), flags=re.I)):
                        U_WKdays.extend(times)
                    if not bool(re.search(r'Παρασκ', title.text.strip(), flags=re.I)):
                        U_WKend.extend(times)
                else:
                    if not bool(re.search(r'Σάββατ', title.text.strip(), flags=re.I)):
                        S_WKdays.extend(times)
                    if not bool(re.search(r'Παρασκ', title.text.strip(), flags=re.I)):
                        S_WKend.extend(times)

    S_WKdays =[datetime.strptime(t, "%H:%M" ) for t in S_WKdays]
    S_WKend = [datetime.strptime(t, "%H:%M" ) for t in S_WKend]
    U_WKdays = [datetime.strptime(t, "%H:%M" ) for t in U_WKdays]
    U_WKend = [datetime.strptime(t, "%H:%M" ) for t in U_WKend] 

    if (day == 'Sat') | (day == 'Sun'):
        return list(set(S_WKend)), list(set(U_WKend))
    else:
        return list(set(S_WKdays)), list(set(U_WKdays))


def get_bus_times(day):
    """
    Current day:
    day = 'Mon' | 'Tue' | 'Wed' | 'Thu | 'Fri' | 'Sat' | 'Sun'
    
    resp = requests.post('https://telematics.oasa.gr/api/?act=getSchedLines&p1=309%CE%92&p2=157&p3=1762').json()
    B_WKdays = [datetime.strptime(item["sde_start1"], "%Y-%m-%d %H:%M:%S").strftime("%H:%M") for item in resp["go"]]
    B_WKdays =[datetime.strptime(t, "%H:%M" ) for t in B_WKdays]

    resp = requests.post('https://telematics.oasa.gr/api/?act=getSchedLines&p1=309%CE%92&p2=158&p3=1762').json()
    B_Sat = [datetime.strptime(item["sde_start1"], "%Y-%m-%d %H:%M:%S").strftime("%H:%M") for item in resp["go"]]
    B_Sat =[datetime.strptime(t, "%H:%M" ) for t in B_Sat]

    resp = requests.post('https://telematics.oasa.gr/api/?act=getSchedLines&p1=309%CE%92&p2=159&p3=1762').json()
    B_Sun = [datetime.strptime(item["sde_start1"], "%Y-%m-%d %H:%M:%S").strftime("%H:%M") for item in resp["go"]]
    B_Sun =[datetime.strptime(t, "%H:%M" ) for t in B_Sun]
    """
    # WEEKDAYS
    resp = fetch_or_cache(
        'https://telematics.oasa.gr/api/?act=getSchedLines&p1=309%CE%92&p2=157&p3=1762',
        "309B_weekdays"
    )
    B_WKdays = [datetime.strptime(item["sde_start1"], "%Y-%m-%d %H:%M:%S").strftime("%H:%M") for item in resp["go"]]
    B_WKdays = [datetime.strptime(t, "%H:%M") for t in B_WKdays]


    # SATURDAY
    resp = fetch_or_cache(
        'https://telematics.oasa.gr/api/?act=getSchedLines&p1=309%CE%92&p2=158&p3=1762',
        "309B_saturday"
    )
    B_Sat = [datetime.strptime(item["sde_start1"], "%Y-%m-%d %H:%M:%S").strftime("%H:%M") for item in resp["go"]]
    B_Sat = [datetime.strptime(t, "%H:%M") for t in B_Sat]


    # SUNDAY
    resp = fetch_or_cache(
        'https://telematics.oasa.gr/api/?act=getSchedLines&p1=309%CE%92&p2=159&p3=1762',
        "309B_sunday"
    )
    B_Sun = [datetime.strptime(item["sde_start1"], "%Y-%m-%d %H:%M:%S").strftime("%H:%M") for item in resp["go"]]
    B_Sun = [datetime.strptime(t, "%H:%M") for t in B_Sun]

    if day == 'Sat':
        return B_Sat
    elif day == 'Sun':
        return B_Sun
    else:
        return B_WKdays


def best_times(place: str, day: str):
    """
    
    """
    
    S_times, U_times = get_train_times(place, day)
    S_times = [datetime.strftime(t, "%H:%M") for t in sorted(S_times)]
    U_times = [datetime.strftime(t, "%H:%M") for t in sorted(U_times)]

    B_times = get_bus_times(day)
    B_times = [datetime.strftime(t, "%H:%M") for t in sorted(B_times)]

    if place == 'Doukissis':
        offset = timedelta(minutes=75)
        offset_stop = timedelta(minutes=60)

        S_Compatible = []
        U_Compatible = []
        for B_time in B_times:
            for S_time in S_times:
                waiting = datetime.strptime(S_time, "%H:%M") - (datetime.strptime(B_time, "%H:%M") + offset)
                if (waiting.total_seconds()/60) <= 0:
                    continue
                
                if (waiting.total_seconds()/60) > 20:
                    continue

                B_time_stop = datetime.strptime(B_time, "%H:%M") + offset_stop
                B_time_stop = datetime.strftime(B_time_stop, "%H:%M")
                S_Compatible.append((B_time, int(waiting.total_seconds()/60), S_time, B_time_stop))

            for U_time in U_times:
                waiting = datetime.strptime(U_time, "%H:%M") - (datetime.strptime(B_time, "%H:%M") + offset)
                if (waiting.total_seconds()/60) <= 0:
                    continue
                
                if (waiting.total_seconds()/60) > 20:
                    continue

                B_time_stop = datetime.strptime(B_time, "%H:%M") + offset_stop
                B_time_stop = datetime.strftime(B_time_stop, "%H:%M")
                U_Compatible.append((B_time, int(waiting.total_seconds()/60), U_time, B_time_stop))

    else:
        S_offset = timedelta(minutes=14)
        U_offset = timedelta(minutes=16)

        S_Compatible = []
        U_Compatible = []
        for B_time in B_times:
            for S_time in S_times:
                waiting = datetime.strptime(B_time, "%H:%M") - (datetime.strptime(S_time, "%H:%M") + S_offset)
                if (waiting.total_seconds()/60) <= 0:
                    continue
                
                if (waiting.total_seconds()/60) > 25:
                    continue

                S_Compatible.append((S_time, int(waiting.total_seconds()/60), B_time))

            for U_time in U_times:
                waiting = datetime.strptime(B_time, "%H:%M") - (datetime.strptime(U_time, "%H:%M") + U_offset)
                if (waiting.total_seconds()/60) <= 0:
                    continue
                
                if (waiting.total_seconds()/60) > 25:
                    continue

                U_Compatible.append((U_time, int(waiting.total_seconds()/60), B_time))

    return S_Compatible, U_Compatible

def export_schedules():
    data = {}

    for dest in ["Koropi", "Doukissis"]:
        data[dest] = {}
        for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            S_Table, U_Table = best_times(dest, day)

            data[dest][day] = {
                "SubRail": S_Table,
                "Metro": U_Table
            }

    with open("schedules.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":

    export_schedules()