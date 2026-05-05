import scrapy
from scrapy_playwright.page import PageMethod


class CourseraSpider(scrapy.Spider):
    name = "coursera"

    start_urls = [
        "https://www.coursera.org/search?query=maths"
    ]



    def parse_metadata(self, card):
        text = " ".join(card.css("p::text").getall())

        level = None
        course_type = None
        duration = None

        parts = [p.strip() for p in text.split("·")]

        for part in parts:
            if part in ["Beginner", "Intermediate", "Advanced"]:
                level = part
            elif "month" in part.lower() or "week" in part.lower():
                duration = part
            else:
                course_type = part  # Course / Specialization / Certificate

        return level, course_type, duration




    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("goto", url),
                        PageMethod("wait_for_load_state", "networkidle"),
                        PageMethod("wait_for_selector", "h3")
                    ]
                }
            )

    


    def parse(self, response):

        cards = response.css("div.cds-ProductCard-gridCard")

        for card in cards:

            level, course_type, duration = self.parse_metadata(card)

            yield {
            "platform": "Coursera",
            "title": card.css("h3::text").get(),
            "url": response.urljoin(card.css("a::attr(href)").get()),
            "level": level,
            "duration": duration
            }

    def extract_rating(self, card):
        text = " ".join(card.css("p::text").getall())
        if "★" in text:
            return text.split("★")[1].split()[0]
        return None

    def extract_level(self, card):
        for t in card.css("p::text").getall():
            if t.strip() in ["Beginner", "Intermediate", "Advanced"]:
                return t.strip()
        return None

    def extract_duration(self, card):
        for t in card.css("p::text").getall():
            if "week" in t.lower() or "month" in t.lower():
                return t.strip()
        return None