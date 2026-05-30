# Strava MCP Server

An MCP (Model Context Protocol) server that provides access to the Strava API — query your activities, stats, routes, and more from any MCP-compatible client.

## Tools

| Tool | Description |
|------|-------------|
| `get_athlete` | Get your profile information |
| `get_athlete_stats` | Get all-time, YTD, and recent stats |
| `get_activities` | List your activities (paginated) |
| `get_activity` | Get detailed activity data (splits, laps, segments) |
| `get_activity_laps` | Get laps for a specific activity |
| `get_routes` | List your saved routes |

## Setup

### 1. Create a Strava API App

Go to [strava.com/settings/api](https://www.strava.com/settings/api) and create an application.

### 2. Get a Refresh Token

Authorize your app with the required scopes:

```
https://www.strava.com/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=http://localhost&scope=read,activity:read_all&approval_prompt=auto
```

Then exchange the code for tokens:

```bash
curl -X POST https://www.strava.com/oauth/token \
  -d client_id=YOUR_CLIENT_ID \
  -d client_secret=YOUR_CLIENT_SECRET \
  -d code=AUTH_CODE \
  -d grant_type=authorization_code
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your credentials
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run

```bash
python server.py
```

## MCP Client Configuration

Add to your MCP client config (e.g., Claude Desktop, Copilot CLI):

```json
{
  "mcpServers": {
    "strava": {
      "command": "python",
      "args": ["/path/to/strava-mcp-server/server.py"],
      "env": {
        "STRAVA_CLIENT_ID": "your_client_id",
        "STRAVA_CLIENT_SECRET": "your_client_secret",
        "STRAVA_REFRESH_TOKEN": "your_refresh_token"
      }
    }
  }
}
```

## License

MIT
