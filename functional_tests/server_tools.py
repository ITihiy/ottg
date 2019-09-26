import sys
from django.core.management import call_command
from io import StringIO


def reset_database():
    call_command('flush', '--noinput')


def create_session_on_server(email):
    print('create_session_on_server', file=sys.stderr)
    out = StringIO()
    call_command('create_session', email, stdout=out)
    key = out.getvalue().strip()
    print('key:', key, file=sys.stderr)
    return key