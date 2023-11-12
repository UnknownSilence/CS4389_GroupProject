from http import HTTPStatus
from typing import Any

from flask import (abort, Blueprint, jsonify, redirect, request, session, url_for)

from .api import (
    login as login_handler, 
    register as registration_handler,
    accounts as account_handler
)

from .db import database
from .db.common_operations import getUserByID
from .config import BASE_DIR

api = Blueprint('api', __name__, url_prefix='/api')

def formView(request: request, get_response: Any, post_response: Any) -> Any:
    if (request.method == 'GET'):
        return get_response()
    elif (request.method == 'POST'):
        return post_response()
    else:
        return abort(HTTPStatus.METHOD_NOT_ALLOWED)
    
@api.route('/login', methods=(['POST']))
def login():
    return login_handler.onLogin(request)
    
@api.route('/register', methods=('GET', 'POST'))
def register():
    get = lambda: 'Register Page' #render_template('auth/register.html')
    post = lambda: registration_handler.onRegister(request)
    return formView(request, get, post)

@api.route('/@me', methods=(['GET']))
def get_current_user():
    user_id = session.get('user_id')

    if (user_id is None):
        return redirect(url_for('/'))

    db = database.get()
    record = getUserByID(db, user_id)

    return jsonify({
        'ID': user_id,
        'Username': record['user'],
        'First Name': record['first_name'],
        'Last Name': record['last_name'],
        'Date of Birth': record['date_of_birth'],
        'Primary Address': record['address'],
        'Phone Number': record['phone_number']
    })
    
#path for account    
@api.route('/accounts', methods=['GET'])
def accounts():
    return account_handler.onRequestAccountInfo(request)