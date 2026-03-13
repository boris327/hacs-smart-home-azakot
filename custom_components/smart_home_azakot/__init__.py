"""Smart Home Azakot — אזעקות חכמות — Home Assistant Integration."""
from __future__ import annotations

import logging
from datetime import timedelta

import aiohttp
import async_timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

DOMAIN = "smart_home_azakot"
PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR]

OREF_ALERT_URL = "https://www.oref.org.il/WarningMessages/alert/alerts.json"
OREF_HISTORY_URL = "https://www.oref.org.il/Shared/Ajax/GetAlarmsHistory.aspx?lang=he&mode=1"

OREF_HEADERS = {
    "Referer": "https://www.oref.org.il/",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (compatible; HomeAssistant/SmartHomeAzakot)",
}

CATEGORY_MAP = {
    "1": "ירי רקטות וטילים",
    "2": "רעידת אדמה",
    "3": "חדירת כלי טיס עוין",
    "4": "אירוע חומרים מסוכנים",
    "6": "גל צונאמי",
    "13": "חדירת מחבלים",
}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Smart Home Azakot from a config entry."""
    coordinator = SmartHomeAzakotCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


class SmartHomeAzakotCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch Oref Alert data."""

    def __init__(self, hass: HomeAssistant) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=10),
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from Oref API."""
        try:
            async with async_timeout.timeout(8):
                async with aiohttp.ClientSession() as session:
                    alert_data = {}
                    try:
                        async with session.get(OREF_ALERT_URL, headers=OREF_HEADERS) as resp:
                            if resp.status == 200:
                                import json
                                text = await resp.text(encoding="utf-8-sig")
                                try:
                                    alert_data = json.loads(text) if text.strip() else {}
                                except Exception:
                                    alert_data = {}
                    except Exception as e:
                        _LOGGER.debug("Alert fetch error: %s", e)

                    history_data = []
                    try:
                        async with session.get(OREF_HISTORY_URL, headers=OREF_HEADERS) as resp:
                            if resp.status == 200:
                                import json
                                text = await resp.text(encoding="utf-8-sig")
                                try:
                                    history_data = json.loads(text) if text.strip() else []
                                except Exception:
                                    history_data = []
                    except Exception as e:
                        _LOGGER.debug("History fetch error: %s", e)

                    areas = alert_data.get("data", []) or []
                    cat = str(alert_data.get("cat", ""))

                    return {
                        "active": len(areas) > 0,
                        "areas": areas,
                        "areas_count": len(areas),
                        "areas_list": " • ".join(areas) if areas else "אין אזעקות פעילות",
                        "category": CATEGORY_MAP.get(cat, "לא ידוע") if cat else "—",
                        "category_id": cat,
                        "title": alert_data.get("title", ""),
                        "desc": alert_data.get("desc", ""),
                        "alert_id": alert_data.get("id", ""),
                        "history_count": len(history_data),
                        "history": history_data[:20],
                    }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with Oref API: {err}") from err
