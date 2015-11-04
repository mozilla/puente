from django.shortcuts import render

from django.utils.translation import ugettext as _
from django.utils.translation import ngettext, pgettext


def index_view(request):
    return render(request, 'base/index.html')


def jingo_view(request):
    num = 2

    return render(request, 'base/jingo_page.html', {
        'title': _('This is a title'),
        'nstring': ngettext('%(num)s apple', '%(num)s apples', num) % {'num': num},
        'pstring': pgettext('sidebar', 'Click me')
    })


def django_view(request):
    num = 2

    return render(request, 'admin/django_page.html', {
        'title': _('This is a title'),
        'nstring': ngettext('%(num)s apple', '%(num)s apples', num) % {'num': num},
        'pstring': pgettext('sidebar', 'Click me')
    })
