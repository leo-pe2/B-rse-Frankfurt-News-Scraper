# B-rse-Frankfurt-News-Scraper
Scrapes the API of https://www.boerse-frankfurt.de/nachrichten (in german). Gpt-4o-mini will generate a summary of the news content. 
The python script monitors the endpoint and checks every 15s for new entries. 
Disadvantage: The time of publishing is always 9-15min behind the current time.

To use: Create a .env file and paste your OpenAI API KEY. OPENAI_API_KEY=...

Example output:

Neue Nachricht gefunden:
  Headline                   : ROUNDUP/Kampf der Keybox: Florenz verbietet Schlüsselkästen
  Path Segment               : ROUNDUP-Kampf-der-Keybox-Florenz-verbietet-Schluesselkaesten-d3d748d6-e88e-4365-850a-0334d4874a96
  Veröffentlichungszeit      : 11.02.2025 11:49:04
  Scraping-Zeit              : 11.02.2025 12:04:18
  Zeit seit Veröffentlichung : 0h 15m 14s

KI-Zusammenfassung in Stichpunkten:
- Florenz verbietet als erste große Stadt in Italien Schlüsselkästen für Ferienwohnungen.
- Gemeinderat verabschiedete Regelung mit großer Mehrheit zur Bekämpfung des Massentourismus.
- Ziel ist es, Mietwohnungen zu schützen und die Lebensqualität der Anwohner zu verbessern.
- Eigentümer von Ferienwohnungen haben 10 Tage Zeit, um Schlüsselkästen abzunehmen; sonst droht eine Strafe von 400 Euro.
- Protest von Anwohnern, die unter Airbnb-Vermietungen leiden; Bürgerinitiative 'Salviamo Firenze' aktiv.
- Italien hat bereits bestehende Regelungen für Kurzzeit-Vermietungen, einschl. persönlicher Treffen zwischen Besitzern und Gästen.
- Florenz empfängt jährlich über 4,5 Millionen Touristen, während das historische Zentrum nur noch 60.000 Einwohner hat.
- In anderen Städten wie Rom und Venedig werden ebenfalls Regelungen angestrebt, um den Massentourismus zu kontrollieren.
- Venedig verlangt seit letztem Jahr Eintritt von Kurzbesuchern, um die Besucherzahlen zu steuern.
