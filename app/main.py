from fastapi import FastAPI, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="Target Microservice")

# Prometheus Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['endpoint', 'http_status'])
ERROR_COUNT = Counter('http_errors_total', 'Total HTTP 5xx Errors')

# Internal state simulation
is_degraded = False

@app.get("/")
def read_root():
    REQUEST_COUNT.labels(endpoint='/', http_status='200').inc()
    return {"status": "healthy", "degraded": is_degraded}

@app.get("/simulate-failure")
def simulate_failure():
    global is_degraded
    is_degraded = True
    return {"message": "🚨 Service forced into DEGRADED state. Throwing 5xx errors."}

@app.post("/reset")
def reset_service():
    global is_degraded
    is_degraded = False
    return {"message": "✅ Auto-remediation executed: Service state reset to healthy."}

@app.get("/data")
def get_data():
    global is_degraded
    if is_degraded:
        ERROR_COUNT.inc()
        REQUEST_COUNT.labels(endpoint='/data', http_status='500').inc()
        return Response("Internal Server Error (Simulated)", status_code=500)
    
    REQUEST_COUNT.labels(endpoint='/data', http_status='200').inc()
    return {"data": ["item1", "item2", "item3"]}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
