"""Binary sensor platform for Oref Alert."""
from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DOMAIN, OrefAlertCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Oref Alert binary sensors."""
    coordinator: OrefAlertCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([OrefAlertActiveBinarySensor(coordinator)])


class OrefAlertActiveBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor — True when alert is active."""

    def __init__(self, coordinator: OrefAlertCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_name = "Oref Alert Active"
        self._attr_unique_id = "oref_alert_active"
        self._attr_device_class = BinarySensorDeviceClass.SAFETY

    @property
    def is_on(self) -> bool:
        return bool(self.coordinator.data.get("active", False))

    @property
    def icon(self) -> str:
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
