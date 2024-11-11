import json
import sys
from datetime import datetime

import tzlocal
from awscrt import mqtt, mqtt5
from awsiot import mqtt_connection_builder

# Read the command line args
endpoint = sys.argv[1]
certificate_filepath = sys.argv[2]
private_key_filepath = sys.argv[3]
device_name = sys.argv[4]


# Callback when the connection successfully connects
def on_connection_success(connection, callback_data):
    assert isinstance(callback_data, mqtt.OnConnectionSuccessData)
    print(
        "Connection Successful with return code: {} session present: {}".format(
            callback_data.return_code, callback_data.session_present
        )
    )


# Callback when a connection attempt fails
def on_connection_failure(connection, callback_data):
    assert isinstance(callback_data, mqtt.OnConnectionFailureData)
    print("Connection failed with error code: {}".format(callback_data.error))


# Callback when a connection has been disconnected or shutdown successfully
def on_connection_closed(connection, callback_data):
    print("Connection closed")


# Create MQTT5 client
mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=endpoint,
    cert_filepath=certificate_filepath,
    pri_key_filepath=private_key_filepath,
    client_id=device_name,
    clean_session=False,
    keep_alive_secs=30,
    on_connection_success=on_connection_success,
    on_connection_failure=on_connection_failure,
    on_connection_closed=on_connection_closed,
)
print("MQTT5 Client created")

# Connect to the MQTT broker
connect_future = mqtt_connection.connect()
connect_future.result()
print("MQTT5 Client started")

# Define the telemetry data
telemetry_data = {
    "device": device_name,
    "timestamp": datetime.now(tz=tzlocal.get_localzone()).strftime(
        "%Y-%m-%d %H:%M:%S%z"
    ),
    "temperature": 25.1,
}

# Publish the telemetry data to a specific topic
message_topic = f"$aws/things/{device_name}/telemetry"
mqtt_connection.publish(
    topic=message_topic, payload=json.dumps(telemetry_data), qos=mqtt5.QoS.AT_LEAST_ONCE
)

# Disconnect from the MQTT broker
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
print("MQTT5 Client stopped")
