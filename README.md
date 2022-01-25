# Home Assistant Kostal PIKO IQ Inverter Integration

This integration connects to the REST API of the Kostal PIKO IQ inverter
to get the same data that are displayed on the web interface.

Thank you very much to https://www.msxfaq.de/sonst/iot/kostal15.htm for providing all the necessary information.

For some Kostal API information see the [API description](docs/api.yaml).

This integration uses the RESTful API of the inverter to make the information available in Home Assistant. You can access it via `http://INVERTER_IP/api/v1/`.

It is an easy task to extend this integration to provide all available values (like the values of each phase).
So far I didn't need them and therefore I have only added the values I am interested in.

Feel free to open a pull request or a ticket in case of any questions.

This integration integrated and has modified some parts of the [Kostal Plenticore library](https://github.com/ITTV-tools/kostalplenticorepy). Thanks for that great work.

According to my knowledge the Kostal Plenticore API differs from the Kostal Plenticore Plus / PIKO IQ REST API. That is why I have written this integration. It should work for both PIKO IQ and Plenticore Plus inverters but not for Plenticore inverters.

## Installation
### HACS
Not yet supported

### Manual installation
1. Download the source code of this repository.
1. Open the folder of your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` folder there, you need to create it.
1. Copy the content of the `custom_components` folder of the downloaded archive into your HA `custom_components` folder.
1. Restart Home Assistant
1. Add to the sensor list in your `configuration.yaml` file (or where ever you specify sensors):
    ```yaml
    # Example configuration.yaml entry
    sensor:
      - platform: kostal_piko_iq
        host: IP_OF_YOUR_INVERTER
        password: YOUR_PASSWORT
    ```

    > **Note:** Please ensure to read the [Home Assistant Secrets handling documentation](https://www.home-assistant.io/docs/configuration/secrets/) carefully and follow its instructions. It is at least recommended to use a `secrets.yaml` file.
1. Ensure that your configuration is valid
1. Restart Home Assistant

# Disclaimer
The code within this repository comes with no guarantee, the use of this code is your responsibility.

> I and any contributor to this repository take **NO** responsibility and/or liability for how you choose to use any of the source code available here. **By using any of the files available in this repository, you understand that you are AGREEING TO USE AT YOUR OWN RISK.**