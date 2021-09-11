# -*- coding: utf-8 -*-

import os
from pytrader.log import logger

"""
  backtest strategy runner
  ------
  execute selected strategy script
"""


def argparser(subparser):
  parser = subparser.add_parser('backtest')
  parser.add_argument('-s', '--strategy', default='openbreakout', help="the strategy" )
  parser.add_argument('-t', '--ticker', default=[], help="the ticker symbol" )
  return parser

def main(args):
  logger.debug('pytrader backtest')
  logger.debug(args)
  os.system(f'python backtest/{args.strategy}.py')


