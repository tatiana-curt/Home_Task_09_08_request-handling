# import datetime
import os
from datetime import datetime
from app.settings import FILES_PATH
from django.shortcuts import render


def file_list(request, date=None):
    # Не хватает логики для фильтрации.
    template_name = 'index.html'

    context = {
        'files': []
    }

    if date != None:
        context['date'] = datetime.fromisoformat(date).date()

    for dir in os.listdir(path=FILES_PATH):
        ctime = os.stat(f'{FILES_PATH}\{dir}').st_ctime
        mtime = os.stat(f'{FILES_PATH}\{dir}').st_mtime

        file_info_dict = {'name': dir,
                          'ctime': datetime.fromtimestamp(ctime).date(),
                          'mtime': datetime.fromtimestamp(mtime).date()}
        context['files'].append(file_info_dict)

    return render(request, template_name, context)


def file_content(request, name):
    file_name_path = f'{FILES_PATH}\{name}'
    with open(file_name_path, encoding='utf-8') as f:
        return render(request,'file_content.html', context={'file_name': name,
                                                        'file_content': f.read()})


# Вопросы:
#
# 1. При вводе в поисковой строкее URL-а формата http://127.0.0.1:8000/2018-01-01/
# вывадится кнопка с фильтром, но фильтрации по дате не происходит, как сделать непонимаю.
# Также перестает выводиться информации в полях "Создан" "Изменен"

