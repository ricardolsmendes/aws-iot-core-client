# Most of this code is based on the aws-iot-device-sdk-python-v2 sample available at
# https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/samples/pubsub.py.

import json
import random
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


# Create a MQTT connection from the command line data
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

print(f"Connecting to {endpoint} with client ID '{device_name}'...")
connect_future = mqtt_connection.connect()
# Future.result() waits until a result is available
connect_future.result()

# Define the telemetry data
temperature = random.uniform(23, 26)
telemetry_data = {
    "device": device_name,
    "timestamp": datetime.now(tz=tzlocal.get_localzone()).strftime(
        "%Y-%m-%d %H:%M:%S%z"
    ),
    "temperature": temperature,
}

# Publish the telemetry data to a specific topic
message_topic = f"$aws/things/{device_name}/telemetry"
print(f"Publishing message with temperature {temperature} to topic {message_topic}")
mqtt_connection.publish(
    topic=message_topic, payload=json.dumps(telemetry_data), qos=mqtt5.QoS.AT_LEAST_ONCE
)

# Disconnect
print("Disconnecting...")
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()
