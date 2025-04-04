from fastapi import FastAPI, HTTPException
from services.youtube_service import YouTubeAnalyticsService
# from services.snowflake_service import SnowflakeService
from services.stripe_service import StripeService
from services.facebook_service import FacebookService
app = FastAPI()

@app.post("/ingest/youtube-analytics")
def ingest_youtube_analytics_data(start_date: str, end_date: str, metrics: str, dimensions: str = None, filters: str = None, table: str = "youtube_analytics"):
    """
    Endpoint to fetch YouTube Analytics data and insert it into Snowflake.

    :param start_date: Start date for the report (YYYY-MM-DD)
    :param end_date: End date for the report (YYYY-MM-DD)
    :param metrics: Metrics to fetch (e.g., views, estimatedMinutesWatched)
    :param dimensions: Optional dimensions (e.g., video, country)
    :param filters: Optional filters (e.g., video==abc123)
    :param table: Snowflake table to insert data into
    """
    try:
        youtube_analytics_service = YouTubeAnalyticsService()
        # snowflake_service = SnowflakeService()

        
        # Fetch analytics data from YouTube
        data = youtube_analytics_service.get_analytics_data(
            start_date=start_date,
            end_date=end_date,
            metrics=metrics,
            dimensions=dimensions,
            filters=filters
        )

        return {"data": data}
        # Transform the data into rows for Snowflake
        # rows = []
        # for row in data["rows"]:
        #     rows.append(tuple(row))

        # Insert transformed data into Snowflake
        # snowflake_service.insert_data(table, rows)

        return {"message": "YouTube Analytics data ingested successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ingest/stripe")
def ingest_stripe_data(table: str = "stripe_analytics"):
    try:
        stripe_service = StripeService()
        # snowflake_service = SnowflakeService()
        data = stripe_service.get_transaction_data()
        # Transform data for Snowflake
        # snowflake_data = [(txn['id'], txn['amount'], txn['currency'], txn['created']) for txn in data['data']]
        # snowflake_service.insert_data(table, snowflake_data)
        return {"message": "Stripe data ingested successfully", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/ingest/facebook")
def ingest_facebook_data(page_id: str, table: str = "facebook_analytics"):
    try:
        facebook_service = FacebookService()
        # snowflake_service = SnowflakeService()
        data = facebook_service.get_page_data(page_id)
        # Transform data for Snowflake
        # snowflake_data = [(page_id, stat['name'], stat['value']) for stat in data['data']]
        # snowflake_service.insert_data(table, snowflake_data)
        return {"message": "Facebook data ingested successfully", "data":data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
