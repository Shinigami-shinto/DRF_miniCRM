# Mini-CRM
Building a mini-version of a CRM system in Django and DRF

## Usage & Examples
Add Some objects or use the provided db.sqlite3
Make a venv, activate it and install the requirements via pip

Make a superuser
Run a local server `python3 manage.py runserver`

example API call to check for unpaid invoices: curl http://127.0.0.1:8000/leads/unpaid-invoices/\<user\_id\>/ | python -m 'json.tool'
Make sure to replace the user\_id by an the id of the user you would like to check

There's Throttling implemented
exmple to showcase the throtling;
`for i in {0..11}; do   curl localhost:8000/leads/unpaid-invoices/2/ | jq; sleep 0.5; done`


