from django.core import mail
from selenium.webdriver.common.keys import Keys
import re
import os
import time
import urllib3
from exchangelib import Credentials, Account, DELEGATE, Configuration
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter

from .base import FunctionalTest


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):
    def test_can_get_email_link_to_log_in(self):
        # Edith goes to the awesome superlists site
        # and notices a "Log in" section in the navbar for the first time
        # It's telling her to enter her email address. so she does
        test_email = os.environ.get('EXCH_HOST_USER') if self.staging_server else 'edith@example.com'

        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(test_email)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # A message appears telling her an email has been sent
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))

        # She checksher email and finds a message
        body = self.wait_for_email(test_email, SUBJECT)

        # It has a url link in it
        self.assertIn('Use this link to log in', body)
        url_search = re.search(r'http://.+/.+$', body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # She clocks it
        self.browser.get(url)

        # She is logged in
        self.wait_to_be_logged_in(email=test_email)

        # Now she logs out
        self.browser.find_element_by_link_text('Log out').click()

        # She is logged out
        self.wait_to_be_logged_out(email=test_email)

    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body
        email_id = None
        start_time = time.time()
        try:
            creds = Credentials(username=os.environ.get('EXCH_HOST_USER'), password=os.environ.get('EXCH_HOST_PASS'))
            config = Configuration(server=os.environ.get('EXCH_HOST'), credentials=creds)
            acc = Account(primary_smtp_address=os.environ.get('EXCH_HOST_USER'), autodiscover=False, config=config,
                      access_type=DELEGATE, )
        except:
            self.fail('Exchange account improperly configured')
        try:
            while time.time() - start_time < 60:
                for message in acc.inbox.all().order_by('-datetime_received')[:10]:
                    if message.subject == subject:
                        email_id = message
                        return message.body
                acc.inbox.refresh()
        finally:
            if email_id:
                email_id.delete()
