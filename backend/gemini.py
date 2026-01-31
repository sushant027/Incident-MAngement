import os, requests

GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def similar_incidents(payload):
    if not GEMINI_KEY:
        return None
    # minimal RAG stub (stored advisory only)
    return {
        "recommendation": "Check previous outage in same service",
        "similar": []
    }
