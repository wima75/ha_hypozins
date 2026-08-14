"""HypozinsEntity base class."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import HypozinsDataUpdateCoordinator


class HypozinsEntity(CoordinatorEntity[HypozinsDataUpdateCoordinator]):
    """Base entity for hypozins, grouped into one device per mortgage provider."""

    def __init__(
        self,
        coordinator: HypozinsDataUpdateCoordinator,
        device_key: str,
        device_name: str,
        attribution: str,
    ) -> None:
        """Initialize the entity and assign it to its provider device."""
        super().__init__(coordinator)
        self._attr_attribution = attribution
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_key)},
            name=device_name,
        )
