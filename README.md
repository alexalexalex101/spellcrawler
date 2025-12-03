# SpellCrawler – Website Spell Checker

Scan your website for misspelled words and generate an HTML report.

Docker is required to run this crawler.
Rebuild after each run.

For ease of use, move project folder to the user's folder.
Otherwise, find the file path of the project folder and cd into the first "spellcrawler" directory.

## Quick Start

1. Replace the URL in spellcheck_spider.py
2. On Windows, run the run_spellcrawler.bat file.
3. On Mac, run the command below in the terminal once and then run the file.
chmod +x run_spellcrawler_mac.command


## Manually start

1. Replace the URL in spellcheck_spider.py
2. Point to directory: cd spellcrawler
3. Run local server: python allow_server.py
4. In a separate cmd prompt, point to directory: cd spellcrawler
5. Build Docker image: docker build -t spellcrawler .
6. Run crawler: docker run -v "%cd%\output:/app/output" spellcrawler
7. Open output/spell_report.html


Ran from user folder:
## WINDOWS:
Easy paste 1:
cd spellcrawler
python allow_server.py

Easy paste 2: 
cd spellcrawler
docker build -t spellcrawler .
docker run -v "%cd%\output:/app/output" spellcrawler


## MAC:
Easy paste 1:
cd spellcrawler
python3 allow_server.py

Easy paste 2: 
cd spellcrawler
docker build -t spellcrawler .
docker run -v "$(pwd)/output:/app/output" spellcrawler

