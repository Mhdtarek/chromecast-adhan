import argparse 
import logging 
import requests 
import schedule 
import sys 
import time 
import zeroconf 
from pychromecast import quick_play 
from rich.console import Console 
from rich.table import Table 
CAST_NAME = "kok" 
MEDIA_URL = "https://media.sd.ma/assabile/adhan_3435370/cd17c7200df5.mp3" 
console = Console() 
 
def get_prayer_times(city, country): 
   url = "http://api.aladhan.com/v1/timingsByCity?" 
   full_url = f"{url}city={city}&country={country}&method=4" 
   response = requests.get(full_url) 
   return response.json()["data"]["timings"] 
 
def display_prayer_times(times): 
   table = Table(title="Prayer Times today") 
   for prayer, time in times.items(): 
       table.add_row(prayer, time) 
   console.print(table) 
 
def schedule_prayers(times, include_isha_fajr): 
   prayers = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"] if include_isha_fajr else ["Dhuhr", "Asr", "Maghrib"] 
   for prayer in prayers: 
       schedule.every().day.at(times[prayer]).do(prayer_time) 
   while True: 
       schedule.run_pending() 
       time.sleep(1) 
 
def prayer_time(): 
   args = get_args() 
   setup_logging(args) 
   chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[args.cast], known_hosts=args.known_host) 
   if not chromecasts: 
       print(f'No chromecast with name "{args.cast}" discovered') 
       sys.exit(1) 
   cast = list(chromecasts)[0] 
   cast.wait() 
   app_name = "homeassistant_media" 
   app_data = {"media_id": args.url} 
   quick_play.quick_play(cast, app_name, app_data) 
   time.sleep(10) 
   browser.stop_discovery() 
 
def get_args(): 
   parser = argparse.ArgumentParser(description="Example on how to use the Home Asssitant Media Controller to play an URL.") 
   parser.add_argument("--cast", default=CAST_NAME) 
   parser.add_argument("--known-host", action="append") 
   parser.add_argument("--show-debug", action="store_true") 
   parser.add_argument("--show-zeroconf-debug", action="store_true") 
   parser.add_argument("--url", default=MEDIA_URL) 
   return parser.parse_args() 
 
def setup_logging(args): 
   if args.show_debug: 
       logging.basicConfig(level=logging.DEBUG) 
   if args.show_zeroconf_debug: 
       print("Zeroconf version: " + zeroconf.__version__) 
       logging.getLogger("zeroconf").setLevel(logging.DEBUG) 
 
def main(): 
   mode = console.input("[yellow]Usage[/] (1: Prayer Times, 2: Quran chromecast):?") 
   if mode == "1": 
       city = console.input("What's the city that you are in (use % for space)? ") 
       country = console.input("What country are you in (use % for space and no abreviations)? ") 
       times = get_prayer_times(city, country) 
       display_prayer_times(times) 
       if console.input("do you want to broadcast when it's time to pray (y/n)? ") == "y": 
           include_isha_fajr = console.input("Do you want to include Isha And Fajr (y/n)? ") == "y" 
           schedule_prayers(times, include_isha_fajr) 
   else: 
       ayah_or_surah = console.input("Ayah or Surah (a/s)? ") 
       if ayah_or_surah == "a": 
           AyahUrl = "https://cdn.islamic.network/quran/audio/128/ar.alafasy/" 
           AyahNumber = console.input("Ayah Number?[bold] [/]") 
           MEDIA_URL = AyahUrl + AyahNumber + ".mp3" 
       elif ayah_or_surah == "s": 
           SurahUrl = "https://cdn.islamic.network/quran/audio-surah/128/ar.alafasy/" 
           SurahNumber = console.input("Surah Number?[bold] [/]") 
           MEDIA_URL = SurahUrl + SurahNumber + ".mp3" 
       prayer_time() 
 
if __name__ == "__main__": 
   main()
