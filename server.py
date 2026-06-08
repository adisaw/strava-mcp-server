import os
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")

BASE_URL = "https://www.strava.com/api/v3"

mcp = FastMCP("strava")

_access_token: str | None = None


async def get_access_token() -> str:
    """Refresh and return a valid Strava access token."""
    global _access_token
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://www.strava.com/api/v3/oauth/token",
            data={
                "client_id": STRAVA_CLIENT_ID,
                "client_secret": STRAVA_CLIENT_SECRET,
                "refresh_token": STRAVA_REFRESH_TOKEN,
                "grant_type": "refresh_token",
            },
        )
        resp.raise_for_status()
        data = resp.json()
        _access_token = data["access_token"]
    return _access_token


async def strava_get(endpoint: str, params: dict | None = None) -> dict | list:
    """Make an authenticated GET request to the Strava API."""
    token = await get_access_token()
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{BASE_URL}{endpoint}",
            headers={"Authorization": f"Bearer {token}"},
            params=params or {},
        )
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def get_athlete() -> dict:
    """Get the authenticated athlete's profile information."""
    return await strava_get("/athlete")


@mcp.tool()
async def get_athlete_stats(athlete_id: int) -> dict:
    """Get all-time, year-to-date, and recent stats for an athlete.

    Args:
        athlete_id: The ID of the athlete (use get_athlete to find your ID)
    """
    return await strava_get(f"/athletes/{athlete_id}/stats")


@mcp.tool()
async def get_activities(page: int = 1, per_page: int = 30) -> list:
    """Get a list of the authenticated athlete's activities.

    Args:
        page: Page number (default 1)
        per_page: Number of activities per page (default 30, max 200)
    """
    return await strava_get(
        "/athlete/activities", params={"page": page, "per_page": per_page}
    )


@mcp.tool()
async def get_activity(activity_id: int, include_all_efforts: bool = False) -> dict:
    """Get detailed information about a specific activity including splits, laps, and segment efforts.

    Args:
        activity_id: The ID of the activity
        include_all_efforts: Whether to include all segment efforts (default False)
    """
    return await strava_get(
        f"/activities/{activity_id}",
        params={"include_all_efforts": str(include_all_efforts).lower()},
    )


@mcp.tool()
async def get_activity_laps(activity_id: int) -> list:
    """Get laps/splits for a specific activity.

    Args:
        activity_id: The ID of the activity
    """
    return await strava_get(f"/activities/{activity_id}/laps")


@mcp.tool()
async def get_activity_kudos(activity_id: int, page: int = 1, per_page: int = 30) -> list:
    """Get the athletes who gave kudos on an activity.

    Args:
        activity_id: The ID of the activity
        page: Page number (default 1)
        per_page: Number of items per page (default 30)
    """
    return await strava_get(
        f"/activities/{activity_id}/kudos",
        params={"page": page, "per_page": per_page},
    )


@mcp.tool()
async def get_routes(page: int = 1, per_page: int = 30) -> list:
    """Get the authenticated athlete's saved routes.

    Args:
        page: Page number (default 1)
        per_page: Number of routes per page (default 30)
    """
    return await strava_get(
        "/athlete/routes", params={"page": page, "per_page": per_page}
    )


if __name__ == "__main__":
    mcp.run()
