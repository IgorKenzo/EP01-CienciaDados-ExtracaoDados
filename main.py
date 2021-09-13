# https://www.analyticsvidhya.com/blog/2017/07/web-scraping-in-python-using-scrapy/
# https://www.digitalocean.com/community/tutorials/como-fazer-crawling-em-uma-pagina-web-com-scrapy-e-python-3-pt
# http://pythonclub.com.br/material-do-tutorial-web-scraping-na-nuvem.html
import scrapy
import re

class PokemonScrapper(scrapy.Spider):
    name = 'pokemon_scrapper'
    domain = 'https://bulbapedia.bulbagarden.net'

    start_urls = ["https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"]

    def parse(self, response):

        pokemons = response.css('tr')

        for pokemon in pokemons:
            #yield {'pokemon_name': pokemon.css('td>a::text').get()}
            # print({
            #     'Ndex' : pokemon.css('td:nth-child(2)::text').get(),
            #     't1' : pokemon.css('td:nth-child(5)>a>span::text').get(),
            #     't2' : pokemon.css('td:nth-child(6)>a>span::text').get()
            # })
            
            pokemon_url = pokemon.css('td>a::attr(href)').get()
            if pokemon_url is not None:
                yield response.follow(self.domain + pokemon_url, self.parse_pokemon)

    def parse_pokemon(self, response):
        # yield {'pokemon_name': response.css('td big big b::text').get(),
        # 'Height': response.css('.mw-parser-output>table:nth-of-type(2)>tbody>tr:nth-of-type(6)>td>table>tbody>tr>td:nth-of-type(2)::text').get(),
        # 'Weight': response.css('.mw-parser-output>table:nth-of-type(2)>tbody>tr:nth-of-type(6)>td:nth-of-type(2)>table>tbody>tr>td:nth-of-type(2)::text').get()}
        # print({
        #     't1' : response.xpath('string(//*[@id="mw-content-text"]/div/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr/td[1])').get(),
        #     't2' : response.xpath('string(//*[@id="mw-content-text"]/div/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2])').get()
        # })    
        
        # evo = re.search(r"(?<=(into)) ([\w\s\'\-]+|(Mr\. (Mime|Rime))) (?=(starting)|(when))", response.xpath('string(//*[@id="mw-content-text"])').get())
        # a = evo
        # if a != None:
        #     a = a.group().strip()
        #     if a == "Mr. Mime" or a == "Mr. Rime" or a == "Mime Jr":
        #         pass
        #     else:
        #         a = a.split(" ")
        #         if len(a) > 1 or a == "being":
        #             a = None
        evo = ""    
        t = response.xpath('string(//*[@id="mw-content-text"])').get()
        while True:
            e = re.search(r"(?<=nto| or)(?: either)?((?:\s[A-Z][\w\.'-]+)+) (?=(starting)|(when))", t)
            which = re.search(r"which", t)
            if e == None: break
            else:
                if which != None:
                    if e.span()[0] > which.span()[0]: break

                evo += e.group(1).strip() + "#"
                t = t[0:e.span()[0]:] + t[e.span()[1]::]

        # print(response.url)
        # print(response.css('td big big b::text').get())
        # print(evo)
        yield {
            'Ndex' : response.xpath('string(//*[@id="mw-content-text"]/div/table[2]/tbody/tr[1]/td/table/tbody/tr[1]/th/big/big/a/span)').re(r"#\d\d\d")[0],
            'pokemon_name': response.css('td big big b::text').get(),
            'pokemon_height': response.xpath('string(//*[@id="mw-content-text"]/div/table[2])').re(r"\d+\.\d+ m")[0],
            'pokemon_weight': response.xpath('string(//*[@id="mw-content-text"]/div/table[2])').re(r"\d+\.\d+ kg")[0],
            't1' : response.xpath('string(//*[@id="mw-content-text"]/div/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr/td[1])').get().strip(),
            't2' : response.xpath('string(//*[@id="mw-content-text"]/div/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2])').get().strip(),
            'color' : response.xpath('string(//a[@title="List of Pokémon by color"]/../../table/tbody/tr/td/text())').get().strip(),
           'evolution' : evo if evo != "" else "Final"
        #    'evolution' : a if a != None else "Final"
            #a[title*="List of Pokémon by color"]
            #//a[title="List of Pokémon by color"]/../../tbody/tr/td/text())
            #response.xpath('string(//*[@id="mw-content-text"]/div/table[2]/tbody/tr[11]/td[1]/table/tbody/tr/td/text())').get()
        }                                    