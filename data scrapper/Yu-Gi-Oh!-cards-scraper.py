#from scrapy import Spider, Item, Field
from collections import OrderedDict

import scrapy
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.linkextractors import LinkExtractor

class Card(scrapy.Item):
  url = scrapy.Field()
  title = scrapy.Field()
  attribute = scrapy.Field()
  level = scrapy.Field()
  monster_type = scrapy.Field()
  card_type = scrapy.Field()
  attack = scrapy.Field()
  defence = scrapy.Field()
  description = scrapy.Field()
  pendulum_scale = scrapy.Field()
  pendulum_effect = scrapy.Field()
  decks = scrapy.Field()

class Deck(scrapy.Item):
  title = scrapy.Field()
  number_of_cards = scrapy.Field()
  url = scrapy.Field()
  cards = []

# def parse_url(value):
#     print value
#     return value

class YuGiOh_spider(CrawlSpider):
  name = 'Yu-Gi-Oh! Decks & Cards'
  start_urls = ['http://www.db.yugioh-card.com/yugiohdb/card_list.action']
  rules = [Rule(LinkExtractor(tags='input', attrs='value', restrict_xpaths='//*[@class="pack pack_en"]', unique=True), 'parse_deck')]
  #rules += [Rule(LinkExtractor(tags='input', attrs='value', restrict_xpaths='//*[@class="list_style"]/ul/li', unique=True), 'parse_card')]

  def clean_data(self, data):
    for key in data.keys():
      data[key] = data[key].strip()
    return data

  def parse_7rows_cards(self, details_table_rows, card):
    card['attribute'] = details_table_rows[0].css('td')[0].css('span.item_box_value::text').extract()[0]
    card['level'] = details_table_rows[0].css('td')[1].css('span.item_box_value::text').extract()[0]
    card['pendulum_scale'] = details_table_rows[1].css('td div::text').extract()[1]
    card['pendulum_effect'] = details_table_rows[2].css('td div::text').extract()[3]
    card['monster_type'] = details_table_rows[3].css('td div::text').extract()[1]
    card['card_type'] = details_table_rows[4].css('td div::text').extract()[2]
    card['attack'] = details_table_rows[5].css('td')[0].css('span.item_box_value::text').extract()[0]
    card['defence'] = details_table_rows[5].css('td')[1].css('span.item_box_value::text').extract()[0]
    card['description'] = details_table_rows[6].css('td div::text').extract()[3]

  def parse_5rows_cards(self, details_table_rows, card):
    card['attribute'] = details_table_rows[0].css('td')[0].css('span.item_box_value::text').extract()[0]
    card['level'] = details_table_rows[0].css('td')[1].css('span.item_box_value::text').extract()[0]
    card['monster_type'] = details_table_rows[1].css('td div::text').extract()[1]
    card['card_type'] = details_table_rows[2].css('td div::text').extract()[2]
    card['attack'] = details_table_rows[3].css('td')[0].css('span.item_box_value::text').extract()[0]
    card['defence'] = details_table_rows[3].css('td')[1].css('span.item_box_value::text').extract()[0]
    card['description'] = details_table_rows[4].css('td div::text').extract()[3]
    card['pendulum_effect'] = 'N/A'
    card['pendulum_scale'] = 'N/A'

  def parse_2rows_cards(self,details_table_rows, card):
    card['attribute'] = details_table_rows[0].css('td')[0].css('div::text').extract()[1]
    card['description'] = details_table_rows[1].css('td')[0].css('div::text').extract()[3]
    card['level'] = 'N/A'
    card['monster_type'] = 'N/A'
    card['card_type'] = 'N/A'
    card['attack'] = 'N/A'
    card['defence'] = 'N/A'
    card['pendulum_effect'] = 'N/A'
    card['pendulum_scale'] = 'N/A'

  def parse_card(self, response):
    number_of_rows = len(response.css('#details tr'))
    details_table_rows = response.selector.css('#details tr')
    card = Card()
    card['url'] = response.url
    card['title'] = response.xpath('//*[@id="broad_title"]/div/h1/text()').extract()[0]
    if number_of_rows == 7:
      self.parse_7rows_cards(details_table_rows, card)
    elif number_of_rows == 5:
      self.parse_5rows_cards(details_table_rows, card)
    elif number_of_rows == 2:
      self.parse_2rows_cards(details_table_rows, card)
    else:
      raise Exception('----------$%#^%$#^Unknown nuumber of rows: %s' % number_of_rows)
    card = self.clean_data(card)
    decks = response.css('#pack_list table tr td b::text').extract()
    decks =  list(OrderedDict.fromkeys(decks))
    card['decks'] = decks
    return card

  def parse_deck(self, response):
    deck = Deck()
    deck['url'] = response.url
    deck['title'] = response.css("#broad_title > div > h1 > strong::text").extract()
    deck['number_of_cards'] = response.css('div.page_num_title > div > strong::text').re('.*?(\d+).*')
    return deck
    #yield scrapy.Request(response.url)

#"""
#  Card >>>>>> http://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=2&cid=4041
#  
#  yugi deck >>> http://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=1&pid=13311001&rp=99999
#"""