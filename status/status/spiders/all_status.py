# -*- coding: utf-8 -*-
import scrapy


class AllStatusSpider(scrapy.Spider):
    name = 'all_status'
    allowed_domains = ['isga.obrnadzor.gov.ru']
    #start_urls = ['http://isga.obrnadzor.gov.ru/accredreestr/details/0b0e1313-1010-130d-0f11-0e0c130e0c11/1/']

    with open('status_ids.txt') as f:
        ids = f.readlines()

    ids = [x.strip() for x in ids]

    start_urls = []
    for item in ids:
        start_urls.append('http://isga.obrnadzor.gov.ru/accredreestr/details/' + item + '/1/')

    def parse(self, response):
        final_data = {'response': response}

        table_1_names = []
        table_1_values = []
        for i in range(1, 16):
            name = response.xpath('//*[@class="table table-bordered"]/tbody/tr[{0}]/td[1]/text()'.format(i)).extract_first()
            value = response.xpath('//*[@class="table table-bordered"]/tbody/tr[{0}]/td[2]/text()'.format(i)).extract_first()
            if name and value:
                name = name.strip()
                value = value.strip()
            table_1_names.append(name)
            table_1_values.append(value)

        final_data.update(dict(zip(table_1_names, table_1_values)))

        table_2_names = []
        table_2_values = []

        i = 1
        while True:
            name = response.xpath('//*[@data-name="additional-info"]/tbody/tr[{0}]/td[1]/text()'.format(i)).extract_first()
            value = response.xpath('//*[@data-name="additional-info"]/tbody/tr[{0}]/td[2]/text()'.format(i)).extract_first()
            if name and value:
                name = name.strip()
                value = value.strip()
            else:
                break
            table_2_names.append(name)
            table_2_values.append(value)

            i += 1

        tbl_2_dict = dict(zip(table_2_names, table_2_values))
        final_data['solution_type'] = tbl_2_dict

        table_3_names = []
        table_3_values = []

        i = 2
        while True:
            values = []
            name = response.xpath('(//*[@class="td_bord"])[{0}]/text()'.format(i)).extract_first()
            value_1 = response.xpath('(//*[@class="td_bord"])[{0}]/text()'.format(i + 1)).extract_first()
            value_2 = response.xpath('(//*[@class="td_bord"])[{0}]/text()'.format(i + 2)).extract_first()
            if name and value_1 and value_2:
                name = name.strip()
                value_1 = value_1.strip()
                value_2 = value_2.strip()
            else:
                break
            table_3_names.append(name)
            values = [value_1, value_2]
            table_3_values.append(values)

            i += 4

        table_3_dict = dict((zip(table_3_names, table_3_values)))
        final_data['branch'] = table_3_dict

        yield final_data
