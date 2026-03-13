"""Sensor platform for Smart Home Azakot."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DOMAIN, SmartHomeAzakotCoordinator


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        AzakotStatusSensor(coordinator),
        AzakotZonesCountSensor(coordinator),
        AzakotZonesListSensor(coordinator),
        AzakotCategorySensor(coordinator),
        AzakotTitleSensor(coordinator),
        AzakotHistoryCountSensor(coordinator),
    ])


class AzakotBaseSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, key, name, icon):
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"smart_home_azakot_{key}"
        self._attr_icon = icon

    @property
    def native_value(self):
        return self.coordinator.data.get(self._key)


class AzakotStatusSensor(AzakotBaseSensor):
    def __init__(self, c):
        super().__init__(c, "active", "Azakot Status", "mdi:alert-octagon")

    @property
    def native_value(self):
        return "active" if self.coordinator.data.get("active") else "clear"

    @property
    def extra_state_attributes(self):
        d = self.coordinator.data
        return {
            "areas": d.get("areas", []),
            "title": d.get("title", ""),
            "desc": d.get("desc", ""),
            "category": d.get("category", ""),
            "alert_id": d.get("alert_id", ""),
        }


class AzakotZonesCountSensor(AzakotBaseSensor):
    def __init__(self, c):
        super().__init__(c, "areas_count", "Azakot Zones Count", "mdi:map-marker-multiple")

    @property
    def native_value(self):
        return self.coordinator.data.get("areas_count", 0)


class AzakotZonesListSensor(AzakotBaseSensor):
    def __init__(self, c):
        super().__init__(c, "areas_list", "Azakot Zones List", "mdi:map-marker-alert")


class AzakotCategorySensor(AzakotBaseSensor):
    def __init__(self, c):
        super().__init__(c, "category", "Azakot Category", "mdi:shield-alert")


class AzakotTitleSensor(AzakotBaseSensor):
    def __init__(self, c):
        super().__init__(c, "title", "Azakot Title", "mdi:bell-alert")


class AzakotHistoryCountSensor(AzakotBaseSensor):
    def __init__(self, c):
        super().__init__(c, "history_count", "Azakot History Count", "mdi:history")

    @property
    def extra_state_attributes(self):
        return {"history": self.coordinator.data.get("history", [])}
