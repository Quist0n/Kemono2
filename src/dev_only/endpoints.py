from flask import Blueprint, make_response, render_template

dev_only = Blueprint('dev-only', __name__)

@dev_only.route('/dev-only', methods=['GET'])
def main_page():
    props = {
        'currentPage': 'dev-only',
    }

    response = make_response(render_template(
        'dev_only/_index.html',
        props = props
    ), 200)
    response.headers['Cache-Control'] = 's-maxage=60'
    return response

@dev_only.route('/dev-only', methods=['POST'])
def activate_dev_mode():
    pass
