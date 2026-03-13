"""Config flow for Oref Alert integration."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from . import DOMAIN


class OrefAlertConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Oref Alert."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        # Only one instance allowed
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            return self.async_create_entry(
                title="פיקוד העורף — Oref Alert",
                data={},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),
            description_placeholders={
                "info": "לחץ על אישור להתקנת האינטגרציה. לא נדרשת הגדרה נוספת."
            },
        )
