from django.urls import reverse
from datracker.models import Page


def navbar_menu(request):

    pages = Page.objects.all().order_by('pk')

    output = [{'label': page.label, 'url': page.get_absolute_url()} for page in pages if page.can_be_seen_by(request.user)]

    if request.user.is_authenticated:
        output.append({'label': 'Logout', 'url': reverse('logout')})
    else:
        output.append({'label': 'Login', 'url': reverse('login')})

    return {'navbar_links': output}
