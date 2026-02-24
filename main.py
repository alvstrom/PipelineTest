from fastapi import FastAPI, HTTPException
import httpx

app= FastAPI(title="weather-api wrapper")


#health check endpoint
@app.get("/")
def read_root():
    """Health check endpoint to prove the server is running."""
    return {"status": "healthy", "service": "weather-wrapper-api"}


@app.get("/weather/helsinki")
async def get_weather_helsinki():
    """Fetches live weather data for Helsinki and strips out the junk."""
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 60.1695,
        "longitude": 24.9354,
        "current": "temperature_2m,wind_speed_10m",
        "timezone": "Europe/Helsinki"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            raw_data = response.json()
            
            current = raw_data.get("current", {})
            
            return {
                "location": "Helsinki, Finland",
                "temperature_celsius": current.get("temperature_2m"),
                "wind_speed_kmh": current.get("wind_speed_10m"),
                "timestamp": current.get("time")
            }
            
        except httpx.RequestError:
            # If the external API goes down
            raise HTTPException(status_code=500, detail="Failed to fetch weather data")
        
        