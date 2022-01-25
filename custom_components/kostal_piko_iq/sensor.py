"""Kostal PIKO IQ Inverter."""

import logging

from datetime import timedelta
import voluptuous as vol
from dataclasses import dataclass

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import (SensorEntity, PLATFORM_SCHEMA)

from homeassistant.const import (CONF_HOST, CONF_PASSWORD, ENERGY_KILO_WATT_HOUR)
from homeassistant.util import Throttle

from .const import (
    SENSOR_DESCRIPTIONS,
    KostalSensorEntityDescription,
)
from .helper import KostalRestClient

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=10)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_PASSWORD): cv.string
})

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Kostal Piko IQ Inverter platform."""
    host = config[CONF_HOST]
    password = config[CONF_PASSWORD]

    try:
        _LOGGER.info(f'Connecting to Kostal Piko IQ Inverter...')
        client = KostalRestClient(host, password)
        client.login()
    except Exception as err:
        _LOGGER.error(f'Could not connect to Kostal PIKO IQ Inverter: {err}')
        return

    _LOGGER.info(f'Setting up Kostal Piko IQ Inverter sensors...')
    sensors = []
    for description in SENSOR_DESCRIPTIONS:
        sensors.append(
            KostalSensor(client=client, description=description))

    async_add_entities(sensors)


class KostalSensor(SensorEntity):
    """Representation of the Kostal Sensor."""

    def __init__(self, client: KostalRestClient, description: KostalSensorEntityDescription):
        """Initialize the sensor."""
        self.entity_description = description.description

        self.client = client
        self._module_id = description.module_id
        self._value_id = description.value_id

        self.update()

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        try:
            self._attr_native_value = self.getData()
            self._attr_available = True
        except Exception as err:
            _LOGGER.error(
                f"Failed updating Kostal sensor {self.entity_description.name}: {err}")
            self._attr_available = False

    def getData(self):
        """Get sensor data from inverter."""
        value = self.client.getProcessdata(
            self._module_id, [self._value_id])

        if not value:
            raise Exception(
                f"Error during updating sensor {self.entity_description.name}")

        value = value[0]["value"]
        if self.entity_description.native_unit_of_measurement == ENERGY_KILO_WATT_HOUR:
            return round(float(value / 1000), 2)
        else:
            return round(float(value), 2)


