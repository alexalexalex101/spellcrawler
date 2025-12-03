import scrapy
from spellchecker import SpellChecker
from scrapy import signals
from scrapy.signalmanager import dispatcher
from jinja2 import Template
import unicodedata
import os


def find_project_root():
    """
    Returns the correct project root path on:
    - Windows
    - macOS
    - Linux
    - Docker (/app)
    - When running from ANY folder
    """

    # Docker always uses /app
    if os.path.exists("/app") and os.path.isdir("/app"):
        return "/app"

    # Otherwise walk upward from this file until scrapy.cfg is found
    path = os.path.abspath(__file__)
    while True:
        path = os.path.dirname(path)
        if os.path.exists(os.path.join(path, "scrapy.cfg")):
            return path
        if path == "/" or len(path) < 3:
            break

    # Fallback to old behavior (project root = two levels up)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def remove_accents(text):
    nfkd_form = unicodedata.normalize("NFD", text)
    return "".join(c for c in nfkd_form if not unicodedata.combining(c))


class SpellCheckSpider(scrapy.Spider):
    name = "spellcheck"
    allowed_domains = ["pctvs.org"]
    start_urls = ["https://pctvs.org"]

    custom_settings = {
        "CLOSESPIDER_PAGECOUNT": 1000,  # limit crawl
    }

    def __init__(self):
        self.results = []
        self.spell = SpellChecker(language="en")

        # Load Spanish word list
        if os.path.exists("spanish_words.txt"):
            with open("spanish_words.txt", encoding="utf-8") as f:
                clean_words = [remove_accents(w.strip().lower()) for w in f if w.strip()]
            self.spell.word_frequency.load_words(clean_words)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        spanish_file = os.path.join(base_dir, "spanish_words.txt")

        if os.path.exists(spanish_file):
            self.spell.word_frequency.load_text_file(spanish_file)
        else:
            self.logger.warning(f"spanish_words.txt not found at {spanish_file}!!")

        self.page_count = 0

        # Custom allowed words
        self.custom_words = {
            "pctvs", "Passaic", "County", "Technical", "Institute",
            "Wayne", "New", "Jersey", "Google", "Microsoft", "Facebook",
            "STEM", "Cisco", "AutoCAD", "Python", "JavaScript",
            "CTE", "NJ", "PCTI", "async", "div", "etc", "max",
            "noreferrer", "rschooltoday", "submenu", "svg",
        }

        # Load custom dictionary
        self.spell.word_frequency.load_words({remove_accents(w.lower()) for w in self.custom_words})

        # Load extra custom words from file
        project_root = find_project_root()
        self.project_root = project_root
        custom_file = os.path.join(project_root, "custom_words.txt")

        if os.path.exists(custom_file):
            with open(custom_file, encoding="utf-8") as f:
                extra_words = [remove_accents(w.strip().lower()) for w in f if w.strip()]
            self.spell.word_frequency.load_words(extra_words)
        else:
            self.logger.warning(f"custom_words.txt not found at {custom_file}!!")

        # Connect spider_closed to closing signal
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):
        self.page_count += 1
        self.logger.info(f"📄 Crawled page #{self.page_count}: {response.url}")

        text = " ".join(response.css("body *::text").getall())

        words = []
        for w in text.split():
            stripped = w.strip(".,!?()[]{}:;\"'")
            if stripped[:1].isupper():
                continue

            clean = remove_accents(stripped.lower())
            if clean.isalpha() and 3 <= len(clean) <= 20:
                words.append(clean)

        misspelled = sorted(list(self.spell.unknown(words)))

        self.results.append({
            "url": response.url,
            "misspelled": misspelled
        })

        # FOLLOW ONLY INTERNAL LINKS
        for link in response.css("a::attr(href)").getall():
            url = response.urljoin(link)

            if not url.startswith("http"):
                continue

            if "pctvs.org" in url:
                yield scrapy.Request(url, callback=self.parse)

    def spider_closed(self, spider):
        project_root = find_project_root()
        output_dir = "/app/output"
        os.makedirs(output_dir, exist_ok=True)

        template_path = os.path.join(project_root, "templates", "report_template.html")

        with open(template_path, encoding="utf-8") as f:
            template = Template(f.read())

        sorted_results = sorted(self.results, key=lambda x: len(x["misspelled"]), reverse=True)

        html = template.render(
            pages=sorted_results,
            total_pages=self.page_count,
        )

        output_path = os.path.join(output_dir, "spell_report.html")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        self.logger.info(f"✅ Spell check report saved to {output_path}")
