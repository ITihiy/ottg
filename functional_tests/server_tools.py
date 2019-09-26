from django.core.management import call_command
from io import StringIO


def reset_database():
    call_command('flush', '--noinput')


def create_session_on_server(email):
    out = StringIO()
    call_command('create_session', email, stdout=out)
    return out.getvalue().strip()