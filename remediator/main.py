import logging
from fastapi import FastAPI, Request
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AutoRemediator")

app = FastAPI(title="Auto-Remediation Service")

@app.post("/webhook")
async def receive_alert(request: Request):
    body = await request.json()
    logger.info(f"🔔 Received Alertmanager Webhook Payload: {body}")
    
    alerts = body.get("alerts", [])
    for alert in alerts:
        status = alert.get("status")
        alertname = alert.get("labels", {}).get("alertname", "UnknownAlert")
        
        if status == "firing":
            logger.warning(f"⚠️ ALERT FIRING: '{alertname}'. Initiating auto-remediation...")
            
            try:
                # Trigger self-heal routine on the target application API
                response = requests.post("http://app:8000/reset", timeout=5)
                if response.status_code == 200:
                    logger.info("✨ SUCCESS: Auto-remediation completed. Target app restored to healthy state.")
                else:
                    logger.error(f"❌ Remediation failed with status code: {response.status_code}")
            except Exception as e:
                logger.error(f"🔥 Error executing remediation request: {e}")
                
    return {"status": "received"}
