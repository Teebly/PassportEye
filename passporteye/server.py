import os

from flask import Flask, request, jsonify

from passporteye import read_mrz

app = Flask(__name__)
application = app  # for gunicorn


@app.route("/health")
def health():
    return "Hello"


@app.route("/extract", methods=["POST"])
def handle_address_confirmation():
    return jsonify(read_mrz(request.data).to_dict())


# example usage:
# http :3008/extract @test.jpeg
if __name__ == "__main__":
    app.debug = os.getenv("DEBUG", False)
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "3008")))
