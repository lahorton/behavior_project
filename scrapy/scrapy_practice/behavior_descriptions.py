import scrapy
import json

class ScrapyPractice(scrapy.Spider):
    # This scrapes each page that describes the various behaviors.
    name = "behaviors"

    def start_requests(self):
        urls = ['http://www.pbisworld.com/behavior-descriptions/aggressive-bullying/', 'http://www.pbisworld.com/behavior-descriptions/anxiety/', 'http://www.pbisworld.com/behavior-descriptions/confrontational-defensive/', 'http://www.pbisworld.com/behavior-descriptions/defiant/', 'http://www.pbisworld.com/behavior-descriptions/disorganized/', 'http://www.pbisworld.com/behavior-descriptions/disrespectful/', 'http://www.pbisworld.com/behavior-descriptions/disruptive/', 'http://www.pbisworld.com/behavior-descriptions/failing-to-turn-in-work/', 'http://www.pbisworld.com/behavior-descriptions/frustration/', 'http://www.pbisworld.com/behavior-descriptions/hyperactivity/', 'http://www.pbisworld.com/behavior-descriptions/impulsive/', 'http://www.pbisworld.com/behavior-descriptions/inappropriate-language/', 'http://www.pbisworld.com/behavior-descriptions/lack-of-participation/', 'http://www.pbisworld.com/behavior-descriptions/lack-of-responsibility/', 'http://www.pbisworld.com/behavior-descriptions/lack-of-social-skills/', 'http://www.pbisworld.com/behavior-descriptions/low-or-no-work-completion/', 'http://www.pbisworld.com/behavior-descriptions/lying-cheating', 'http://www.pbisworld.com/behavior-descriptions/name-calling/', 'http://www.pbisworld.com/behavior-descriptions/negative-attitude/', 'http://www.pbisworld.com/behavior-descriptions/off-task-disruptive/', 'http://www.pbisworld.com/behavior-descriptions/off-task-non-disruptive/', 'http://www.pbisworld.com/behavior-descriptions/out-of-seat/', 'http://www.pbisworld.com/behavior-descriptions/poor-coping-skills/', 'http://www.pbisworld.com/behavior-descriptions/poor-peer-relationships/', 'http://www.pbisworld.com/behavior-descriptions/poor-self-esteem/', 'http://www.pbisworld.com/behavior-descriptions/rushing-through-work/', 'http://www.pbisworld.com/behavior-descriptions/sadness-depression/', 'http://www.pbisworld.com/behavior-descriptions/somatic-complaints/', 'http://www.pbisworld.com/behavior-descriptions/stealing/', 'http://www.pbisworld.com/behavior-descriptions/tantrums-out-of-control/', 'http://www.pbisworld.com/behavior-descriptions/tardiness/', 'http://www.pbisworld.com/behavior-descriptions/unable-to-work-independently/', 'http://www.pbisworld.com/behavior-descriptions/unfocused-inattentive/', 'http://www.pbisworld.com/behavior-descriptions/unmotivated/', 'http://www.pbisworld.com/behavior-descriptions/upset-crying/', 'http://www.pbisworld.com/behavior-descriptions/other/']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # This gets a dictionary with separate lists of urls and behavior descriptions.
    # def parse(self, response):
    #     SET = 'div.behavtable'
    #     for tablea in response.css(SET):
    #         yield {
    #             'url' : tablea.css('.tablea ::attr(href)').extract(),
    #             'words' : tablea.css('.tablea ::text').extract()
    #         }

    def parse(self, response):
        SET = 'div #content'
        SET_1 = 'div.titlecent'

        list_behav_dict = []
        for SET in response.css(SET):
            behav_dict = {}
            title = response.css('div.titlecent ::text').extract()
            title = "".join(title)
            title = title.strip()
            description = response.css('.behavdes ul ::text').extract()
            description = "".join(description)
            description = description.strip()
            behav_dict[title] = description
            list_behav_dict.append(behav_dict)

        print(list_behav_dict)



            # yield{
            #     'title': response.css('div.titlecent ::text').extract(),
            #     'description': response.css('.behavdes ul ::text').extract()
            # }


    #this works to extract all the content on the page as a list.
    # response.css('div #content ::text').extract()

    #this works for the entire content w/ list: div #content

    #scrapy -o behavior_descriptions.json

