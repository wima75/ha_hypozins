"""
Custom integration to fetch Swiss mortgage interest rates.

Tracks fixed-rate mortgage rates from Postfinance and BPK.
"""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration

from .api import HypozinsApiClient
from .const import DOMAIN, LOGGER
from .coordinator import HypozinsDataUpdateCoordinator
from .data import HypozinsData

if TYPE_CHECKING:
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
        update_interval=timedelta(hours=12),
        config_entry=entry,
    )
    entry.runtime_data = HypozinsData(
        client=HypozinsApiClient(session=async_get_clientsession(hass)),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: HypozinsConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
