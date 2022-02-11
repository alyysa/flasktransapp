
from flask import Flask , request, jsonify
import datetime
import psycopg2 

conn = psycopg2.connect(
   database="d7gpfa7i9lr84k", user='vdieznrdbkpvdv', password='9f32270e23791dd9cf109506fc3d3b2fed07ec9f6d758285a69db4693bb7ad4e', host='ec2-52-30-133-191.eu-west-1.compute.amazonaws.com', port= '5432'
)

app = Flask(__name__)

def validate1(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d-%m-%y')
    except ValueError:
        return False
    return True

def validate2(date_text):
    try:
        datetime.datetime.strptime(date_text, '%d-%b-%y')
    except ValueError:
        print(date_text)
        print("not working")
        return False
    return True
def generatePayload(data):
    obj = {}
    obj['Account Number'] = data[1]
    obj['Value Date'] = data[2]
    obj['Comment'] = data[3]
    obj['Trans Date'] = data[4]
    obj['Withraw Amount'] = data[5]
    obj['Deposit Amount'] = data[6]
    obj[' Balance Amount'] = data[7]
    return obj
@app.route('/')
def index():
  return '<h1>I want to Deploy Flask to Heroku</h1>'
#@app.route('/', defaults={'date': None})
@app.route('/<date>' , methods=['GET'])
def date(date):
    print(date)
    if not date:
        return "Please Enter a date in DD-MM-YY Format"
    if validate1(date):
        cursor = conn.cursor()
        query = "select * from transactiondata.transaction_log where value_date = TO_TIMESTAMP('"+date+"','DD-MM-YY');"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        if not data:
            return "No transactions Found"
        payload = []
        for i in data:
            payload.append(generatePayload(i))

        return jsonify(payload)

    else:
        return "Incorrect data format, should be DD-MM-YY"
    
@app.route('/balance/', defaults={'date': None})
@app.route('/balance/<date>' , methods=['GET'])
def balace_details(date):
    print(date)
    if not date:
        return "Please Enter a date in DD-MM-YY Format"
    if validate1(date):
        cursor = conn.cursor()
        query = "select bal_amt from transactiondata.transaction_log where value_date = TO_TIMESTAMP('"+date+"','DD-MM-YY');"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        if not data:
            return "No transactions Found"
        payload = {"balance" : data[0][0]}
        return jsonify(payload)
    else:
        return "Incorrect data format, should be DD-MM-YY"
@app.route('/details/', defaults={'date': None})
@app.route('/details/<date>' , methods=['GET'])
def date_details(date):
    print(date)
    if not date:
        return "Please Enter a date in DD-MM-YY Format"
    if validate1(date):
        cursor = conn.cursor()
        query = "select tran_details from transactiondata.transaction_log where value_date = TO_TIMESTAMP('"+date+"','DD-MM-YY');"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        if not data:
            return "No transactions Found"
        payload = {"Transaction Details" : data[0][0]}
        return jsonify(payload)
    else:
        return "Incorrect data format, should be DD-MM-YY"

@app.route('/add' , methods=['POST'])
def date_deta():
    content = request.json
    print(content)
    if not content['Account No']:
        return "Please Enter Account number"
    if not validate2(content['Date'].replace(' ','-')) or not validate2(content['Value Date'].replace(' ','-')):
        return "Please Enter Date in dd Mon YY"
    if not content['Transaction Details']:
        return "Please Enter Transaction Details"
    if not content['Balance AMT']:
        return "Please Enter Balance AMT"
    cursor = conn.cursor()

    query = " insert into  transactiondata.transaction_log(account_no, date, tran_details, value_date, with_amt, dep_amt, bal_amt) values( "+ str(content['Account No'])+",TO_TIMESTAMP('"+content['Date']+"', 'DD Mon YY'),'"+content['Transaction Details']+"',TO_TIMESTAMP('"+content['Value Date']+"', 'DD Mon YY'),'"+content['Withdrawal AMT']+"','"+content['Deposit AMT']+"','"+content['Balance AMT']+"')"
    cursor.execute(query)
    conn.commit()
    return "Transaction Successfully Added to Database"




if __name__ == '__main__':


	app.run(debug=True)
