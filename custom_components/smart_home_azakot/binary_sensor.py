"""Binary sensor for Smart Home Azakot."""
from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DOMAIN, SmartHomeAzakotCoordinator


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([AzakotActiveBinarySensor(coordinator)])


class AzakotActiveBinarySensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Azakot Active"
        self._attr_unique_id = "smart_home_azakot_active"
        self._attr_device_class = BinarySensorDeviceClass.SAFETY

    @property
    def is_on(self):
        return bool(self.coordinator.data.get("active", False))

    @property
    def icon(self):
        return "mdi:alert-octagon" if self.is_on else "mdi:shield-check"

    @property
    def extra_state_attributes(self):
        d = self.coordinator.data
        return {
            "areas": d.get("areas", []),
            "areas_count": d.get("areas_count", 0),
            "category": d.get("category", ""),
            "title": d.get("title", ""),
        }
