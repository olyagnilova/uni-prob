# -*- coding: utf-8 -*-
import scrapy
import ast

class AlltablesSpider(scrapy.Spider):
    name = 'alltables'
    allowed_domains = ['indicators.miccedu.ru']
    with open('vuz_ids.txt', 'r') as myfile:
        ids = ast.literal_eval(myfile.read())

    start_urls = []
    # uncomment to parse 2017 data
    # for item in ids:
    #         start_urls.append('http://indicators.miccedu.ru/monitoring/2017/_vpo/inst.php?id=' + item)

    # uncomment to parse 2018 data
    for item in ids:
        start_urls.append('http://indicators.miccedu.ru/monitoring/_vpo/inst.php?id=' + item)

    def parse(self, response):
        # Таблица 1
        name = response.xpath('(//*[@class="tt"])/following-sibling::td/b/text()').extract_first()
        address = response.xpath('(//*[@id="post"])/text()').extract_first()
        branches = len(response.xpath('(//*[@class="blockcontent"])[1]/p').extract())

        final_dict = {'name': 'Наименование образовательной организации',
                      'address': 'Адрес',
                      'branches': 'Количество филиалов'}
        final_data = {'name':  name,
                      'address': address,
                      'branches': branches,
                      'response': response}

        table_1_data = []
        table_1_names = []
        table_1_dict = []
        for i in range(3, 8):
            table_1_names.append('t1_' + str(i))
            table_1_dict.append(response.xpath('(//*[@id="info"])/tr[{0}]/td[1]/text()'.format(i)).extract_first())
            table_1_data.append(response.xpath('(//*[@id="info"])/tr[{0}]/td[2]/text()'.format(i)).extract_first())

        table_1_final = dict(zip(table_1_names, table_1_data))
        table_1_dict_final = dict(zip(table_1_names, table_1_dict))
        final_data.update(table_1_final)
        final_dict.update(table_1_dict_final)
        final_data['t1_6'] = response.xpath('(//*[@id="info"])/tr[6]/td[2]/p/text()'.format(i)).extract_first()

        # Таблица 2

        table_2_actual = []
        table_2_threshold = []
        table_2_delta = []
        table_2_actual_names = []
        table_2_threshold_names = []
        table_2_delta_names = []
        table_2_actual_dict = []
        table_2_threshold_dict = []
        table_2_delta_dict = []

        for i in range(2, 9):
            table_2_tag = response.xpath('((//*[@id="result"])/tr[{0}]/td[1]/text())'.format(i)).extract_first()
            if table_2_tag:
                table_2_actual_names.append('t2_1_' + table_2_tag)
                table_2_threshold_names.append('t2_2_' + table_2_tag)
                table_2_delta_names.append('t2_3_' + table_2_tag)
            else:
                table_2_actual_names.append('t2_1_' + 'notag')
                table_2_threshold_names.append('t2_2_' + 'notag')
                table_2_delta_names.append('t2_3_' + 'notag')
            actual = " ".join(response.xpath('((//*[@id="result"])/tr[1]/thead/td[3]/text())').extract())
            treshold =  " ".join(response.xpath('((//*[@id="result"])/tr[1]/thead/td[4]/text())').extract())
            delta =  " ".join(response.xpath('((//*[@id="result"])/tr[1]/thead/td[5]/text())').extract())
            if actual and treshold and delta:
                table_2_actual_dict.append(response.xpath('(//*[@id="result"])/tr[{0}]/td[2]/text()'.format(i)).extract_first() + ', ' + actual)
                table_2_threshold_dict.append(response.xpath('(//*[@id="result"])/tr[{0}]/td[2]/text()'.format(i)).extract_first() + ', ' + treshold)
                table_2_delta_dict.append(response.xpath('(//*[@id="result"])/tr[{0}]/td[2]/text()'.format(i)).extract_first() + ', ' + delta)
            else:
                table_2_actual_dict.append(response.xpath('(//*[@id="result"])/tr[{0}]/td[2]/text()'.format(i)).extract_first())
                table_2_threshold_dict.append(response.xpath('(//*[@id="result"])/tr[{0}]/td[2]/text()'.format(i)).extract_first())
                table_2_delta_dict.append(response.xpath('(//*[@id="result"])/tr[{0}]/td[2]/text()'.format(i)).extract_first())
            table_2_actual.append(response.xpath('(//*[@id="result"])/tr[{0}]/td[3]/span/text()'.format(i)).extract_first())
            table_2_threshold.append(response.xpath('(//*[@id="result"])/tr[{0}]/td[4]/text()'.format(i)).extract_first())
            table_2_delta.append(response.xpath('(//*[@id="result"])/tr[{0}]/td[5]/span/sup/text()'.format(i)).extract_first())

        table_2_a = dict(zip(table_2_actual_names, table_2_actual))
        table_2_t = dict(zip(table_2_threshold_names, table_2_threshold))
        table_2_d = dict(zip(table_2_delta_names, table_2_delta))

        table_2_a_dict = dict(zip(table_2_actual_names, table_2_actual_dict))
        table_2_t_dict = dict(zip(table_2_threshold_names, table_2_threshold_dict))
        table_2_d_dict = dict(zip(table_2_delta_names, table_2_delta_dict))

        final_data.update(table_2_a)
        final_data.update(table_2_t)
        final_data.update(table_2_d)

        final_dict.update(table_2_a_dict)
        final_dict.update(table_2_t_dict)
        final_dict.update(table_2_d_dict)

        # Таблица 3

        table_3_data = []
        table_3_names = []
        table_3_dict = []

        for j in range(1, 8):
            for i in range(2, 18):
                indicator = response.xpath('(//*[@class="napde"])[{0}]/tr[{1}]/td[2]/text()'.format(j, i)).extract_first()
                measure = response.xpath('(//*[@class="napde"])[{0}]/tr[{1}]/td[3]/text()'.format(j, i)).extract_first()
                if measure and indicator:
                    table_3_dict.append(indicator + ', ' + measure)
                else:
                    table_3_dict.append(indicator)
                tmp_dict_3 = dict(zip(table_3_names, table_3_dict))
                final_dict.update(tmp_dict_3)

                table_3_names.append(response.xpath('(//*[@class="napde"])[{0}]/tr[{1}]/td[1]/text()'.format(j, i)).extract_first())
                table_3_data.append(response.xpath('(//*[@class="napde"])[{0}]/tr[{1}]/td[4]/text()'.format(j, i)).extract_first())
                tmp_table_3 = dict(zip(table_3_names, table_3_data))
                final_data.update(tmp_table_3)

        # Таблица 4

        table_41_data = []
        table_41_names = []

        for i in range(4, 8):
            table_41_names.append('t4_1_' + str(i - 3))
            table_41_data.append(response.xpath('(//*[@class="val"])[{0}]/text()'.format(i)).extract_first())

        table_41_final = dict(zip(table_41_names, table_41_data))
        final_data.update(table_41_final)

        table_42_data = []
        table_42_names = []
        table_43_data = []
        table_43_names = []

        for i in range (1, 9):
            table_42_names.append('t4_2_' + str(i))
            table_43_names.append('t4_3_' + str(i))
            table_42_data.append(response.xpath('(//*[@id="kont_by_otr"])/tr[{0}]/td[2]/*/*/*/text()'.format(i)).extract_first())
            table_43_data.append(response.xpath('(//*[@id="kont_by_otr"])/tr[{0}]/td[3]/span/text()'.format(i)).extract_first())

        table_42_final = dict(zip(table_42_names, table_42_data))
        table_43_final = dict(zip(table_43_names, table_43_data))
        final_data.update(table_42_final)
        final_data.update(table_43_final)

        table_44_data = []
        table_44_names = []
        table_44_dict = []

        for i in range(2, 23):
            for j in range(2, 5):
                # поправить УГН(С)
                program = response.xpath('(//*[@id="analis_reg"])/tr[{0}]/td[1]/text()'.format(i)).extract_first()
                indicator = " ".join(response.xpath('(//*[@id="analis_reg"])/thead/tr[1]/td[{0}]/text()'.format(j)).extract())
                if program and indicator:
                    table_44_dict.append(program + ', ' + indicator)
                    table_44_names.append('t4_4_' + program.split(" ")[0] + '_' + str(j - 1))
                else:
                    table_44_dict.append('notag')
                    table_44_names.append('t4_4_notag_' + str(j - 1))
                table_44_data.append(response.xpath('(//*[@id="analis_reg"])/tr[{0}]/td[{1}]/text()'.format(i, j)).extract_first())

        table_44_final_dict = dict(zip(table_44_names, table_44_dict))
        table_44_final = dict(zip(table_44_names, table_44_data))
        final_data.update(table_44_final)
        final_dict.update(table_44_final_dict)

        # Таблица 5

        table_5_data = []
        table_5_names = []
        table_5_dict = []

        for i in range(2, 66):
            table_5_names.append('t5_' + str(i - 1))
            indicator = response.xpath('(//*[@id="analis_dop"])/tr[{0}]/td[2]/text()'.format(i)).extract_first()
            measure = response.xpath('(//*[@id="analis_dop"])/tr[{0}]/td[3]/text()'.format(i)).extract_first()
            if indicator and measure:
                table_5_dict.append(indicator + ', ' + measure)
            else:
                table_5_dict.append(indicator)
            table_5_data.append(response.xpath('(//*[@id="analis_dop"])/tr[{0}]/td[4]/text()'.format(i)).extract_first())

        table_5_final = dict(zip(table_5_names, table_5_data))
        table_5_dict_final = dict(zip(table_5_names, table_5_dict))
        final_data.update(table_5_final)
        final_dict.update(table_5_dict_final)

        yield final_data
        #yield final_dict
