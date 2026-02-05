# Python HTTP Track

## Run Service A
```bash
cd service-a
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
<img width="1920" height="239" alt="Screenshot (865)" src="https://github.com/user-attachments/assets/3c91e060-ecc6-4359-93dc-7323b4324d26" />

Service A runs on:http://127.0.0.1:8080
Test Service A:curl http://127.0.0.1:8080/health
curl "http://127.0.0.1:8080/echo?msg=hello"
<img width="1920" height="239" alt="Screenshot (866)" src="https://github.com/user-attachments/assets/de0497d1-958d-44b8-8d65-bded27a4809b" />


## Run Service B (new terminal)
```bash
cd service-b
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
<img width="1920" height="228" alt="Screenshot (867)" src="https://github.com/user-attachments/assets/a9de9339-389e-4962-836a-376e550fd990" />

Service B runs on:
http://127.0.0.1:8081
<img width="1920" height="229" alt="Screenshot (868)" src="https://github.com/user-attachments/assets/092ba892-923d-4cdf-826f-7cc1dcb0270c" />

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
<img width="1920" height="247" alt="Screenshot (869)" src="https://github.com/user-attachments/assets/c91b2331-cf91-4611-a0bf-fae970b2e2d6" />

**Failure proof (independent failure)**

Stop Service A using Ctrl + C
Keep Service B running
Run:curl -i "http://127.0.0.1:8081/call-echo?msg=hello"

Expected result:

HTTP 503 Service Unavailable

Error message indicating Service A is unreachable

Service B remains running and logs the error
<img width="1920" height="536" alt="Screenshot (870)" src="https://github.com/user-attachments/assets/e3164f75-cd7f-478f-96b0-d1ebdfb51364" />


****What makes this distributed?
****
This system is distributed because Service A and Service B run as independent processes on different ports and communicate over HTTP across a network boundary (localhost). Service B depends on Service A via a network call with a timeout, and when Service A is stopped, Service B continues running and returns HTTP 503 instead of crashing. This demonstrates independent failure handling and network-based communication, which are core properties of distributed systems.

**Notes**

Each service runs in its own terminal

Service B uses a timeout when calling Service A

Basic logging records service name, endpoint, status code, and latency

**What happens on timeout?**

Service B calls Service A using an HTTP client with a timeout (for example requests.get(..., timeout=1.0)). If Service A is slow or doesn’t respond within that time, the client raises a timeout exception. Service B catches it, logs an error (timeout/latency details), and returns HTTP 503 Service Unavailable to the caller. This prevents Service B from hanging forever.

**What happens if Service A is down?**

If Service A is stopped (Ctrl+C), there is no process listening on 127.0.0.1:8080. When Service B tries to call Service A, the HTTP request fails (connection refused or connect timeout). Service B catches the error, logs that Service A is unreachable, and returns HTTP 503 with a JSON error message. Service B itself stays running, showing independent failure.

**What do your logs show, and how would you debug?**

Each request logs basic request info:

service name (service-a / service-b)

endpoint (/health, /echo, /call-echo)

status code (200, 503, etc.)

latency (how long the request took)

To debug:

1.Reproduce the issue with curl.

2.Check Service B logs to see whether it was a timeout vs connection failure.

3.Confirm Service A is actually running by calling curl http://127.0.0.1:8080/health.

4.If ports are wrong, verify listeners with netstat -ano | findstr :8080 and :8081.

5.Use the latency and status logs to pinpoint whether the slowdown/failure is in Service A, the network call, or Service B’s handler.
