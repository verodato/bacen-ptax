#!/usr/bin/env python
import os
from datetime import datetime

import argparse
import json

from core.parser_bo_ptax import ParserBoPtax
from core.log import log
from core.utils import countdown


def get_argument():
    """
    Function responsible for setting and taking the --time argument passed via cli. The argument is required for the
    script to run.

    E.g python3 main.py -t '10:00'
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-t', '--time', help='Set an time (E.g hh:mm)', required=True)
    args = arg_parser.parse_args()
    if args.time:
        return args.time


def main():
    print('Started ptax main')
    _request_data = datetime.today().strftime('%d/%m/%Y')
    # _request_data = '04/06/2022'  # test
    # Initialization of the class responsible for returning a json object containing the ptax quotes
    pbop = ParserBoPtax(request_data=_request_data)

    # We get out of the loop whenever a new quote is found and posted.
    while True:
        quotes_ptax = pbop.start()

        if quotes_ptax is None:
            log('console').info('There are no quotes for that date.')
        else:
            # To check if we are getting a new quote from ptax we compare the time in the last line of the object with
            # the time passed as argument in the execution of the script started by crontab.
            if quotes_ptax[-1].get('hora') >= get_argument():
                log('console').info('A new quote has been found.')
                # Output json file
                try:
                    log('console').info('Saving quotes in output/quotes.json')
                    to_json = json.dumps(quotes_ptax)
                    with open(os.path.abspath(os.path.join(os.path.dirname(__file__)))+'/output/quotes.json', 'w') as f:
                        f.write(to_json)
                    log('console').info('Done.')
                except BaseException as err:
                    log('console').error(f'An error occurred while trying to save the file in json format. \n {err}')
                finally:
                    break
            else:
                log('console').info('No new quotes found.')
        countdown(300)  # 5 min


if __name__ == '__main__':
    log('console').info('Initializing...')
    main()
