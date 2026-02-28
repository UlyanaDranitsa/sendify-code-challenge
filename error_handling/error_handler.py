import functools
from typing import Callable, Any
from mcp.types import TextContent

from error_handling.exceptions import ShipmentError


def mcp_tool_error_handler(func: Callable) -> Callable:
    """
    Decorator for error handling inside mcp tool
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except ShipmentError as e:
            return [TextContent(type="text", text=str(e))]
        except Exception as e:
            return [TextContent(type="text", text="Unknown error occurred during shipment processing")]

    return wrapper