import argparse
from datetime import datetime


arg_parser = argparse.ArgumentParser(description='EPREL scraper')
arg_parser.add_argument(
    '-m',
    '--mode',
    help=(
        'parsing mode: '
        'remaining = all in range except parsed, exceptional '
        'and not released yet (default mode); '
        'not_collected = the same as remaining + not released; '
        'all = all in range; '
        'pdf = collect PDFs for parsed products'
    ),
    choices=['remaining', 'not_collected', 'all', 'pdf'],
    default='remaining'
)
arg_parser.add_argument(
    '-pc',
    '--pdf_commit',
    help=(
        'add PDF commit. Value should be in "YYYY-MM-DD HH:MM:SS.mmmmmm" '
        'format. '
        'If there is no value posted, current time commit will be added'
    ),
    nargs='?',
    const=str(datetime.now())
)
command_line_args = arg_parser.parse_args()
