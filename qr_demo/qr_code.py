from io import BytesIO
from base64 import b64encode
import barcode
import qrcode
from barcode.writer import ImageWriter
import frappe

@frappe.whitelist()
def get_barcode(data: str, doctype='') -> str:
    barcode_bytes = get_barcode_bytes(data, doctype, format="PNG")
    base_64_string = bytes_to_base64_string(barcode_bytes)

    return add_file_info(base_64_string, "image/png")

@frappe.whitelist()
def get_qr_code(data: str) -> str:
	qr_code_bytes = get_qr_code_bytes(data, format="PNG")
	base_64_string = bytes_to_base64_string(qr_code_bytes)

	return add_file_info(base_64_string, "image/png")

def add_file_info(data: str, mime_type: str) -> str:
    """Add info about the file type and encoding.

    This is required so the browser can make sense of the data."""
    return f"data:{mime_type};base64, {data}"


def get_barcode_bytes(data, doctype, format: str) -> bytes:
    """Create a barcode and return the bytes."""
    if doctype == 'Sales Invoice':
        barcode_class = barcode.get_barcode_class('code128')
    else:
        barcode_class = barcode.get_barcode_class('ean8')
    barcode_instance = barcode_class(data, writer=ImageWriter())
    barcode_image = barcode_instance.render()

    buffered = BytesIO()
    barcode_image.save(buffered, format=format)

    return buffered.getvalue()

def get_qr_code_bytes(data, format: str) -> bytes:
	"""Create a QR code and return the bytes."""
	img = qrcode.make(data)

	buffered = BytesIO()
	img.save(buffered, format=format)

	return buffered.getvalue()

def bytes_to_base64_string(data: bytes) -> str:
    """Convert bytes to a base64 encoded string."""
    return b64encode(data).decode("utf-8")
