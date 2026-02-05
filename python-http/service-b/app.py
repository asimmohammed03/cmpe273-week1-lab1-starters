from flask import Flask, request, jsonify
import requests
import time
import logging

app = Flask(__name__)
SERVICE_NAME = "service-b"
SERVICE_A_URL = "http://127.0.0.1:8080/echo"
TIMEOUT_SECONDS = 1

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

@app.route("/call-echo", methods=["GET"])
def call_echo():
    msg = request.args.get("msg", "")
    try:
        resp = requests.get(
            SERVICE_A_URL,
            params={"msg": msg},
            timeout=TIMEOUT_SECONDS
        )
        resp.raise_for_status()
        return jsonify(
            service_b="ok",
            service_a=resp.json()
        )
    except requests.exceptions.RequestException as e:
        logging.error("Error calling service A: %s", str(e))
        return jsonify(
            service_b="ok",
            service_a="unavailable",
            error=str(e)
        ), 503

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081)
