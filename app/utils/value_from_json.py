import re


def value_json(find_in, attr_to_capture, called_key=''):
    '''Получение значения из json по названию атрибута.'''
    return_value = ''
    if isinstance(find_in, dict):
        for key, value in find_in.items():
            return_value += get_internal_value(
                key, value, attr_to_capture
            )
    elif isinstance(find_in, list):
        for list_item in find_in:
            return_value += get_internal_value(
                called_key, list_item, attr_to_capture
            )
    return return_value[:-3] if return_value else ''


def get_internal_value(key, value, attr_to_capture):
    '''
    Получение внутреннего значения с рекурсивным вызовом
    функции получения значения value_json() для атрибута
    modelIdentifier и других возможных мультиатрибутов.
    '''
    internal_value = ''
    if type(value) in (dict, list):
        internal_value = value_json(value, attr_to_capture, key)
    elif key == attr_to_capture:
        internal_value = str(value)
    internal_value = re.sub('\t|  ', ' ', internal_value).strip()
    internal_value = internal_value if internal_value != 'None' else '-'
    return f'{internal_value} | ' if internal_value != '' else ''
