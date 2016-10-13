#!/usr/bin/env python

import conf

import smtplib
import datetime

import requests


def check(url):
    try:
        r = requests.get(url)
        if r.status_code < 400:
            return url, True, r.status_code
        return url, False, r.status_code
    except requests.RequestException:
        return url, False, None


def _sendmail(email_from, email_to, message, username, password, server, tls):
    server = smtplib.SMTP(server)
    if tls:
        server.starttls()
    server.login(username, password)
    server.sendmail(email_from, email_to, message)
    server.quit()


def sendmail(subject, message):
    message = 'Subject: %s\nFrom: %s\n\n%s' % (subject, conf.EMAIL_FROM, message)
    return _sendmail(conf.EMAIL_FROM,
                     conf.EMAIL_TO,
                     message,
                     conf.SMTP_USERNAME,
                     conf.SMTP_PASSWORD,
                     conf.SMTP_SERVER,
                     conf.SMTP_TLS)


results = []
errors = []
for url in conf.URLS:
    result = check(url)
    results.append(result)
    if not result[1]:
        errors.append(result)

if errors:
    message = []
    for url, error, status_code in errors:
        status_code = status_code if status_code else '   '
        message.append('- [%s] %s' % (status_code, url))

    message.append('')
    message.append('server: %s' % conf.HOSTNAME)
    message.append('timestamp: %s' % datetime.datetime.now().isoformat())
    message.append('')
    message.append('--')
    message.append('mon, simple website monitor <https://github.com/ondrejsika/mon>')
    message = '\n'.join(message)

    print(message)
    sendmail('[mon] Errors found', message)



