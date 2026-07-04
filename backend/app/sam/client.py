from datetime import date, timedelta

import requests

from app.core.config import settings


def test_sam_api_connection():
    if not settings.SAM_API_KEY:
        return {
            "status": "error",
            "message": "SAM_API_KEY is missing from .env",
        }

    posted_to = date.today()
    posted_from = posted_to - timedelta(days=30)

    params = {
        "api_key": settings.SAM_API_KEY,
        "limit": 1,
        "offset": 0,
        "postedFrom": posted_from.strftime("%m/%d/%Y"),
        "postedTo": posted_to.strftime("%m/%d/%Y"),
    }

    try:
        response = requests.get(
            settings.SAM_API_BASE_URL,
            params=params,
            timeout=20,
        )

        return {
            "status": "ok" if response.status_code == 200 else "error",
            "status_code": response.status_code,
            "url_tested": settings.SAM_API_BASE_URL,
            "mode": settings.SAM_API_MODE,
            "posted_from": params["postedFrom"],
            "posted_to": params["postedTo"],
            "response_preview": response.text[:1000],
        }

    except requests.RequestException as error:
        return {
            "status": "error",
            "message": str(error),
        }
