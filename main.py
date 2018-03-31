import csv


def print_all_data_of_interest():
    # bringing in raw CSV data
    with open('C:/Users/Elisa/Documents/Capstone/ACO.SSP.PUF.Y2016.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        col_of_interest_indices = []
        is_header = True
        for row in reader:
            # row is list of str
            if is_header == True:
                col_of_interest_indices = find_headers_of_interest_index(row)
                print_data_of_interest(row, col_of_interest_indices)
                is_header = False
            else:
                print_data_of_interest(row, col_of_interest_indices)


def find_headers_of_interest_index(header_row):
    headers_of_interest = ['ACO_Name', 'ACO_State', 'Initial_Start_Date', 'Current_Track_1', 'Current_Track_2', 'Current_Track_3',
                           'N_AB', 'BnchmkMinExp', 'GenSaveLoss', 'EarnSaveLoss', 'Met_QPS', 'Prior_Sav_Adj', 'UpdatedBnchmk', 'HistBnchmk']
    col_of_interest_indices = []
    for header in headers_of_interest:
        col_of_interest_indices.append(header_row.index(header))
    return col_of_interest_indices


def print_data_of_interest(row, col_indices):
    data = []
    for index in col_indices:
        data.append(row[index])
    print(data)


def main():
    print_all_data_of_interest()


if __name__ == '__main__':
    main()
