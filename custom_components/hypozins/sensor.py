"""Sensor platform for hypozins."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE

from .const import (
    BPK_ATTRIBUTION,
    BPK_DEVICE_KEY,
    BPK_DEVICE_NAME,
    POSTFINANCE_ATTRIBUTION,
    POSTFINANCE_DEVICE_KEY,
    POSTFINANCE_DEVICE_NAME,
)
from .entity import HypozinsEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import HypozinsDataUpdateCoordinator
    from .data import HypozinsConfigEntry


@dataclass(frozen=True, kw_only=True)
class HypozinsSensorEntityDescription(SensorEntityDescription):
    """Describes a hypozins mortgage rate sensor."""

    device_key: str
    device_name: str
    attribution: str


ENTITY_DESCRIPTIONS: tuple[HypozinsSensorEntityDescription, ...] = (
    HypozinsSensorEntityDescription(
        key="postfinance_2j",
        name="Festhypothek 2 Jahre",
        icon="mdi:home-percent",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        device_key=POSTFINANCE_DEVICE_KEY,
        device_name=POSTFINANCE_DEVICE_NAME,
        attribution=POSTFINANCE_ATTRIBUTION,
    ),
    HypozinsSensorEntityDescription(
        key="postfinance_5j",
        name="Festhypothek 5 Jahre",
        icon="mdi:home-percent",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        device_key=POSTFINANCE_DEVICE_KEY,
        device_name=POSTFINANCE_DEVICE_NAME,
        attribution=POSTFINANCE_ATTRIBUTION,
    ),
    HypozinsSensorEntityDescription(
        key="bpk_3j",
        name="Festhypothek 3 Jahre",
        icon="mdi:home-percent",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        device_key=BPK_DEVICE_KEY,
        device_name=BPK_DEVICE_NAME,
        attribution=BPK_ATTRIBUTION,
    ),
    HypozinsSensorEntityDescription(
        key="bpk_5j",
        name="Festhypothek 5 Jahre",
        icon="mdi:home-percent",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        device_key=BPK_DEVICE_KEY,
        device_name=BPK_DEVICE_NAME,
        attribution=BPK_ATTRIBUTION,
    ),
    HypozinsSensorEntityDescription(
        key="bpk_saron_marge",
        name="SARON Hypothek Marge",
        icon="mdi:home-percent",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        device_key=BPK_DEVICE_KEY,
        device_name=BPK_DEVICE_NAME,
        attribution=BPK_ATTRIBUTION,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: HypozinsConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        HypozinsSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class HypozinsSensor(HypozinsEntity, SensorEntity):
    """hypozins mortgage rate sensor."""

    entity_description: HypozinsSensorEntityDescription

    def __init__(
        self,
        coordinator: HypozinsDataUpdateCoordinator,
        entity_description: HypozinsSensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(
            coordinator,
            device_key=entity_description.device_key,
            device_name=entity_description.device_name,
            attribution=entity_description.attribution,
        )
        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}_{entity_description.key}"
        )

    @property
    def native_value(self) -> float | None:
        """Return the native value of the sensor."""
        return self.coordinator.data.get(self.entity_description.key)
