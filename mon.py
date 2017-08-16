#!/usr/bin/env python

import conf

import os
import smtplib
import datetime


def _bytes_to_human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i+1)*10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

def check_disk(path, threshold):
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    status = free > threshold
    return path, threshold, status, used, free, total



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
for path, threshold in conf.DISKS:
    result = check_disk(path, threshold)
    results.append(result)
    if not result[2]:
        errors.append(result)

if errors:
    message = []
    for path, threshold, status, used, free, total in errors:
        status_text = ' OK ' if status else 'WARN'
        text = '- [%s] path: %s, threshold: %s, free: %s' % (
            status_text,
            path,
            _bytes_to_human(threshold),
            _bytes_to_human(free),
        )
        message.append(text)

    message.append('')
    message.append('server: %s' % conf.HOSTNAME)
    message.append('timestamp: %s' % datetime.datetime.now().isoformat())
    message.append('')
    message.append('--')
    message.append('mon-disk, simple disk monitor <https://github.com/ondrejsika/mon-disk>')
    message = '\n'.join(message)

    print(message)
    sendmail('[mon-disk] Errors found', message)



