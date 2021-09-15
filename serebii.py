# https://www.analyticsvidhya.com/blog/2017/07/web-scraping-in-python-using-scrapy/
# https://www.digitalocean.com/community/tutorials/como-fazer-crawling-em-uma-pagina-web-com-scrapy-e-python-3-pt
# http://pythonclub.com.br/material-do-tutorial-web-scraping-na-nuvem.html
import scrapy

class PokemonDamageScrapper(scrapy.Spider):
    name = 'pokemon_damage_scrapper'
    domain = 'https://www.serebii.net'

    start_urls = ["https://www.serebii.net/pokedex-swsh/"]

    def parse(self, response):

        # dexTable = response.css('.dextab tr td a::attr(href)').getall()
        # print(dexTable)
        regions = {
        "kanto"  : response.css('form[name="nav"]'),
        "johto"  : response.css('form[name="nav2"]'),
        "hoenn"  : response.css('form[name="nav4"]'),
        "sinnoh" : response.css('form[name="nav5"]'),
        "unova"  : response.css('form[name="nav6"]'),
        "kalos"  : response.css('form[name="nav7"]'),
        "alola"  : response.css('form[name="nav8"]'),
        "galar"  : response.css('form[name="nav9"]')
        }
        
        for r, form in regions.items():
            optionsLink = form.css('select option::attr(value)').getall()
            # print(r, optionsLink)
            optionsLink.pop(0)
            for pkmnLink in optionsLink:
                pkmn = pkmnLink.split('/')[2]
                # print(pkmn)
                
                yield response.follow(self.domain + pkmnLink, self.parse_pokemon, meta={'name' : pkmn})

    def parse_pokemon(self, response):
        name = response.meta.get('name')
    
        texth1 = response.xpath('string(//*[@id="content"]/main/div[2]/table[1]/tr/td[1]/table/tr/td[2]/h1/text())').get()
        array = texth1.split(";", 1)
        array[0] = array[0].strip()

        print(array)

        yield {
            'Ndex' : array[0],
            'pokemon_name' : array[1],
            'Normal'   : response.xpath('string(//h2[.="Weakness"]/../../../tr[3]/td[1]/text())').get(),
            'Fire'     : response.xpath('string(//h2[.="Weakness"]/../../../tr[3]/td[2]/text())').get(),
            'Water'    : response.xpath('string(//h2[.="Weakness"]/../../../tr[3]/td[3]/text())').get(),
            'Electric' : response.xpath('string(//h2[.="Weakness"]/../../../tr[3]/td[4]/text())').get(),
            'Grass'    : response.xpath('string(//h2[.="Weakness"]/../../../tr[3]/td[5]/text())').get(),
            'Ice'      : response.xpath('string(//h2[.="Weakness"]/../../../tr[3]/td[6]/text())').get(),
            'Fighting' : response.xpath('string(//h2[.="Weakness"]/../../../tr[3]/td[7]/text())').get(),
            'Poison'   : response.xpath('string(//h2[.="Weakness"]/../../../tr[3]/td[8]/text())').get(),
            'Ground'   : response.xpath('string(//h2[.="Weakness"]/../../../tr[3]/td[9]/text())').get(),
            'Flying'   : response.xpath('string(//h2[.="Weakness"]/../../../tr[3]/td[10]/text())').get(),
            'Psychic'  : response.xpath('string(//h2[.="Weakness"]/../../../tr[3]/td[11]/text())').get(),
            'Bug'      : response.xpath('string(//h2[.="Weakness"]/../../../tr[3]/td[12]/text())').get(),
            'Rock'     : response.xpath('string(//h2[.="Weakness"]/../../../tr[3]/td[13]/text())').get(),
            'Ghost'    : response.xpath('string(//h2[.="Weakness"]/../../../tr[3]/td[14]/text())').get(),
            'Dragon'   : response.xpath('string(//h2[.="Weakness"]/../../../tr[3]/td[15]/text())').get(),
            'Dark'     : response.xpath('string(//h2[.="Weakness"]/../../../tr[3]/td[16]/text())').get(),
            'Steel'    : response.xpath('string(//h2[.="Weakness"]/../../../tr[3]/td[17]/text())').get(),
            'Fairy'    : response.xpath('string(//h2[.="Weakness"]/../../../tr[3]/td[18]/text())').get() 
        }

        # //*[@id="content"]/main/div[2]/table[1]/tbody/tr/td[1]/table/tbody/tr/td[2]/h1
        # //*[@id="content"]/main/div[2]/table[1]/tbody/tr/td[1]/table/tbody/tr/td[2]/h1
        # #content > main > div:nth-child(2) > table:nth-child(1) > tbody > tr > td:nth-child(1) > table > tbody > tr > td:nth-child(2) > h1