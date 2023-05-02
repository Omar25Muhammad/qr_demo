from io import BytesIO
from base64 import b64encode
import base64
import barcode
import qrcode
from barcode.writer import ImageWriter
from PIL import Image
import zbar
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
        barcode_class = barcode.get_barcode_class('code39')
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


@frappe.whitelist()
def add_barcode(barcode, docname):
    doc1 = frappe.get_doc('Item', docname)
    docs2 = frappe.get_all('Item Price', filters={'item_code': docname}, pluck='name')
    founds = [0, 0]

    for i in doc1.barcodes:
        if i.barcode == barcode:
            founds[0] = 1
            break

    for doc2 in docs2:
        doc2 = frappe.get_doc('Item Price', doc2)
        for i in doc2.barcodes:
            if i.barcode == barcode:
                founds[1] = 1
                break
        
    if all(founds):
         return 'Found!'
    
    if not founds[0]:
        doc1.append('barcodes', {'barcode': barcode})
        doc1.save()
    
    if not founds[1]:
        doc2.append('barcodes', {'barcode': barcode})
        doc2.save()

    frappe.db.commit()

    return 'Done!'
    

@frappe.whitelist()
def scan_barcode(doc):

    base64_string = frappe.get_doc('QR Demo', doc).qr_code
    
    # Decode the base64 string into bytes
    image_bytes = base64.b64decode(base64_string.split(',')[1])

    # Load the bytes as an image using PIL
    image = Image.open(BytesIO(image_bytes))

    # Convert the image to grayscale
    image = image.convert('L')

    # Create a barcode scanner
    scanner = zbar.Scanner()

    # Scan the image for barcodes
    results = scanner.scan(image)

    # Return the barcode data
    if results:
        # frappe.set_value('QR Demo', frappe.get_doc('QR Demo', doc).name, 'barcode', results[0].data.decode('utf-8'))
        # frappe.get_doc('QR Demo', doc).save()
        # frappe.db.commit()

        return results[0].data.decode('utf-8')