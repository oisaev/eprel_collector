from datetime import datetime

from prettytable import PrettyTable

from core.arg_parser import command_line_args
from core.logging import logger
from utils.db import (
    get_pdf_commit_list_db,
    remove_pdf_commits_db,
    save_pdf_commit_db,
)


async def pdf_commit_handler():
    '''
    Обработчик функционала PDF commit'ов:
    - вывода списка
    - создания
    - удаления
    '''
    if (
        command_line_args.pdf_commit_list is not None
        and command_line_args.pdf_commit_list >= 1
    ):
        commits = await get_pdf_commit_list_db(
            command_line_args.pdf_commit_list
        )
        print_commits_list(commits)
    elif (
        command_line_args.pdf_commit_list is not None
        and command_line_args.pdf_commit_list < 1
    ):
        logger.warning('pdf_commit_list value should be >= 1')

    elif command_line_args.pdf_commit is not None:
        try:
            date_time = datetime.fromisoformat(command_line_args.pdf_commit)
        except ValueError:
            logger.warning(
                'pdf_commit value should be "YYYY-MM-DD HH:MM:SS.mmmmmm"'
            )
        else:
            await save_pdf_commit_db(date_time)
            logger.info(f'Added {date_time} PDF commit')

    elif (
        command_line_args.pdf_commit_remove is not None
        and command_line_args.pdf_commit_remove >= 1
    ):
        removed = await remove_pdf_commits_db(
            command_line_args.pdf_commit_remove
        )
        logger.info(f'Removed {removed} PDF commit(s)')
    elif (
        command_line_args.pdf_commit_remove is not None
        and command_line_args.pdf_commit_remove < 1
    ):
        logger.warning('pdf_commit_remove value should be >= 1')


def print_commits_list(commits):
    '''Вывод списка PDF commit'ов на экран.'''
    if not commits:
        print('No commits found')
    else:
        table = PrettyTable()
        table.field_names = ['Commit ID', 'Commit DateTime']
        for id, commit in enumerate(commits):
            table.add_row([id + 1, commit])
        print(table)


async def check_from_to_args_correctness():
    '''Проверка корректности аргументов pdf_commit_from и pdf_commit_to.'''
    from_val = command_line_args.pdf_commit_from
    to_val = command_line_args.pdf_commit_to
    if (
        from_val is not None or to_val is not None
    ) and command_line_args.mode != 'pdf':
        logger.warning(
            'pdf_commit_from and pdf_commit_to arguments should be used only '
            'with pdf mode'
        )
    elif (from_val is not None and from_val < 1) or (
        to_val is not None and to_val < 1
    ):
        logger.warning('pdf_commit_from/pdf_commit_to should be >= 1')
    elif from_val is None and to_val is not None:
        logger.warning("pdf_commit_to can't be without pdf_commit_from")
    elif from_val is not None and to_val is not None and from_val < to_val:
        logger.warning('pdf_commit_from should be >= pdf_commit_to')
    else:
        return True
