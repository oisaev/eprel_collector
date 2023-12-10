import argparse


arg_parser = argparse.ArgumentParser(description='EPREL scraper')
arg_parser.add_argument(
    '-m',
    '--mode',
    help=(
        'parsing mode: '
        'remaining = all in range except parsed, exceptional '
        'and not released yet (default mode); '
        'not_collected = the same as remaining + not released; '
        'all = all in range'
    ),
    choices=['remaining', 'not_collected', 'all']
)
command_line_args = arg_parser.parse_args()
