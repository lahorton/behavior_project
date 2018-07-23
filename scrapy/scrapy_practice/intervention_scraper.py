import scrapy
import json

class ScrapyPractice(scrapy.Spider):
    """ This scrapes each page that describes the interventions"""
    name = "interventions"

    def start_requests(self):
        urls = ['http://www.pbisworld.com/tier-1/interventions-by-behavior/aggressive-bullying/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/anxiety/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/confrontational-defensive/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/defiant/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/disorganized/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/disrespectful/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/disruptive/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/failing-to-turn-in-work/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/frustration/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/hyperactivity/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/impulsive/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/inappropriate-language/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/lack-of-participation/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/lack-of-responsibility/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/lack-of-social-skills/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/low-or-no-work-completion/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/lying-cheating', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/name-calling/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/negative-attitude/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/off-task-disruptive/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/off-task-non-disruptive/', 
                'http://www.pbisworld.com/tier-1/tier-1/interventions-by-behavior/out-of-seat/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/poor-coping-skills/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/poor-peer-relationships/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/poor-self-esteem/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/rushing-through-work/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/sadness-depression/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/somatic-complaints/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/stealing/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/tantrums-out-of-control/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/tardiness/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/unable-to-work-independently/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/unfocused-inattentive/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/unmotivated/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/upset-crying/', 
                'http://www.pbisworld.com/tier-1/interventions-by-behavior/other/']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        """parses the urls from start_requests"""

        SET = 'div.format_text'

        for SET in response.css(SET):
            yield{
                'behavior': response.css('div.format_text ::text').extract()
            }

    # this runs it in the v env: scrapy runspider scraper.py

    
    # scrapy runspider intervention_scraper.py -o intervention_data.json