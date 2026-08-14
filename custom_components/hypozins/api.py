"""API client to fetch Swiss mortgage interest rates from Postfinance and BPK."""

from __future__ import annotations

import asyncio
import re
import socket

import aiohttp
from bs4 import BeautifulSoup

POSTFINANCE_URL = "https://www.postfinance.ch/de/privat/finanzieren/hypotheken/zinssaetze-hypotheken.html"
BPK_URL = "https://bpk.ch/hypotheken/aktuelle-zinssaetze"

_WHITESPACE_RE = re.compile(r"\s+")
_BPK_LAUFZEIT_RE = re.compile(r"^(\d+)\s*Jahre?\s*:\s*([\d.,]+)\s*%$")
_SARON_MARGE_RE = re.compile(r"Marge von\s*([\d.,]+)\s*%")

_EXPECTED_LAUFZEIT_VALUE_COUNT = 2


class HypozinsApiClientError(Exception):
    """Exception to indicate a general API error."""


class HypozinsApiClientCommunicationError(HypozinsApiClientError):
    """Exception to indicate a communication error."""


class HypozinsApiClientParsingError(HypozinsApiClientError):
    """Exception to indicate the fetched page could not be parsed as expected."""


def _normalize(text: str) -> str:
    return _WHITESPACE_RE.sub(" ", text.replace("\xa0", " ")).strip()


def _parse_rate(text: str) -> float:
    match = re.search(r"(\d+[.,]\d+|\d+)", text)
    if not match:
        msg = f"Zinssatz konnte nicht geparst werden: '{text}'"
        raise HypozinsApiClientParsingError(msg)
    return float(match.group(1).replace(",", "."))


class HypozinsApiClient:
    """Client to fetch mortgage interest rates from Postfinance and BPK."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialize the API client."""
        self._session = session

    async def async_get_data(self) -> dict[str, float]:
        """Fetch and parse all mortgage rates."""
        postfinance_html, bpk_html = await asyncio.gather(
            self._fetch(POSTFINANCE_URL),
            self._fetch(BPK_URL),
        )
        data: dict[str, float] = {}
        data.update(self._parse_postfinance(postfinance_html))
        data.update(self._parse_bpk(bpk_html))
        return data

    async def _fetch(self, url: str) -> str:
        """Fetch the raw HTML for a URL."""
        try:
            async with asyncio.timeout(10):
                response = await self._session.get(url)
                response.raise_for_status()
                return await response.text()
        except TimeoutError as exception:
            msg = f"Timeout error fetching information from {url} - {exception}"
            raise HypozinsApiClientCommunicationError(msg) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information from {url} - {exception}"
            raise HypozinsApiClientCommunicationError(msg) from exception

    def _parse_postfinance(self, html: str) -> dict[str, float]:
        """Parse the 2- and 5-year fixed mortgage rates from Postfinance."""
        soup = BeautifulSoup(html, "lxml")
        table_div = soup.find("div", id="e3d1f3")
        if table_div is None:
            msg = "Postfinance: Tabelle mit id='e3d1f3' nicht gefunden"
            raise HypozinsApiClientParsingError(msg)

        rates: dict[str, float] = {}
        for row in table_div.find_all("tr"):
            values = row.find_all("div", class_="table--value")
            if len(values) != _EXPECTED_LAUFZEIT_VALUE_COUNT:
                continue
            laufzeit = _normalize(values[0].get_text(strip=True))
            rates[laufzeit] = _parse_rate(values[1].get_text(strip=True))

        result: dict[str, float] = {}
        laufzeit_keys = (("2 Jahre", "postfinance_2j"), ("5 Jahre", "postfinance_5j"))
        for laufzeit, key in laufzeit_keys:
            if laufzeit not in rates:
                msg = f"Postfinance: Laufzeit '{laufzeit}' nicht gefunden"
                raise HypozinsApiClientParsingError(msg)
            result[key] = rates[laufzeit]
        return result

    def _parse_bpk(self, html: str) -> dict[str, float]:
        """Parse the 3-/5-year fixed mortgage rates and the SARON margin from BPK."""
        soup = BeautifulSoup(html, "lxml")
        paragraphs = [
            _normalize(p.get_text(" ", strip=True)) for p in soup.find_all("p")
        ]

        laufzeit_rates: dict[str, float] = {}
        for text in paragraphs:
            match = _BPK_LAUFZEIT_RE.match(text)
            if match:
                laufzeit_rates[match.group(1)] = float(match.group(2).replace(",", "."))

        result: dict[str, float] = {}
        for jahre, key in (("3", "bpk_3j"), ("5", "bpk_5j")):
            if jahre not in laufzeit_rates:
                msg = f"BPK: Laufzeit '{jahre} Jahre' nicht gefunden"
                raise HypozinsApiClientParsingError(msg)
            result[key] = laufzeit_rates[jahre]

        for text in paragraphs:
            match = _SARON_MARGE_RE.search(text)
            if match:
                result["bpk_saron_marge"] = float(match.group(1).replace(",", "."))
                break
        else:
            msg = "BPK: SARON-Marge nicht gefunden"
            raise HypozinsApiClientParsingError(msg)

        return result
