import os
import re
import time
import requests
from datetime import datetime, timezone
from pydantic import BaseModel
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()
BASE_URL = "https://api.boerse-frankfurt.de/v1/data/category_news?newsType=ALL&lang=de&offset=0&limit=50"

class Summary(BaseModel):
    bullet_points: list[str]

def fetch_latest_news():
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 429:
            print("API rate limit reached (HTTP 429). Pausing for 60 seconds before retrying.")
            time.sleep(60)
            return None
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        return None
    try:
        json_data = response.json()
    except ValueError as json_err:
        print(f"Error parsing JSON response: {json_err}")
        return None
    if "data" in json_data and len(json_data["data"]) > 0:
        return json_data["data"][0]
    else:
        print("No news data available in the API response.")
        return None

def format_german_time(iso_time_str):
    try:
        dt = datetime.fromisoformat(iso_time_str)
        return dt.strftime("%d.%m.%Y %H:%M:%S")
    except Exception as e:
        print(f"Error formatting time: {e}")
        return iso_time_str

def format_time_difference(diff):
    total_seconds = int(diff.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

def fetch_news_body(path_segment):
    detail_url = f"https://api.boerse-frankfurt.de/v1/data/news?id={path_segment}&lang=de"
    try:
        response = requests.get(detail_url)
        response.raise_for_status()
        data = response.json()
        return data.get("body", "")
    except Exception as e:
        print(f"Error fetching detailed news body: {e}")
        return ""

def clean_html(raw_html):
    clean_text = re.sub('<.*?>', '', raw_html)
    return clean_text.strip()

def summarize_text(text: str) -> list[str]:
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Du bist ein Experte im Zusammenfassen von Nachrichten. Extrahiere die wichtigsten Punkte als eine Liste von Stichpunkten."},
                {"role": "user", "content": f"Fasse den folgenden Nachrichtentext in prägnante Stichpunkte zusammen:\n\n{text}"}
            ],
            response_format=Summary,
        )
        summary = completion.choices[0].message.parsed
        return summary.bullet_points
    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return ["Zusammenfassung nicht verfügbar."]

def monitor_news(poll_interval=15):
    last_id = None
    while True:
        news = fetch_latest_news()
        if news:
            current_id = news.get("id")
            if current_id != last_id:
                last_id = current_id
                headline = news.get("headline", "N/A")
                path_segment = news.get("pathSegment", "N/A")
                iso_time = news.get("time", "")
                formatted_release_time = format_german_time(iso_time) if iso_time else "N/A"
                try:
                    release_time = datetime.fromisoformat(iso_time)
                except Exception as e:
                    print(f"Error parsing release time: {e}")
                    release_time = None
                scraping_time = datetime.now(timezone.utc).astimezone()
                formatted_scraping_time = scraping_time.strftime("%d.%m.%Y %H:%M:%S")
                if release_time:
                    time_diff = scraping_time - release_time
                    formatted_diff = format_time_difference(time_diff)
                else:
                    formatted_diff = "N/A"
                raw_body = fetch_news_body(path_segment)
                if raw_body:
                    body_text = clean_html(raw_body)
                    print("Erzeuge KI-Zusammenfassung (bitte warten)...")
                    bullet_points = summarize_text(body_text)
                else:
                    bullet_points = ["Kein detaillierter Nachrichtentext gefunden."]
                output = (
                    f"Neue Nachricht gefunden:\n"
                    f"  Headline                   : {headline}\n"
                    f"  Path Segment               : {path_segment}\n"
                    f"  Veröffentlichungszeit      : {formatted_release_time}\n"
                    f"  Scraping-Zeit              : {formatted_scraping_time}\n"
                    f"  Zeit seit Veröffentlichung : {formatted_diff}\n\n"
                    "KI-Zusammenfassung in Stichpunkten:\n"
                )
                for point in bullet_points:
                    output += f"- {point}\n"
                print(output)
        time.sleep(poll_interval)

if __name__ == "__main__":
    monitor_news()
