import csv
from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://SalesProspects:S@lesProsp@localhost:8889/SalesProspects"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

#secret key, property that needs to be set in order for sessions to work
app.secret_key = "9QvF91rIL1v8keG"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))

    def __init__(self, username, password):
        self.username = username
        self.password = password
        #TODO: Securely store passwords in database

#want this to run for every request that comes in
@app.before_request
def require_login():
    #list of pages can view w/o logging in
    allowed_routes = ["login"]
    if request.endpoint not in allowed_routes and "username" not in session:
        #TODO: Add title to show in browser tab
        return redirect("/login")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        #gets data out of the request
        #request.form is the python dict that contains data sent in a post request
        username = request.form["username"]
        password = request.form["password"]
        #verify this user's pw, retrieve the user with the given un from database
        #if expect to only have one result or only want to get the first, can use .first() as done here
        user = User.query.filter_by(username=username).first()
        #checks first if user exists, then compares the pw
        if user and user.password == password:
            #TODO: Change to use cookies so will not keep logged in long term
            #flag to show whether or not user is considered to be logged in
            session["username"] = username
            #if passes, will be redirected to main page
            return redirect("/")
        else:
            #TODO: explain why login failed
            return "<h1>Incorrect login information</h1>"
    #if don't login will return back to login form        
    return render_template("login.html")

@app.route("/logout")
def logout():
    #removes username from session
    del session["username"]
    return redirect("/")

@app.route("/") #potentially will need to add ("/", methods=["POST", "GET"])
def index():
    data = all_data_of_interest()  
    headers = data[0]
    data = data[1:]
    #TODO: Update title
    return render_template("data.html",title="Data!", data=data, headers=headers)

#generates a list of a list of only the data from the columns of interest
def all_data_of_interest():
    # bringing in raw CSV data
    with open('C:/Users/Elisa/Documents/SalesProspects/Data/ACO.SSP.PUF.Y2016.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        col_of_interest_indices = []
        is_header = True
        data = []
        for row in reader:
            # row is list of str
            if is_header == True:
                col_of_interest_indices = find_headers_of_interest_index(row)
                is_header = False
                data.append(data_of_interest(row, col_of_interest_indices))  
            else:
                data.append(data_of_interest(row, col_of_interest_indices))
        return data

#finds the indices of the columns/headers of interest
def find_headers_of_interest_index(header_row):
    headers_of_interest = ['ACO_Name', 'ACO_State', 'Initial_Start_Date', 'Current_Track_1', 'Current_Track_2', 'Current_Track_3',
                           'N_AB', 'BnchmkMinExp', 'GenSaveLoss', 'EarnSaveLoss', 'Met_QPS', 'Prior_Sav_Adj', 'UpdatedBnchmk', 'HistBnchmk']
    col_of_interest_indices = []
    for header in headers_of_interest:
        col_of_interest_indices.append(header_row.index(header))
    return col_of_interest_indices

#grabs only the data in the row from the column of interest, returns a list
def data_of_interest(row, col_indices):
    data = []
    for index in col_indices:
        data.append(row[index])
    return data


if __name__ == '__main__':
    app.run()
