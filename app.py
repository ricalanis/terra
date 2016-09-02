import os
import json
import tools
import fileops
import inegi
from flask import Flask, render_template, request, redirect, url_for, Response


app = Flask(__name__)


def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE,  \
          GET,POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response

app.after_request(add_cors_headers)

'''
Routing for your application.
'''


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        filename = fileops.save_file(file)
        excel_dict = fileops.read_excel(filename)
        output_dict = inegi.bulk_coords_convert(excel_dict)
        output_csv = fileops.return_csv(output_dict)
        return Response(response=output_csv, status=200, mimetype="text/csv")

    return '''
    <!doctype html>
    <title>Sube un excel como este:.</title>
    <h1>Sube un archivo</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/about/')
def about():
    '''
    Function: about(). Renders the website's about page.
    Route: <API>/about
    Method: GET
    '''
    return render_template('about.html')


@app.route('/query')
def query():
    '''
    Function:
    Route: <API>/
    Method: GET
    Input parameters:
    Usage: /query?q=<String>
    Example:/query?q=Garza%20Sada
    '''
    query = request.args.get('q')
    output = inegi.call_inegi(query)
    return Response(response=json.dumps(output),
                    status=200, mimetype="application/json")


@app.route('/intersection')
def intersection():
    '''
    Function: intersection()
    Route: <API>/intersection
    Method: GET
    Input parameters: calle1, calle2, ciudad
    Usage: /intersection?calle1=<String>&calle2=<String>&ciudad=<String>
    Example:/intersection?calle1=Garza%20Sada&calle2=Acapulco&ciudad=Monterrey
    '''
    street1 = request.args.get('calle1')
    street2 = request.args.get('calle2')
    city = request.args.get('ciudad')
    output = inegi.crossing(street1, street2, city)
    return Response(response=json.dumps(output),
                    status=200, mimetype="application/json")


@app.errorhandler(404)
def page_not_found(error):
    '''
    Function: page_not_found(). Displays our famous HTTP404 error.
    '''
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
