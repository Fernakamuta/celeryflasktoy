from os import environ

from app import create_app


if __name__ == '__main__':
    app = create_app(mode=environ['MODE'])
    app.run(debug=True)
