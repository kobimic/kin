# kin
this is a kin api demo written with flask,peewee(and sqlite),marshmallow,aargon, for registering users, verifying users, sending sms messages and viewing sms history

1) in order to run this you need an account in nexmo
2) export the following env paramters

`export NEXMO_API_KEY=<your nexmo api key>`
`export NEXMO_API_SECRET=<your nexmo api secret>`

3) there is an optional seed key used for hashing , you can skip it for now
`export SECRET_KEY=<your random letters and number to be used as seed>`
4) use virtual and activate it 
`virtualenv venv;source venv/bin/activate`
5) install dependencies
`pip install -r requirements.txt `
6) run the flask app
`python app.py`

you can use one of the 5 endpoints
for registering new users :
POST: http://127.0.0.1:8000/api/v1/users/register 

for verifying new users :
POST: http://127.0.0.1:8000/api/v1/users/verify

for sending sms messages :
POST: http://127.0.0.1:8000/api/v1/users/send

for viewing sms history
GET: http://127.0.0.1:8000/api/v1/users/messages

for viewing user current status
GET: http://127.0.0.1:8000/api/v1/users/info

