# kin
this is a kin api demo written with flask,peewee(and sqlite),marshmallow,aargon, for registering users, verifying users, sending sms messages and viewing sms history

## design thoughts:
- the design idea was that each user belongs to a plan(like student, private(regular), team, company...) that contains the sms cost per message, and the initial credit for that plan.
- each user being created have a FK to a plan(in this demo they all belong to a "regular" which is being created on the first request thanks to defaults), and the initial credit is copied from that plan to his/her user record to be used
this allows to change the plan sms cost for all the plan users, with out updating all the users
- after the user is being verfied, he/she can send sms messages with the cost specified in the user plan 
- and the user can also see its list of messages(content and date) and also its details+current balance

## how to run
1) in order to run this **you need an account in nexmo**
2) export the following env paramters

`export NEXMO_API_KEY=<your nexmo api key>`
`export NEXMO_API_SECRET=<your nexmo api secret>`

3) there is an optional seed key used for hashing , but you can skip it for now

`export SECRET_KEY=<your random letters and number to be used as seed>`

4) **use virtual and activate it **
`virtualenv venv;source venv/bin/activate`
5) **install dependencies**
`pip install -r requirements.txt `
6) **run the flask app**
`python app.py`

## available endpoints
you can use one of the 5 endpoints
###### for registering new users :
POST: http://127.0.0.1:8000/api/v1/users/register 

###### for verifying new users :
POST: http://127.0.0.1:8000/api/v1/users/verify

###### for sending sms messages :
POST: http://127.0.0.1:8000/api/v1/users/send

###### for viewing sms history
GET: http://127.0.0.1:8000/api/v1/users/messages

###### for viewing user current status
GET: http://127.0.0.1:8000/api/v1/users/info




