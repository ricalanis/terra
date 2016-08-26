from werkzeug import secure_filename
from xlrd import open_workbook
import pandas as pd
import os
import csv

from io import StringIO


import tools

ALLOWED_EXTENSIONS = set(['xls', "xlsx"])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def save_file(file):
    if file and allowed_file(file.filename):
        random_folder = tools.id_generator()
        filepath = "data/" + random_folder
        os.makedirs(filepath)
        filename = filepath + "/" + secure_filename(file.filename)
        file.save(filename)
    return filename

def clean_cell(cell):
    output = cell.value.split("text:")[0].replace("'","")
    print(output)
    return output

def read_excel(filename):
    book = open_workbook(filename,on_demand=True)
    output_list = []
    for name in book.sheet_names():
        output_dict = {}
        sheet = book.sheet_by_name(name)
        col_names = sheet.row(0)
        for i in range(1,sheet.nrows,1):
            output_dict = { clean_cell(col_names[j]): clean_cell(sheet.row(i)[j]) for j in range(0,len(col_names),1)}
            output_list.append(output_dict)
    return output_list


def return_csv(data_array):
    data_df = pd.DataFrame.from_dict(data_array)
    output_io = StringIO()
    data_df.to_csv(path_or_buf = output_io, quoting = csv.QUOTE_ALL, index= False)
    response_out = output_io.getvalue()
    return response_out
