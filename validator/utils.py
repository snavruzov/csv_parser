import re
import smtplib
import dns.resolver

class EmailCheck:
    _address = None
    _mx_record = None

    _regex = r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'

    # Address used for SMTP MAIL FROM command
    def __init__(self, email):
        self._address = email

    def syntax_check(self):
        # Syntax check
        match = re.match(self._regex, self._address)
        if match is None:
            return 'NO'
        return 'OK'

    def mx_smtp_check(self):
        smtp_ok = 'OK'
        mx_ok = 'OK'
        # Get domain for DNS lookup
        split_address = self._address.split('@')
        domain = str(split_address[1])
        print('Domain: ' + domain)

        # MX record lookup
        try:
            records = dns.resolver.query(domain, 'MX')
            mx_record = records[0].exchange
            self._mx_record = str(mx_record)
        except dns.exception.DNSException:
            mx_ok = 'NO'
        else:
            print(mx_record)
            smtp_ok = self._smtp_check()

        return mx_ok, smtp_ok

    def _smtp_check(self):
        # SMTP lib setup (use debug level for full output)
        smtp_ok = 'OK'
        try:
            server = smtplib.SMTP(timeout=10)
            server.set_debuglevel(0)

            # SMTP Conversation
            server.connect(self._mx_record)
            status, _ = server.helo()
            print(status)
            if status != 250:
                server.quit()
                smtp_ok = 'NO'

            server.mail('')
            status, message = server.rcpt(str(self._address))

            server.quit()

            print(status)
            print(message)

            # Assume SMTP response 250 is success
            if status != 250:
                smtp_ok = 'NO'

        except smtplib.SMTPServerDisconnected:  # Server not permits verify user
            smtp_ok = 'NO'
        except smtplib.SMTPConnectError:
            smtp_ok = 'NO'

        return smtp_ok
