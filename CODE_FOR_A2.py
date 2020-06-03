import time 
import pandas as pd
from flask import Flask, render_template,url_for,jsonify,request,redirect,g
import sqlite3
app = Flask(__name__)
Login_ID=[]
@app.route('/index')
def index(): 
	return render_template("index.html")

@app.route('/checkout')
def checkout(): 
	return render_template("checkout.html")

@app.route('/login')
def login(): 
	return render_template("login.html")
@app.route('/Wallet')
def Wallet(): 
	connection = sqlite3.connect("customer.db")
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM Transactions WHERE Email = ?",([Login_ID[0]]))
	Transactions = cursor.fetchall()
	connection.commit
	connection = sqlite3.connect("shop_data.db")
	cursor = connection.cursor()
	cursor.execute("SELECT Price FROM DIM_CRYPTO_DATA ")
	Cryptoprice = cursor.fetchall()
	Price =[]
	for t in Cryptoprice:
		for x in t :
			Price.append(x)
	connection.commit
	print (Transactions)
	print(Login_ID[0])
	return render_template("Wallet.html",Transactions=Transactions, Price = Price , FRemail=Transactions[0][0])
@app.route('/Transaction',methods =['GET','POST'])
def Transaction():
	connection = sqlite3.connect("customer.db")
	cursor = connection.cursor()
	if request.method == 'POST' :
		Returningemail = request.form['Returningemail']
		Returningquantity = request.form['Returningquanity']
		Returningmonetaryvalue = request.form['Returningmonetaryvalue']
		CurrencyID = request.form['CurrencyID']
		cursor.execute("SELECT * FROM Customer WHERE Email =?",([Returningemail]))
		Credentials = cursor.fetchall
		
	if Credentials :
		 cursor.execute("""INSERT INTO Transactions (Email,Currency,Quantity,Worth) VALUES(?,?,?,?)""",([Returningemail,CurrencyID,Returningquantity,Returningmonetaryvalue]))
		 connection.commit
		 return redirect(url_for('Wallet'))
	else:
		return render_template("CheckoutT.html",Email=Returningemail)

@app.route('/Edit')
def Edit(): 
	return render_template("Edit.html")
@app.route('/Tax',methods=['GET','POST'])
def Tax():
	connection = sqlite3.connect("shop_data.db")
	cursor = connection.cursor()
	if request.method == 'POST':
		Frname = request.form['Forname']
		DoB = request.form['DOBL']
		NIN = request.form['NINL']
		Tax = request.form['TaxGBP']
		NiGBP = request.form['NiGBP']
		HmccGBP = request.form['HmccGBP']
		TotalPayGBP = request.form['TotalPayGBP']
		NetPayGBP = request.form['NetPayGBP']
		cursor.execute("""INSERT INTO Employees (Name,DateOfBirth,NationalInsuranceNumber,Totalpay,Taxation,NationalInsurance,HMCC,NetPay) 
		VALUES (?,?,?,?,?,?,?,?)""",([Frname,DoB,NIN,TotalPayGBP,Tax,NiGBP,HmccGBP,NetPayGBP]))
	connection.commit()
	connection.close()
	return redirect(url_for('Edit'))	

@app.route('/api/get_all_data/')
def api_all_data():

	connection = sqlite3.connect("shop_data.db")
	cursor = connection.cursor() 

	cursor.execute("SELECT Currency_Name, TimeId, High from CRYPTO_PARENT Where TimeId Like '201801%'")
	crypto_data = cursor.fetchall()

	df = pd.DataFrame(crypto_data, columns=['Currency_Name', 'Time', 'High'])

	df['Value'] = (1 / df['High'])

	df['Time'] = pd.to_datetime(df['Time'])

	df = df.pivot(index='Time', columns='Currency_Name', values='Value').reset_index()

	headers = list(df)[1:]

	data = df[headers].values.tolist()

	
	return jsonify(data)

@app.route('/insert_value',methods = ['GET','POST'])
def insert_value():
	connection = sqlite3.connect("customer.db")
	cursor = connection.cursor()
	if request.method == 'POST' :
		Fname = request.form['Fname']
		Lname = request.form['Lname']
		CardNumber = request.form['CardNumber']
		CVV = request.form['CVV']
		Email = request.form['Email']
		cursor.execute("""INSERT INTO Customer (Fname,Lname,CardNumber,CVV,Email)
		VALUES (?,?,?,?,?,?)""", ([Fname,Lname,CardNumber,CVV,Email]))
	connection.commit()
	cursor.execute("SELECT * FROM Accounts WHERE Email Address = ?",([Email]))
	AccountCheck = cursor.fetchall()
	if AccountCheck:
		Login_ID.append(Email)
		return redirect(url_for('Wallet'))
	else:
		return render_template('loginT.html',Email=Email)

@app.route('/Sign_Up',methods = ['GET','POST'])
def Sign_Up():
	connection = sqlite3.connect("customer.db")
	cursor = connection.cursor()
	if request.method == 'POST':
		Uname = request.form['Username']
		Pword = request.form['Password']
		Email = request.form['Email']
		print(Uname)
	cursor.execute("""INSERT INTO Accounts (Username,Password,Email Address) VALUES(?,?,?)""",([Uname,Pword,Email]))  
	connection.commit()
	connection.close()
	return redirect(url_for('login.html'))
	
	## if results :
	# print("login") 
	#redirect (url_for('login.html'))
	#else : 
	# print("Can't login")
	#redirect( url_for('index.html'))
	# cursor.execute("""INSERT INTO users (username, password)
	#VALUES (?,?)""", ([Uname,Pword]))

@app.route('/login_User',methods = ['GET','POST'])
def login_User():
	connection = sqlite3.connect("customer.db")
	cursor = connection.cursor()
	if request.method == "POST":
		Username_login = request.form['uname']
		Password_login = request.form['psw']
	cursor.execute("SELECT * FROM Accounts WHERE Username = ? AND Password = ?",([Username_login,Password_login]))
	results = cursor.fetchall()
	connection.commit()
	print (results)
	if results:
		for i in results :
			if 'Admin1234'in i[1] and 'Password1' in i[2]:
				return redirect (url_for('Edit'))
			else :
				Login_ID.append(i[0])
				return redirect (url_for('Wallet'))
	else:
		return redirect( url_for('login'))

if __name__ == "__main__":
	app.run(host='192.168.0.01',port= 9000, debug=False)