from flask import Flask, request, jsonify, render_template,json
import sqlite3 as sqlite
from sqlite3 import Error
import sys
import os

app = Flask(__name__)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#first screen
@app.route('/', methods=['GET'])
def home():
    return """<h1>Ticket Selling system</h1>
    <p>A very basic API</p>
    """


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#Details about all the events for which tickets are available
@app.route("/events", methods=['GET'])
def api_events():
    conn = sqlite.connect('../data/events.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_events = cur.execute("SELECT * FROM event;").fetchall()
    return jsonify(all_events)

#Details of all the tickets for a particular event
@app.route("/events/<event_id>/tickets", methods=['GET'])
def api_tickets(event_id):
    conn = sqlite.connect('../data/events.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    sql = """SELECT e.eventname,v.venuename,s.sectionid, 
                                s.rownumber,s.seatsavailable,s.priceperseat FROM event e
                                INNER JOIN venue v on e.venueid=v.venueid
                                INNER JOIN section s on s.venueid=v.venueid
                                where e.eventid = %s""" %(event_id)
    all_events = cur.execute(sql).fetchall()
    return jsonify(all_events)

#Method for seller to post tickets, use Curl Commands or Postman
@app.route("/seller", methods=['POST'])
def api_seller():
    _json = request.json
    _sellerid = _json['id']
    _eventid=_json['eventid']
    _card = _json['card']
    _sellingprice = _json['price']
    _sectionid=_json['sectionid']
    _seatnumber=_json['seatnumber']
    sellerInsert = "INSERT INTO seller VALUES(%s,%s,%s,%s,%s,%s)" % (_sellerid, _eventid, _card, _sellingprice,_sectionid,_seatnumber)

    conn = sqlite.connect('../data/events.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(sellerInsert)
    conn.commit()
    cur.close()
    conn.close()
    return 'success'

#Method to update a ticket, Again use curl or postman, gives result of section and rows/tickets updated
@app.route("/events/<event_id>/soldout", methods=['PUT'])
def api_update_tickets(event_id):
    _json = request.json
    _sectionid= _json['sectionid']
    _rownumber = _json['rownumber']

    conn = sqlite.connect('../data/events.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    updatetickets = """UPDATE section set soldoutflag = 'Sold Out'  where exists 
            (select * from section s 
             inner join "event" e on e.venueid=s.venueid
             where eventid=%s and sectionid=%s
             and rownumber=%s)""" %(event_id,_sectionid,_rownumber)
    cur.execute(updatetickets)
    out = """select * from section s 
             inner join "event" e on e.venueid=s.venueid
             where eventid=%s and sectionid=%s
             and rownumber=%s""" %(event_id,_sectionid,_rownumber)
    all_events = cur.execute(out).fetchall()
    return jsonify(all_events)

#gives detail about best ticket for each event. it is based on the maximum price ticket
@app.route("/events/<event_id>/tickets/best", methods=['GET'])
def api_best_tickets(event_id):
    conn = sqlite.connect('../data/events.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    sql = """select e.eventname,v.venuename,s.sectionid,s.rownumber,max(s.priceperseat) as PricePerSeat from "event" e
            inner join venue v on v.venueid=e.venueid
            inner join "section" s on s.venueid =e.venueid
            where e.eventid=%s ;""" %(event_id)
    all_events = cur.execute(sql).fetchall()
    return jsonify(all_events)



if __name__ == '__main__':

    if os.environ.get('PORT') is not None:
        app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT'))
    else:
        app.run(debug=True, host='0.0.0.0')
