# SpellCrawler – Website Spell Checker

Scan your website for misspelled words and generate an HTML report.

Docker must be installed and open in order to run.
Rebuild after each run.

## Quick Start

1. Replace the URL in spellcheck_spider.py
2. On Windows, run the run_spellcrawler.bat file.
3. On Mac, run the commands below in the terminal and then run the run_spellcrawler_mac.command file. (only need to do once per installation)
#### Please remember that file path may vary. Replace folder names as needed.

### cd downloads
### cd spellcrawler-main (or whatever the project folder is called)
### chmod +x run_spellcrawler_mac.command


## Manually start

1. Replace the URL in spellcheck_spider.py
2. Point to directory (varies, but typically use cd <main folder file path goes here>).
3. Run local server: python allow_server.py
4. In a separate cmd prompt, point to directory again.
5. Build Docker image: docker build -t spellcrawler .
6. Run crawler: docker run -v "%cd%\output:/app/output" spellcrawler
7. Open output/spell_report.html


## WINDOWS:
### Easy paste 1:
##### cd downloads
##### cd spellcrawler-main
##### python allow_server.py

### Easy paste 2: 
##### cd downloads
##### cd spellcrawler-main
##### docker build -t spellcrawler .
##### docker run -v "%cd%\output:/app/output" spellcrawler


## MAC:
### Easy paste 1:
##### cd downloads
##### cd spellcrawler-main
##### python3 allow_server.py

### Easy paste 2: 
##### cd downloads
##### cd spellcrawler-main
##### docker build -t spellcrawler .
##### docker run -v "$(pwd)/output:/app/output" spellcrawler

