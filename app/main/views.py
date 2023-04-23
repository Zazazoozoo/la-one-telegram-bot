from flask import render_template, Blueprint
main = Blueprint(
    'main',
    __name__,
    url_prefix='/'
)


@main.route('/', methods=['GET', 'POST'])
def index():
    return "Hello world"
