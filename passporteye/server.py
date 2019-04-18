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
        mrz = read_mrz(request.data)
        if mrz:
            return jsonify(mrz.to_dict())
        else:
            print(f"Could not extract anything on first pass, will try base64")
            raise ValueError
    except ValueError:
        # https://stackoverflow.com/a/49459036/419338
        # some JS implementation do not pad enough, but py3 will truncate redundant padding
        decoded = base64.b64decode(request.data + b"=====")
        mrz = read_mrz(BytesIO(decoded), flip_horizontal=request.headers.get('flip'))
        if not mrz:
            print(f"Could not extract anything on second pass")
            return jsonify({})
        d = mrz.to_dict()
        print(f"Got doc type {d.get('type')} from {d.get('country')} with score {d['valid_score']}")
        return jsonify(d)


# example usage:
# http :3008/extract @test.jpeg
if __name__ == "__main__":
    app.debug = os.getenv("DEBUG", False)
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "3008")))
