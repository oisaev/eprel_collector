from datetime import datetime

from prettytable import PrettyTable

from core.arg_parser import command_line_args
from core.logging import logger
from utils.db import get_pdf_commit_list, remove_pdf_commits, save_pdf_commit


async def pdf_commit_handler():
    if (command_line_args.pdf_commit_list is not None and
            command_line_args.pdf_commit_list >= 1):
        commits = await get_pdf_commit_list(command_line_args.pdf_commit_list)
        print_commits_list(commits)
    elif (command_line_args.pdf_commit_list is not None and
            command_line_args.pdf_commit_list < 1):
        logger.warning('pdf_commit_list value should be >= 1')

    elif command_line_args.pdf_commit is not None:
        try:
            date_time = datetime.fromisoformat(command_line_args.pdf_commit)
        except ValueError:
            logger.warning(
                'pdf_commit value should be "YYYY-MM-DD HH:MM:SS.mmmmmm"'
            )
        else:
            await save_pdf_commit(date_time)
            logger.info(f'Added {date_time} PDF commit')

    elif (command_line_args.pdf_commit_remove is not None and
            command_line_args.pdf_commit_remove >= 1):
        removed = await remove_pdf_commits(command_line_args.pdf_commit_remove)
        logger.info(f'Removed {removed} PDF commit(s)')
    elif (command_line_args.pdf_commit_remove is not None and
            command_line_args.pdf_commit_remove < 1):
        logger.warning('pdf_commit_remove value should be >= 1')


def print_commits_list(commits):
    if not commits:
        print('No commits found')
    else:
        table = PrettyTable()
        table.field_names = ['Commit ID', 'Commit DateTime']
        for id, commit in enumerate(commits):
            table.add_row([id+1, commit])
        print(table)
