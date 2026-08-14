"""Custom types for hypozins."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import HypozinsApiClient
    from .coordinator import HypozinsDataUpdateCoordinator


type HypozinsConfigEntry = ConfigEntry[HypozinsData]


@dataclass
class HypozinsData:
    """Data for the hypozins integration."""

    client: HypozinsApiClient
    coordinator: HypozinsDataUpdateCoordinator
    integration: Integration
