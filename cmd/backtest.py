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
  parser.add_argument('-i', '--interval', default=[], help="data granularity for test" )
  parser.add_argument('-s', '--strategy', default='openbreakout', help="the strategy" )
  parser.add_argument('-t', '--ticker', default=[], help="the ticker symbol" )
  return parser

def main(args):
  logger.info('pytrader backtest')
  logger.debug(args)

  args_str=""
  for arg in vars(args):

    if arg == 'subcommand':
      continue

    if arg == 'strategy':
      continue

    if arg == 'verbose':
      if getattr(args, arg) == True:
        args_str = args_str + f"--{arg}"
      else:
        continue

    args_str = args_str + f"--{arg} {getattr(args, arg)} "


  cmd = f'python backtest/{args.strategy}.py {args_str}'
  os.system(cmd)


