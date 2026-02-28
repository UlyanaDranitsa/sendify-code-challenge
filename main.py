from mcp.server.fastmcp import FastMCP
from error_handling.error_handler import mcp_tool_error_handler
from processing.shipment_processing import parse_shipment, get_shipment_info

mcp = FastMCP("db-sсhenker")

@mcp_tool_error_handler
@mcp.tool()
async def get_shipment_object(reference_num: str) -> str | None:
    """
        Retrieves and parses tracking information for a DB Schenker shipment.

        Args:
            reference_num (str): The shipment reference or tracking number.
        """
    shipment_info_dict = await get_shipment_info(reference_num)
    shipment_object = parse_shipment(shipment_info_dict)
    json_string = shipment_object.model_dump_json()
    return json_string

def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
