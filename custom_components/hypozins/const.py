"""Constants for hypozins."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "hypozins"

POSTFINANCE_DEVICE_KEY = "postfinance"
POSTFINANCE_DEVICE_NAME = "Postfinance Hypotheken"
POSTFINANCE_ATTRIBUTION = "Data provided by postfinance.ch"

BPK_DEVICE_KEY = "bpk"
BPK_DEVICE_NAME = "BPK Hypotheken"
BPK_ATTRIBUTION = "Data provided by bpk.ch"

SNB_DEVICE_KEY = "snb"
SNB_DEVICE_NAME = "SNB Referenzzinssätze"
SNB_ATTRIBUTION = "Data provided by snb.ch"
