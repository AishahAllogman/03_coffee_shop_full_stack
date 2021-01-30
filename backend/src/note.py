@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def drinks-detail(payload):
    Drink=Drink.query.all()
    for drink in Drink:
        drinks=drink.long()
        if len(drinks) == 0:
            abort(404)
    return json {
        "success":True,
        "drinks":drinks
    }

'''

app.route('/drinks/<int:drinks_id>', methods=['DELETE'])
@requires_auth('DELETE:Drink')
def delete_drinks(drink_id):
    try:
        drink= Drink.query.get(drink_id)
        if drink is None:
           abort(404)
        drink.delete() 
        return jsonify({
            'success': True,
            'deleted': drink_id,
        })

    except BaseException:
        print(sys.exc_info())
        abort(422)

        '''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(401)
def Autherro(error):
    return jsonify({
                    "success": False, 
                    "error": 401,
                    "message": "not authonication"
                    }), 401

                    @app.route('/drinks')
def reteirve_drinks():
    Drink=Drink.query.all()
    for drink in Drink: 
        drinks=drink.short()
    return jsonify({
        'success':True,
        'drinks':drinks
    }



    import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
    return response

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def reteirve_drinks():
    Drink=Drink.query.all()
    for drink in Drink: 
        drinks=drink.short()
    return jsonify({
        'success':True,
        'drinks':drinks
    }

#@app.route('/drinks-detail', methods=['GET'])
#@requires_auth('get:drinks-detail')
#def drinks-detail(payload):
    #Drink=Drink.query.all()
    #for drink in Drink:
        #drinks=drink.long()
        #if len(drinks) == 0:
            #abort(404)
    #return json {
        #"success":True,
        #"drinks":drinks
    #}
     


## Error Handling

#new delete 
app.route('/drinks/<int:drinks_id>', methods=['DELETE'])
@requires_auth('delete:drtinks')
def delete_drinks(payload,drinks_id):
    try:
        drink= Drink.query.get(drinks_id)
        if drink is None:
           abort(404)
        drink.delete() 
        return jsonify({
            'success': True,
            'deleted': drinks_id,
        })
    except BaseException:
        print(sys.exc_info())
        abort(422)