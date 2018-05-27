import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from datracker.models import Page, Issue, IssueCategory
from datracker.enums import AuthGroupNames, IssueCategories, Pages


lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus lacinia bibendum quam id cursus. Mauris vehicula ante vel velit gravida, vel porta tortor ornare."

common_password = 'password'


class ContentTypes:
    ISSUE = ContentType.objects.get_for_model(Issue)


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
            "content": lorem_ipsum,
        },
        {
            "pk": Pages.DASHBOARD,
            "title": "Dashboard",
            "label": "Dashboard",
            "slug": "dashboard",
            "meta_title": "DaTracker - Dashboard",
            "meta_description": "Company & Tasks.",
            "content": lorem_ipsum,
        },
        {
            "pk": Pages.ISSUES,
            "title": "Issues",
            "label": "Issues",
            "slug": "issues",
            "meta_title": "DaTracker - Issues",
            "meta_description": "Check status of Issues.",
            "content": lorem_ipsum,
        },
        {
            "pk": Pages.FAQ,
            "title": "FAQ",
            "label": "FAQ",
            "slug": "faq",
            "meta_title": "DaTracker - FAQ",
            "meta_description": "Considering using DaTracker? Check this out.",
            "content": lorem_ipsum,
        },
    ]

    data_issue_category = [
        {
            "pk": IssueCategories.DEVELOPMENT,
            "name": "Development tasks",
            "description": lorem_ipsum,
        },
        {
            "pk": IssueCategories.PERSONAL,
            "name": "Personal issues",
            "description": lorem_ipsum,
        },
        {
            "pk": IssueCategories.DOCUMENTATION,
            "name": "Neccesity to write docs",
            "description": lorem_ipsum,
        },
        {
            "pk": IssueCategories.RELIGIOUS,
            "name": "Religious duty",
            "description": lorem_ipsum,
        },
        {
            "pk": IssueCategories.POLITICAL,
            "name": "Political promotion",
            "description": lorem_ipsum,
        },
    ]

    data_employees = [
        {
            "first_name": "Michael",
            "last_name": "Tucket",
            "username": "michael.tucken",
            "email": "tucken.michael@gamail.com",
        },
        {
            "first_name": "Larkin",
            "last_name": "Mooze",
            "username": "larkin.mooze",
            "email": "larkin.mooze@gamail.com",
        },
        {
            "first_name": "Salem",
            "last_name": "Machlavi",
            "username": "salem.machlavi",
            "email": "salem.machlavi@gamail.com",
        },
        {
            "first_name": "Robert",
            "last_name": "Dunick",
            "username": "robert.dunick",
            "email": "robert.dunick@gamail.com",
        },
        {
            "first_name": "Veronica",
            "last_name": "Viley",
            "username": "veronica.viley",
            "email": "veronica.viley@gamail.com",
        },
        {
            "first_name": "Martin",
            "last_name": "Summett",
            "username": "martin.summett",
            "email": "martin.summett@gamail.com",
        },
        {
            "first_name": "Charles",
            "last_name": "Wacklow",
            "username": "charles.wacklow",
            "email": "charles.wacklow@gamail.com",
        },
        {
            "first_name": "Brendan",
            "last_name": "Hickey",
            "username": "brendan.hickey",
            "email": "brendan.hickey@gamail.com",
        },
        {
            "first_name": "Joseph",
            "last_name": "Malstein",
            "username": "joseph.malstein",
            "email": "joseph.malstein@gamail.com",
        },
        {
            "first_name": "Michael",
            "last_name": "Torfu",
            "username": "michael.torfu",
            "email": "michael.torfu@gamail.com",
        },
    ]

    data_issue_names = [
        'Test C++ desktop program',
        'Make JVM documentation',
        'Repar broken chair',
        'Read cryptography manual',
        'Design architecture',
        'Analyze marketing data',
        'Install new Java version',
        'Launch web marketing campaign',
        'Add new model structure to Android App',
        'Learn Rust Language',
        'Meeting with a client',
        'Go to church and ask god for help',
        'Investigate network issues',
    ]

    issue_categories = []

    employees = []

    total_issues = 66

    data_auth_groups = {
        AuthGroupNames.EMPLOYEES: [{
            ContentTypes.ISSUE: ["close_issue"],
        }],
        AuthGroupNames.MANAGERS: [{
            ContentTypes.ISSUE: ["close_issue", "update_solved_time"]
        }],
        AuthGroupNames.CEOS: [{
            ContentTypes.ISSUE: ["close_issue", "update_solved_time"]
        }]
    }

    def _create_pages(self):

        # Pages
        Page.objects.all().delete()

        for page in self.data_page:

            new_page = Page.objects.create(**page)
            self.stdout.write(self.style.SUCCESS(
                'Page #{} {} has been succesfully created.'.format(new_page.pk, new_page.title)
            ))

    def _create_issue_categories(self):
        # Issue Categories
        IssueCategory.objects.all().delete()

        for issue_category in self.data_issue_category:

            new_category = IssueCategory.objects.create(**issue_category)
            self.issue_categories.append(new_category)
            self.stdout.write(self.style.SUCCESS(
                'IssueCategory #{} {} has been succesfully created.'.format(
                    new_category.pk, new_category.name
                )
            ))

    def _create_user_groups(self):

        Group.objects.all().delete()

        for group_name, group_permissions_list in self.data_auth_groups.items():
            group = Group.objects.create(name=group_name)

            for group_permissions in group_permissions_list:

                for permissions_content_type, permission_list in group_permissions.items():

                    for permission_name in permission_list:

                        perm = Permission.objects.get(codename=permission_name, content_type=permissions_content_type)
                        group.permissions.add(perm)

                self.stdout.write(self.style.SUCCESS(
                    'User group {} has been succesfully created.'.format(
                        group.name,
                    )
                ))

    def _create_employees(self):
        # Employees
        get_user_model().objects.all().delete()
        employee_user_group = Group.objects.get(name=AuthGroupNames.EMPLOYEES)

        for employee in self.data_employees:
            employee['is_staff'] = True
            employee['password'] = common_password
            new_employee = get_user_model().objects.create_user(**employee)
            employee_user_group.user_set.add(new_employee)
            new_employee.save()
            self.employees.append(new_employee)
            self.stdout.write(self.style.SUCCESS(
                'Employee #{} has been succesfully created. Login: {} Password: {}'.format(
                    new_employee.pk,
                    new_employee.username,
                    common_password,
                )
            ))

    def _create_superuser(self):
        # Additionally lets create a superuser
        ceos_user_group = Group.objects.get(name=AuthGroupNames.CEOS)

        new_employee = get_user_model().objects.create_superuser(**{
            'first_name': 'Marshall',
            'last_name': 'Hammond',
            'username': 'admin',
            'email': 'admin@admin.gamail',
            'password': common_password,
        })

        ceos_user_group.user_set.add(new_employee)

        self.employees.append(new_employee)
        self.stdout.write(self.style.SUCCESS(
            'Additional superuser Employee #{} has been created! Login: {} Password: {}'.format(
                new_employee.pk,
                new_employee.username,
                common_password,
            )
        ))

    def _create_issues(self):
        # Issues
        Issue.objects.all().delete()

        now = timezone.now()

        total_issue_names = []

        for i in range(self.total_issues):
            total_issue_names.append(random.choice(self.data_issue_names))

        for issue_name in total_issue_names:

            randomized_create_date = now - timedelta(
                seconds=random.randint(1, 60),
                minutes=random.randint(1, 60),
                days=random.randint(38,159),
            )

            if random.randint(1, 4) == 1:
                randomized_solved_date = None
            else:
                randomized_solved_date = now - timedelta(
                    seconds=random.randint(1, 60),
                    minutes=random.randint(1, 60),
                    days=random.randint(1,38),
                )

            new_issue = Issue.objects.create(
                name=issue_name,
                description=lorem_ipsum,
                created=randomized_create_date,
                solved=randomized_solved_date,
                category=random.choice(self.issue_categories),
                assignee=random.choice(self.employees),
            )

            new_issue.created = randomized_create_date
            new_issue.save()

            self.stdout.write(
                self.style.SUCCESS('Issue #{} {} has been succesfully generated.'.format(
                    new_issue.pk, new_issue.name
                ))
            )

    def handle(self, *args, **options):
        self._create_pages()
        self._create_issue_categories()
        self._create_user_groups() # just create it
        self._create_employees()
        self._create_superuser()
        self._create_issues()

        self.stdout.write(self.style.SUCCESS('Initial data were succesfully generated.'))