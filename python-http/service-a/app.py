from flask import Flask, request, jsonify
import time
import logging

app = Flask(__name__)
SERVICE_NAME = "service-a"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_request(response):
    latency = (time.time() - request.start_time) * 1000
    logging.info(
        "%s endpoint=%s status=%s latency_ms=%.2f",
        SERVICE_NAME,
        request.path,
        response.status_code,
        latency
    )
    return response

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok")

@app.route("/echo", methods=["GET"])
def echo():
    msg = request.args.get("msg", "")
    return jsonify(echo=msg)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
