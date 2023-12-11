import argparse
from datetime import datetime


parser = argparse.ArgumentParser(description='EPREL scraper')

group = parser.add_mutually_exclusive_group()
group.add_argument(
    '-m',
    '--mode',
    help=(
        'Parsing mode: '
        'remaining = all in range except parsed, exceptional '
        'and not released yet (default mode); '
        'not_collected = the same as remaining + not released; '
        'all = all in range; '
        'pdf = collect PDFs for parsed products'
    ),
    choices=['remaining', 'not_collected', 'all', 'pdf'],
    default='remaining',
)
group.add_argument(
    '-pc',
    '--pdf_commit',
    help=(
        'Add PDF commit. Value should be in "YYYY-MM-DD HH:MM:SS.mmmmmm" '
        'format. '
        'If there is no value posted, current time commit will be added'
    ),
    nargs='?',
    const=str(datetime.now()),
)
group.add_argument(
    '-pcl',
    '--pdf_commit_list',
    help='Show N latest PDF commits (default: 10)',
    type=int,
    nargs='?',
    const=10,
)
group.add_argument(
    '-pcr',
    '--pdf_commit_remove',
    help=('Remove N latest PDF commits (default: 1)'),
    type=int,
    nargs='?',
    const=1,
)

parser.add_argument(
    '-pcf',
    '--pdf_commit_from',
    help=(
        'PDF commit from - starting commit (see PDF commit list for '
        'appropriate value). To be used together with PDF mode '
    ),
    type=int,
    nargs='?',
    const=0,
)
parser.add_argument(
    '-pct',
    '--pdf_commit_to',
    help=(
        'PDF commit to - finishing commit (see PDF commit list for '
        'appropriate value). To be used together with PDF mode '
    ),
    type=int,
    nargs='?',
    const=0,
)

command_line_args = parser.parse_args()
