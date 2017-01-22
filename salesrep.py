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


'''# Delete a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurantToDelete = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        flash('%s Successfully Deleted' % restaurantToDelete.name)
        session.commit()
        return redirect(url_for('showRestaurants', restaurant_id=restaurant_id))
    else:
        return render_template('deleteRestaurant.html', restaurant=restaurantToDelete)'''

# Show sales rep details for selected sales rep


@app.route('/salesreps/<int:salesrep_id>/')
@app.route('/salesreps/<int:salesrep_id>/repdetails')
def showRep(salesrep_id):
    salesrep = session.query(SalesReps).filter_by(id=salesrep_id).one()
    details = session.query(RepDetails).filter_by(
        salesrep_id=salesrep_id).all()
    return render_template('repdetails.html', salesrep=salesrep, details=details)


'''# Create a new menu item
@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash('New Menu %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

# Edit a menu item


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(saleserep_name, salesrep_id):

    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        flash('Menu Item Successfully Edited')
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)


# Delete a menu item
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html', item=itemToDelete)'''







if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)