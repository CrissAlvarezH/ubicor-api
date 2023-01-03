import requests

from app.core.config import settings


def revalidate_frontend(university_slug: str, building_codes: str):
    url = f"{settings.FRONTEND_DOMAIN}/api/revalidate"
    query_params = {
        "university": university_slug,
        "buildings": building_codes,
        "secret": settings.FRONTEND_REVALIDATE_SECRET,
    }

    requests.post(url, params=query_params)
