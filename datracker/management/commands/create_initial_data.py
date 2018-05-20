from django.core.management.base import BaseCommand, CommandError
from datracker.models import Employee, Page

from datracker.enums import Pages


class Command(BaseCommand):
    help = 'This command wipes DB and creates initial data again.' \
           'This command is Dangerous, may cause a data-loss. Use with care.'

    data_page = [
        {
            "pk": Pages.ABOUT,
            "title": "What is DaTracker?",
            "label": "About",
            "slug": "about",
            "meta_title": "What is DaTracker?",
            "meta_description": "Wold-class company-management app. Track performance of your employees now!",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus lacinia bibendum quam id cursus. Mauris vehicula ante vel velit gravida, vel porta tortor ornare.",
        },
        {
            "pk": Pages.DASHBOARD,
            "title": "Dashboard",
            "label": "Dashboard",
            "slug": "dashboard",
            "meta_title": "DaTracker - Dashboard",
            "meta_description": "Company & Tasks.",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus lacinia bibendum quam id cursus. Mauris vehicula ante vel velit gravida, vel porta tortor ornare.",
        },
        {
            "pk": Pages.ISSUES,
            "title": "Issues",
            "label": "Issues",
            "slug": "issues",
            "meta_title": "DaTracker - Issues",
            "meta_description": "Check status of Issues.",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus lacinia bibendum quam id cursus. Mauris vehicula ante vel velit gravida, vel porta tortor ornare.",
        },
        {
            "pk": Pages.FAQ,
            "title": "FAQ",
            "label": "FAQ",
            "slug": "faq",
            "meta_title": "DaTracker - FAQ",
            "meta_description": "Considering using DaTracker? Check this out.",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus lacinia bibendum quam id cursus. Mauris vehicula ante vel velit gravida, vel porta tortor ornare.",
        },
    ]

    def handle(self, *args, **options):

        Page.objects.all().delete()

        for page in self.data_page:

            new_page = Page.objects.create(**page)
            self.stdout.write(self.style.SUCCESS(
                'Page #{} {} has been succesfully created.'.format(new_page.pk, new_page.title)
            ))

        # raise CommandError('Command failed does not exist')

        self.stdout.write(self.style.SUCCESS('Initial data were succesfully generated.'))