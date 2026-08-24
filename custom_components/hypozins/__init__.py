"""
Custom integration to fetch Swiss mortgage interest rates.

Tracks fixed-rate mortgage rates from Postfinance and BPK.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_change
from homeassistant.loader import async_get_loaded_integration

from .api import HypozinsApiClient
from .const import DOMAIN, LOGGER
from .coordinator import HypozinsDataUpdateCoordinator
from .data import HypozinsData

if TYPE_CHECKING:
    from datetime import datetime

    from homeassistant.core import HomeAssistant

    from .data import HypozinsConfigEntry

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HypozinsConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = HypozinsDataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        config_entry=entry,
    )
    entry.runtime_data = HypozinsData(
        client=HypozinsApiClient(session=async_get_clientsession(hass)),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    await coordinator.async_config_entry_first_refresh()

    async def _async_scheduled_refresh(_now: datetime) -> None:
        """Refresh the coordinator data on the daily schedule."""
        await coordinator.async_request_refresh()

    entry.async_on_unload(
        async_track_time_change(
            hass,
            _async_scheduled_refresh,
            hour=16,
            minute=30,
            second=0,
        )
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: HypozinsConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
