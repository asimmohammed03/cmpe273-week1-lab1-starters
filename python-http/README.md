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
