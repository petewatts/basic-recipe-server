import argparse
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recipe REST App")
    parser.add_argument("-d", "--debug", action="store_true", help="Debug (Do not use in production)")
    args = parser.parse_args()

    app.run(debug=args.debug)
