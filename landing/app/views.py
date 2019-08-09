from collections import Counter

from django.shortcuts import render_to_response
from django.http import HttpResponse

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    index = request.GET.get('from-landing', 'Введите параметр ab-test-arg')
    if index == 'original':
        counter_click['original_click'] += 1
        print(counter_click)

    if index == 'test':
        counter_click['test_click'] += 1
        print(counter_click)
    return render_to_response('index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    ab_test_arg = request.GET.get('ab-test-arg', 'Введите параметр ab-test-arg')

    if ab_test_arg == 'original':
        counter_show['original_show'] += 1
        print(counter_show)
        return render_to_response('landing.html')
    elif ab_test_arg == 'test':
        counter_show['test_show'] += 1
        print(counter_show)
        return render_to_response('landing_alternate.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    test_conversion = counter_click['test_click']/counter_show['test_show']
    original_conversion = counter_click['original_click'] / counter_show['original_show']

    # Для вывода результат передайте в следующем формате:
    return render_to_response('stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })
