# import datetime
import os
from datetime import datetime
from app.settings import FILES_PATH
from django.shortcuts import render


def file_list(request, date=None):

    template_name = 'index.html'

    context = {
        'files': [],
        'date': None,
    }

    if date != None:
        context['date'] = datetime.fromisoformat(date).date()
    print(context['date'])

    for dir in os.listdir(path=FILES_PATH):
        ctime = os.stat(f'{FILES_PATH}\{dir}').st_ctime
        mtime = os.stat(f'{FILES_PATH}\{dir}').st_mtime

        file_info_dict = {'name': dir,
                          'ctime': datetime.fromtimestamp(ctime).date(),
                          'mtime': datetime.fromtimestamp(mtime).date()}
        if context['date'] != None and (context['date'] <= file_info_dict['ctime']):
            context['files'].append(file_info_dict)

        elif context['date'] == None:
            context['files'].append(file_info_dict)

    return render(request, template_name, context)


def file_content(request, name):
    file_name_path = f'{FILES_PATH}\{name}'

    if os.path.isfile(file_name_path) == True:
        with open(file_name_path, encoding='utf-8') as f:
            return render(request,'file_content.html', context={'file_name': name,
                                                                'file_content': f.read()})


# Вопросы:
# #
# # 1. Перестает выводиться информации в полях "Создан" "Изменен"


