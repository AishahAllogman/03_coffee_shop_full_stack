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

db_drop_and_create_all()


@app.after_request
def after_request(response):
    response.headers.add(
    'Access-Control-Allow-Headers',
     'Content-Type,Authorization,true')
    response.headers.add(
    'Access-Control-Allow-Methods',
     'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/drinks')
def reteirve_drinks():
    Drinks = Drink.query.all()
    drinks = [drink.short()for drink in Drinks]
    # or drink in Drinks:
        # drinks=[drink.short()for drink in Drinks]
    return jsonify({
        'success': True,
        'drinks': drinks
    })


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def drinksdetail(payload):
    Drinks = Drink.query.all()
    drinks = [drink.long()for drink in Drinks]

    return jsonify({
        'success': True,
        'drinks': drinks
    })


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drinks(payload):
    body = request.get_json()
    req_title = body.get('title')
    req_recipe = json.dumps(body['recipe'])
    try:
        drink = Drink(title=req_title, recipe=req_recipe)
        drink.insert()
        return jsonify({
                    'success': True,
                    'drinks': [drink.long()]
                })
    except Exception as e:
            print(e)
            abort(422)


@app.route('/drinks/<int:drinks_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drinks(payload, drinks_id):
    drink = Drink.query.filter(Drink.id == drinks_id).one_or_none()
    if drink is None:
        abort(404)
    body = request.get_json()
    req_title = body.get('title')
    req_recipe = json.dumps(body['recipe'])
    try:
        drink.title = req_title
        drink.recipe = req_recipe
        drink.update()

        return jsonify({
                    'success': True,
                    'drinks': [drink.long()]

                })
    except Exception as e:
            print(e)
            abort(422)


@app.route('/drinks/<int:drinks_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, drinks_id):
    Drinks = Drink.query.filter(Drink.id == drinks_id).one_or_none()
    if Drinks is None:
        abort(404)
    try:
        Drinks.delete()
        return jsonify({
                        'success': True,
                        'detele': drinks_id
                    })
    except Exception as e:
            print(e)
            abort(422)


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


@app.errorhandler(400
def bad_request(error):
    return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response=jsonify(ex.error)
    response.status_code=ex.status_code
    return response
