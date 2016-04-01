#!/usr/bin/env python
# Description: Script for resetting Jira password
# Author: Artyom Krilov <oryades@gmail.com>

import requests
import argparse
import os
import sys
from random import choice


# characters set for temporary password generation
char_set = {
    'small': 'abcdefghijklmnopqrstuvwxyz',
    'nums': '0123456789',
    'big': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'special': '~!@#$%^&*'
}


def generate_pass(length=24):
    """Function to generate a password"""

    password = []

    while len(password) < length:
        key = choice(char_set.keys())
        a_char = os.urandom(1)
        if a_char in char_set[key]:
            if check_prev_char(password, char_set[key]):
                continue
            else:
                password.append(a_char)
    return ''.join(password)


def check_prev_char(password, current_char_set):
    """Function to ensure that there are no consecutive
    UPPERCASE/lowercase/numbers/special-characters."""

    index = len(password)
    if index == 0:
        return False
    else:
        prev_char = password[index - 1]
        if prev_char in current_char_set:
            return True
        else:
            return False


def reset_password(username, password, rest_url):
    """Change current password with random password 5 times,
    then restore the original"""

    url = rest_url
    current_password = password

    # reset password 5 times with temp password
    for i in range(0,5):
        new_password = generate_pass()

        r = requests.put(url, auth=(username, current_password), json={"password": new_password, "currentPassword": current_password})
        if r.status_code == 204:
            print 'Success, temporarily changed to "{}"'.format(new_password)
        else:
            print 'Failed changing to "{}", current password is "{}", ({}), exiting...'.format(new_password, r.text)
            sys.exit(1)

        current_password = new_password

    # reset password to original
    new_password = password
    
    r = requests.put(url, auth=(username, current_password), json={"password": new_password, "currentPassword": current_password})
    if r.status_code == 204:
        print 'Success, password reset to original'
    else:
        print 'Failed changing to original, current password is "{}", ({}), exiting...'.format(current_password, r.text)
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script for resetting Jira password")
    parser.add_argument('--username')
    parser.add_argument('--password')
    parser.add_argument('--rest-url')
    args = parser.parse_args()
    if args.username and args.password and args.rest_url:
        reset_password(args.username, args.password, args.rest_url)
    elif os.environ.get('JIRA_USERNAME') and os.environ.get('JIRA_PASSWORD') and args.rest_url:
        reset_password(os.environ.get('JIRA_USERNAME'), os.environ.get('JIRA_PASSWORD'), args.rest_url)
    else
        print 'Missing arguments'
        sys.exit(1)
