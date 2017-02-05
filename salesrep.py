from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from salesrep_database import Base, SalesReps, RepDetails
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///salesrep.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Show all salesreps
@app.route('/')
@app.route('/salesreps/')
def showSalesReps():
    salesreps = session.query(SalesReps).order_by(asc(SalesReps.name))
    return render_template('salesreps.html', salesreps=salesreps)

# Create a new sales rep
@app.route('/salesreps/new/', methods=['GET', 'POST'])
def newSalesReps():
    if request.method == 'POST':
        newSalesRep = SalesReps(name=request.form['name'])
        session.add(newSalesRep)
        flash('New Sales Representative %s Successfully Created' % newSalesRep.name)
        session.commit()
        return redirect(url_for('showSalesReps'))
    else:
        return render_template('newSalesReps.html')

# Edit a sales rep
@app.route('/salesreps/<int:salesrep_id>/edit/', methods=['GET', 'POST'])
def editSalesRep(salesrep_id):
    editedSalesRep = session.query(
        SalesReps).filter_by(id=salesrep_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedSalesRep.name = request.form['name']
            flash('Sales Representative Successfully Edited %s' % editedSalesRep.name)
            return redirect(url_for('showSalesReps'))
    else:
        return render_template('editSalesReps.html', salesrep=editedSalesRep)


# Delete a salesrep
@app.route('/salesreps/<int:salesrep_id>/delete/', methods=['GET', 'POST'])
def deleteSalesRep(salesrep_id):
    repToDelete = session.query(
        SalesReps).filter_by(id=salesrep_id).one()
    if request.method == 'POST':
        session.delete(repToDelete)
        flash('%s Successfully Deleted' % repToDelete.name)
        session.commit()
        return redirect(url_for('showSalesReps', salesrep_id=salesrep_id))
    else:
        return render_template('deleteSalesRep.html', salesrep=repToDelete)

# Show sales rep details for selected sales rep
@app.route('/salesreps/<int:salesrep_id>/')
@app.route('/salesreps/<int:salesrep_id>/repdetails')
def showRep(salesrep_id):
    salesrep = session.query(SalesReps).filter_by(id=salesrep_id).one()
    details = session.query(RepDetails).filter_by(
        salesrep_id=salesrep_id).all()
    return render_template('repdetails.html', salesrep=salesrep, details=details)


# Add Rep Details
@app.route('/salesreps/<int:salesrep_id>/repdetails/add/', methods=['GET', 'POST'])
def addRepDetails(salesrep_id):
    salesrep = session.query(SalesReps).filter_by(id=salesrep_id).one()
    salesrepdetails=session.query(RepDetails).filter_by(salesrep_id=salesrep_id).first()
    if request.method == 'POST':
        newItem = RepDetails(name=salesrep.name, payout=request.form[
                   'payout'], sub_reps=request.form['sub_reps'], 
                   contractor=request.form['contractor'], salesrep_id=salesrep_id)
        #if newItem.payout!=None and newItem.contractor!=None and newItem.salesrep_id!=None:
        session.add(newItem)
        session.commit()
        flash('Rep Details %s Successfully Added' % (newItem.name))
        return redirect(url_for('showRep', salesrep_id=salesrep_id))
    #else:
    #	print "Need Rep Details completed to commit changes"
    else:
        return render_template('addRepDetails.html', salesrep_id=salesrep_id, salesrep_name=salesrep.name)

# Edit a rep details
@app.route('/salesreps/<int:salesrep_id>/repdetails/edit', methods=['GET', 'POST'])
def editRepDetails(salesrep_id):
    #editedRep = session.query(RepDetails).filter_by(id=salesrep_id).first()
    salesrep = session.query(SalesReps).filter_by(id=salesrep_id).one()
    details=session.query(RepDetails).filter_by(salesrep_id=salesrep_id).all()
    for i in details:
        if request.method == 'POST':
            if request.form['payout']:
                i.payout = request.form['payout']
            if request.form['sub_reps']:
                i.sub_reps = request.form['sub_reps']
            if request.form['contractor']:
                i.contractor = request.form['contractor']
            session.add(salesrep)
            session.commit()
            flash('Sales Rep Successfully Edited')
            return redirect(url_for('showRep', salesrep_id=salesrep_id))
        return render_template('editRepDetails.html', salesrep_id=salesrep_id,
    	    salesrep_name=salesrep.name, details_payout=i.payout, details_sub_reps=i.sub_reps,
    	    details_contractor=i.contractor)


# Delete a rep details
@app.route('/salesreps/<int:salesrep_id>/repdetails/delete', methods=['GET', 'POST'])
def deleteRepDetails(salesrep_id):
    salesrep = session.query(SalesReps).filter_by(id=salesrep_id).one()
    details=session.query(RepDetails).filter_by(salesrep_id=salesrep_id).all()
    if request.method == 'POST':
        session.delete(details)
        flash('%s Successfully Deleted Details for' % salesrep.name)
        session.commit()
        return redirect(url_for('showRep', salesrep_id=salesrep_id))
    else:
        return render_template('deleteRepDetails.html', salesrep_id=salesrep_id, 
        	salesrep_name=salesrep.name)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True #debug activated
    app.run(host='0.0.0.0', port=8000)