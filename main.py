import csv
from flask import Flask, request, redirect, render_template

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def index():
    data = all_data_of_interest()  
    headers = data[0]
    data = data[1:]
    return render_template("data.html",title="Data!", data=data, headers=headers)

#generates a list of a list of only the data from the columns of interest
def all_data_of_interest():
    # bringing in raw CSV data
    with open('C:/Users/Elisa/Documents/SalesProspects/ACO.SSP.PUF.Y2016.csv', newline='') as csvfile:
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
