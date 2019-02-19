import base64
import os
from io import BytesIO

from flask import Flask, request, jsonify

from passporteye import read_mrz

app = Flask(__name__)
application = app  # for gunicorn


@app.route("/health")
def health():
    return "Hello"


@app.route("/extract", methods=["POST"])
def handle_address_confirmation():
    try:
        return jsonify(read_mrz(request.data).to_dict())
    except ValueError:
        # https://stackoverflow.com/a/49459036/419338
        # some JS implementation do not pad enough, but py3 will truncate redundant padding
        decoded = base64.b64decode(request.data + b'=====')
        return jsonify(read_mrz(BytesIO(decoded)).to_dict())


# example usage:
# http :3008/extract @test.jpeg
if __name__ == "__main__":
    app.debug = os.getenv("DEBUG", False)
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "3008")))
