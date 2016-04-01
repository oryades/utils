# Description
Ever had an issue of resetting Jira password, but it doesn't allow you to set the same one? Depending on policy, you can not use last 5 passwords either? This script will reset it using 5 temporary passwords.

# Usage
`JIRA_USERNAME='username' JIRA_PASSWORD='password' python reset_jira_password.py --rest-url='url'`

or

`python reset_jira_password.py --username='username' --password='password' --rest-url='url'`
