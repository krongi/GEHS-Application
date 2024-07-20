import functools
import json

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.exceptions import abort

from db import get_db

bp = Blueprint('dash', __name__)

@bp.route('/')
def index():
    db = get_db()
    error = None

    if error is None:
        cur = db.cursor()
        cur.execute('SELECT tk_number, tk_customer, tk_wo, tk_date, tk_time, tk_bin_num FROM tickets ORDER BY _id DESC LIMIT 10')
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))
        tickets = []
        for child in json_data:
            ticketNumberString = 'Ticket #: ' + str(child.pop('tk_number'))
            ticketCustomerString = ', Customer: ' + child.pop('tk_customer')
            ticketWorkOrderString = ', Work Order: ' + str(child.pop('tk_wo'))
            ticketDayString = ', Date: ' + child.pop('tk_date') + ', '
            ticketDateString = str(child.pop('tk_time')) + ' ' + str(child.pop('tk_bin_num'))
            childString = ticketNumberString + ticketCustomerString + ticketWorkOrderString + ticketDayString + ticketDateString
            tickets.append(childString)
        return  render_template('dash/main.html', tickets = tickets)
        

@bp.route('/main', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        db = get_db()
        error = None

        if error is None:
            cur = db.cursor()
            cur.execute('SELECT  _id FROM wodata LIMIT 4')
            row_headers = [x[0] for x in cur.description]
            rv = cur.fetchall()
            json_data = []
            for result in rv:
                json_data.append(dict(zip(row_headers, result)))
            
        return render_template('dash/main.html')
            



