# aws-iot-core-client

A Python client for AWS IoT Core.

## Usage instructions

1. Set up the IoT infrastructure using the
   [companion Terraform repository](https://github.com/ricardolsmendes/aws-iot-sandbox-infra).
2. Create, activate, and set up Python a virtual environment:
   ```shell
   python -m venv env
   source ./env/bin/activate
   pip install -r requirements.txt
   ```
3. Run the script of your choice as follows.

### publish.py

Simulates a thermometer sending temperature values to the IoT Core endpoint.

```shell
python publish.py <ENDPOINT> <CERTIFICATE-PATH> <PRIVATE-KEY-PATH> simulated-thermometer-<dev|staging|prod>
```

## How to contribute

Please make sure to take a moment and read the [Code of
Conduct](https://github.com/ricardolsmendes/aws-iot-core-client/blob/main/.github/CODE_OF_CONDUCT.md).

### Report issues

Please report bugs and suggest features via the [GitHub
Issues](https://github.com/ricardolsmendes/aws-iot-core-client/issues).

Before opening an issue, search the tracker for possible duplicates. If you find a
duplicate, please add a comment saying that you encountered the problem as well.

### Contribute code

Please make sure to read the [Contributing
Guide](https://github.com/ricardolsmendes/aws-iot-core-client/blob/main/.github/CONTRIBUTING.md)
before making a pull request.
