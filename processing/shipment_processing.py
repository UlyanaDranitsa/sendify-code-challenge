import asyncio

from processing.context_manager import browser_manager
from dtos.model import ShipmentInfo
from error_handling.exceptions import ShipmentFormatError, ShipmentNotFoundError, ShipmentFetchingError


def handle_response_statuses(response, ref_num):
    match response.status:
        case 429:
            return None
        case 400:
            return ShipmentFormatError(ref_num)
        case 404:
            return ShipmentNotFoundError(ref_num)
        case _:
            return ShipmentFetchingError(ref_num)

async def get_shipment_info(reference_num: str) -> dict | None:
    async with browser_manager() as page:
        data = None
        exception = None
        finished = asyncio.Event()

        async def handle_response(response):
            nonlocal data, exception
            url = response.url

            if "/tracking-public/shipments?query=" in url:
                if response.status != 200 and response.status != 429:
                    exception = handle_response_statuses(response, reference_num)
                    finished.set()

            elif "/tracking-public/shipments/land/" in url:
                if response.status == 200:
                    data = await response.json()
                else:
                    exception = handle_response_statuses(response, reference_num)

                if response.status != 429:
                    finished.set()

        page.on("response", handle_response)

        await page.goto("https://www.dbschenker.com/app/tracking-public/")

        button = page.get_by_role("button", name="Allow All Cookies")
        if await button.is_visible():
            await button.click()

        await page.get_by_placeholder("Enter Your Reference Number").fill(reference_num)
        await page.get_by_role("button", name="Search").click()

        try:
            await asyncio.wait_for(finished.wait(), timeout=10)
        except asyncio.TimeoutError:
            raise ShipmentFetchingError(reference_num)

        page.remove_listener("response", handle_response)

        if exception:
            raise exception

        return data

def parse_shipment(json: dict) -> ShipmentInfo | None:
    shipment = ShipmentInfo.model_validate(json)
    return shipment