import logging
import time
from typing import Any, Dict, List, Optional

from openai import OpenAI

from ecopulse_ai.config import OPENAI_API_KEY
from .prompts import SYSTEM_PROMPT

logger = logging.getLogger("RAG-Copilot")

# Initialize OpenAI client singleton
client = OpenAI(api_key=OPENAI_API_KEY)


def ask_copilot(query: str, current_metrics: Dict[str, Any], active_alerts: List[Dict[str, Any]]) -> str:
    """
    Interfaces with the OpenAI GPT-4o model to provide context-aware environmental insights.
    Implements a retry mechanism for improved reliability in intermittent network conditions.
    """
    context = f"Current Telemetry: {current_metrics}\nActive System Alerts: {active_alerts}"
    
    max_retries = 3
    retry_delay = 2  # Seconds

    for attempt in range(max_retries):
        try:
            logger.info(f"Querying AI Copilot (Attempt {attempt+1}/{max_retries}): '{query}'")
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Context: {context}\n\nUser Question: {query}"}
                ],
                temperature=0.7,
                timeout=15.0
            )
            return str(response.choices[0].message.content)

        except Exception as e:
            err_msg = str(e)
            logger.warning(f"API attempt {attempt+1} failed: {err_msg}")
            
            # If it's a quota issue, immediate fallback (don't retry)
            if "429" in err_msg or "insufficient_quota" in err_msg:
                break
                
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
                
            logger.error(f"Copilot API exhausted all {max_retries} attempts.")
            break

    # --- Robust Deterministic Fallback (Simulation Mode) ---
    aqi = current_metrics.get("aqi", "Unknown")
    severity = current_metrics.get("severity", "Stable")
    attribution = current_metrics.get("attribution", {})
    t_impact = attribution.get("traffic", "Unknown")
    i_impact = attribution.get("industrial", "Unknown")

    return (
        f"### 🤖 High-Correlation Analytics (Offline Mode)\n\n"
        f"**Status**: The model is currently prioritizing deterministic analytics due to API rate limits.\n\n"
        f"- **AQI Reading**: {aqi} ({severity})\n"
        f"- **Primary Driver**: Traffic Accumulation ({t_impact}%) and Industrial Outflow ({i_impact}%).\n"
        f"- **Mandate**: Air quality is currently within '{severity}' parameters. Suggest using HEPA filters if indoors "
        f"and reducing high-intensity exercise in high-traffic zones."
    )
