"""DataUpdateCoordinator for hypozins."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import HypozinsApiClientError

if TYPE_CHECKING:
    from .data import HypozinsConfigEntry


class HypozinsDataUpdateCoordinator(DataUpdateCoordinator[dict[str, float]]):
    """Class to manage fetching mortgage rate data."""

    config_entry: HypozinsConfigEntry

    async def _async_update_data(self) -> dict[str, float]:
        """Update data via library."""
        try:
            return await self.config_entry.runtime_data.client.async_get_data()
        except HypozinsApiClientError as exception:
            raise UpdateFailed(exception) from exception
