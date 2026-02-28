class ShipmentError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class ShipmentNotFoundError(ShipmentError):
    def __init__(self, ref_number: str):
        message = f"Shipment {ref_number} not found"
        super().__init__(message)

class ShipmentFormatError(ShipmentError):
    def __init__(self, ref_number: str):
        message = f"Shipment {ref_number} had incorrect format"
        super().__init__(message)

class ShipmentFetchingError(ShipmentError):
    def __init__(self, ref_number: str):
        message = f"Unknown error occurred during fetching shipment {ref_number}"
        super().__init__(message)

