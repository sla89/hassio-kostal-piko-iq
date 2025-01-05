"""Config flow for Kostal Plenticore Solar Inverter integration."""

import logging
from typing import Any

from aiohttp.client_exceptions import ClientError
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_BASE, CONF_HOST, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .helper import KostalRestClient

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


def test_connection(data):
    """Test the connection to the inverter.

    Data has the keys from DATA_SCHEMA with values provided by the user.
    """
    client = KostalRestClient(data["host"], data["password"])
    client.login()

class KostalPikoIQConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Kostal PIKO IQ Solar Inverter."""

    VERSION = 1
    MINOR_VERSION = 20

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            hostname = data[CONF_HOST]
            password = data[CONF_PASSWORD]

            self._async_abort_entries_match({CONF_HOST: hostname})

            try:
                test_connection(user_input)
            except Exception as ex:
                _LOGGER.exception("Got error response trying to connect: %s", ex)
                errors[CONF_BASE] = "unknown"
            else:
                return self.async_create_entry(title=hostname, data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )