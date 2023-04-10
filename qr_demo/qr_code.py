from io import BytesIO
from base64 import b64encode
import barcode
from barcode.writer import ImageWriter
import frappe

@frappe.whitelist()
def get_barcode(data: str) -> str:
    barcode_bytes = get_barcode_bytes(data, format="PNG")
    base_64_string = bytes_to_base64_string(barcode_bytes)

    return add_file_info(base_64_string, "image/png")


def add_file_info(data: str, mime_type: str) -> str:
    """Add info about the file type and encoding.

    This is required so the browser can make sense of the data."""
    return f"data:{mime_type};base64, {data}"


def get_barcode_bytes(data, format: str) -> bytes:
    """Create a barcode and return the bytes."""
    barcode_class = barcode.get_barcode_class('code128')
    barcode_instance = barcode_class(data, writer=ImageWriter())
    barcode_image = barcode_instance.render()

    buffered = BytesIO()
    barcode_image.save(buffered, format=format)

    return buffered.getvalue()


def bytes_to_base64_string(data: bytes) -> str:
    """Convert bytes to a base64 encoded string."""
    return b64encode(data).decode("utf-8")
