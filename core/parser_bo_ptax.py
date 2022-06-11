from http import HTTPStatus

from parsel import Selector
from html_table_parser import HTMLTableParser
import re

import os, sys

from core.log import log
from api.request_ptax import RequestPTAX


class ParserBoPtax(RequestPTAX):

    @classmethod
    def _parser_quotes(cls, source_page):
        """
        We format the table found on the bacen site into a dict object and return it to the caller.
        """
        try:
            log('console').info('Parsing data.')
            parser_tables = HTMLTableParser()
            parser_tables.feed(source_page)
            bo_of_day = parser_tables.tables[0][0][0].split(' ')[-1]  # 'Boletins do dia 02/06/2022'
            # header_1 = parser_tables.tables[0][1]  # ['Hora', 'Tipo', 'Taxa 1/', 'Paridade 2/', '']
            # header_2 = parser_tables.tables[0][2]  # ['Compra', 'Venda', 'Compra', 'Venda', 'Gráfico']
            content_row = parser_tables.tables[0][3:-1]  # ['10:00', 'Abertura', '4,7955', '4,7961', '1,0000', '1,0000', '']
            data = [{'data': bo_of_day, 'hora': row[0], 'compra': row[2], 'venda': row[3]} for row in content_row]
            return data
        except BaseException as err:
            log('console').error('There was an error parsing the data')
            log('root').error(err)
            sys.exit(os.EX_DATAERR)

    def __init__(self, request_data):
        super().__init__(request_data)

        self._msg_not_found = 'Não existe informação para a pesquisa efetuada!'
        self._msg_invalid_date = 'Campo Data Inicial não é válido.'

        self._div_error = '//div[@class="msgErro"]/text()'

    def _get_ptax_quote(self, cookies):
        """
        Responsible for calling the method that takes the page containing the ptax quotes and sends it to the formatting.
        """
        source = self._get_ptax_source(cookies=cookies)
        if source is None:
            # Quote is not available
            return None

        quotes = ParserBoPtax._parser_quotes(source)
        return quotes

    def _get_ptax_source(self, cookies):
        """
        Request on bacen web site
        """
        response = self.web.post(url=self._url_ptax_daily, data=self._payload, cookies=cookies)
        #  Checks if the response was successful
        if response.status_code == HTTPStatus.OK:
            selector = Selector(response.text)
            msg_error = selector.xpath(self._div_error)
            # Checking to see if the site returned an error message.
            if msg_error.get() is None:
                log('console').info('Quotes found.')
                return response.text
            else:
                # When there are no quotes, the bacen site returns an error message.
                # Não existe informação para a pesquisa efetuada!
                if re.compile(self._msg_not_found).search(msg_error.get()):
                    # Quote is not available
                    return None
                elif re.compile(self._msg_invalid_date).search(msg_error.get()):
                    log('console').error('Enter a valid date.')
                    sys.exit(os.EX_IOERR)
                else:
                    log('console').error(msg_error.get())
                    sys.exit(os.EX_SOFTWARE)
        else:
            log('console').error(str(response.status_code))

    def start(self):
        log('console').info('Accessing the central bank website.')
        base_page = self.web.get(url=self._url_base)
        if base_page.status_code == HTTPStatus.OK:
            parsed = self._get_ptax_quote(base_page.cookies)
            return parsed
        else:
            log('console').error(f'An error occurred when trying to access the central bank website. '
                                 f'Code: {base_page.status_code}')
            log('root').error(self._url_base)
            sys.exit(os.EX_NOHOST)





