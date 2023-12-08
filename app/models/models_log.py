from .models_base import ListModelBase


class LogNewCategory(ListModelBase):
    '''Модель для лога продуктов с новой категорией.'''


class LogNotRecognized(ListModelBase):
    '''
    Модель для лога продуктов с ошибкой конвертации
    url_short -> url_long.
    '''


class LogExceptionalCategory(ListModelBase):
    '''Модель для лога продуктов с несобираемой категорией.'''


class LogNotReleased(ListModelBase):
    '''Модель для лога не релизнутых продуктов.'''
