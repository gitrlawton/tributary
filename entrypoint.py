# The contents below scaffold a Flask server within the
# container.


import json
import redis as redis
from flask import Flask, request
from loguru import logger

# We'll keep track of the 10 most recent temperature
# readings.
HISTORY_LENGTH = 10
DATA_KEY = "engine_temperature"

# Create a Flask server, and allow us to interact with
# it using the app variable.
app = Flask(__name__)

# Define an endpoint which accepts POST requests and is
# reachable from the /record endpoint.
@app.route('/record', methods=['POST'])
def record_engine_temperature():
        # Extract the JSON payload from the request.
        payload = request.get_json(force=True)
        logger.info(f"(*) record request --- {json.dumps(payload)} (*)")

        # Extract the engine temperature from the payload.
        engine_temperature = payload.get("engine_temperature")
        logger.info(f"engine temperature to record is: {engine_temperature}")

        # Open up a connection to the Redis database, which
        # is running in a different container.
        database = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
        # Push the current engine temperature reading to a
        # Redis list.
        database.lpush(DATA_KEY, engine_temperature)
        logger.info(f"stashed engine temperature in redis: {engine_temperature}")

        # If the length of our list is greater than 10, pop
        # the oldest one.
        while database.llen(DATA_KEY) > HISTORY_LENGTH:
            database.rpop(DATA_KEY)
        # Extract the current values in the list for logging.
        engine_temperature_values = database.lrange(DATA_KEY, 0, -1)
        logger.info(f"engine temperature list now contains these values: {engine_temperature_values}")

        logger.info(f"record request successful")
        # return a json payload, and a 200 status code to the client
        return {"success": True}, 200

@app.route('/collect', methods=['GET'])
def collect_engine_temperature():
        database = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
        # Retrieve the most recent reading from the database.
        current_engine_temperature = database.lindex(DATA_KEY, 0)

        sum = 0
        for reading in database.lrange(DATA_KEY, 0, -1):
                sum += float(reading)

        average_engine_temperature = sum / database.llen(DATA_KEY)



        return {"current engine temperature": current_engine_temperature, "average engine temperature" : average_engine_temperature}, 200