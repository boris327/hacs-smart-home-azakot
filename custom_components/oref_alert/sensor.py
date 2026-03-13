"""Sensor platform for Oref Alert."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
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
    """Set up Oref Alert sensors."""
    coordinator: OrefAlertCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        OrefAlertStatusSensor(coordinator),
        OrefAlertZonesCountSensor(coordinator),
        OrefAlertZonesListSensor(coordinator),
        OrefAlertCategorySensor(coordinator),
        OrefAlertTitleSensor(coordinator),
        OrefAlertHistoryCountSensor(coordinator),
    ])


class OrefAlertBaseSensor(CoordinatorEntity, SensorEntity):
    """Base class for Oref Alert sensors."""

    def __init__(self, coordinator: OrefAlertCoordinator, key: str, name: str, icon: str) -> None:
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"oref_alert_{key}"
        self._attr_icon = icon

    @property
    def native_value(self):
        return self.coordinator.data.get(self._key)

    @property
    def extra_state_attributes(self):
        return {}


class OrefAlertStatusSensor(OrefAlertBaseSensor):
    def __init__(self, coordinator):
        super().__init__(coordinator, "active", "Oref Alert Status", "mdi:alert-octagon")

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


class OrefAlertZonesCountSensor(OrefAlertBaseSensor):
    def __init__(self, coordinator):
        super().__init__(coordinator, "areas_count", "Oref Alert Zones Count", "mdi:map-marker-multiple")

    @property
    def native_value(self):
        return self.coordinator.data.get("areas_count", 0)


class OrefAlertZonesListSensor(OrefAlertBaseSensor):
    def __init__(self, coordinator):
        super().__init__(coordinator, "areas_list", "Oref Alert Zones List", "mdi:map-marker-alert")

    @property
    def native_value(self):
        return self.coordinator.data.get("areas_list", "אין אזעקות פעילות")


class OrefAlertCategorySensor(OrefAlertBaseSensor):
    def __init__(self, coordinator):
        super().__init__(coordinator, "category", "Oref Alert Category", "mdi:shield-alert")


class OrefAlertTitleSensor(OrefAlertBaseSensor):
    def __init__(self, coordinator):
        super().__init__(coordinator, "title", "Oref Alert Title", "mdi:bell-alert")


class OrefAlertHistoryCountSensor(OrefAlertBaseSensor):
    def __init__(self, coordinator):
        super().__init__(coordinator, "history_count", "Oref Alert History Count", "mdi:history")

    @property
    def extra_state_attributes(self):
        return {"history": self.coordinator.data.get("history", [])}
