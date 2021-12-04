from datetime import datetime, time

import pytz

from config import servertz


def import_text(text):  # Функция забирает текст из сообщения
    result = get_clear_text(text)
    if result == '':
        return 'null'
    return result
