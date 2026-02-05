# Python HTTP Track

## Run Service A
```bash
cd service-a
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Service A runs on:http://127.0.0.1:8080
Test Service A:curl http://127.0.0.1:8080/health
curl "http://127.0.0.1:8080/echo?msg=hello"

## Run Service B (new terminal)
```bash
cd service-b
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Service B runs on:
http://127.0.0.1:8081
Success proof

With both services running, execute:
## Test
```bash
curl "http://127.0.0.1:8081/call-echo?msg=hello"
```
Expected output:
{
  "service_a": { "echo": "hello" },
  "service_b": "ok"
}
**Failure proof (independent failure)**

Stop Service A using Ctrl + C
Keep Service B running
Run:curl -i "http://127.0.0.1:8081/call-echo?msg=hello"

Expected result:

HTTP 503 Service Unavailable

Error message indicating Service A is unreachable

Service B remains running and logs the error


****What makes this distributed?
****
This system is distributed because Service A and Service B run as independent processes on different ports and communicate over HTTP across a network boundary (localhost). Service B depends on Service A via a network call with a timeout, and when Service A is stopped, Service B continues running and returns HTTP 503 instead of crashing. This demonstrates independent failure handling and network-based communication, which are core properties of distributed systems.

**Notes**

Each service runs in its own terminal

Service B uses a timeout when calling Service A

Basic logging records service name, endpoint, status code, and latency
