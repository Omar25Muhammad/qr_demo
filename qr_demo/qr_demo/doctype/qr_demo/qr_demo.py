# Copyright (c) 2022, ALYF GmbH and contributors
# For license information, please see license.txt
from frappe.model.document import Document

from qr_demo.qr_code import get_barcode
import frappe

class QRDemo(Document):

	@frappe.whitelist()
	def the_barcode(self):
		for barcode in frappe.get_doc('Item', self.item_code).barcodes:
			if len(barcode.barcode) == 7 and barcode.barcode.startswith('66'):
				return barcode.barcode
		else:
			return -1
		
	def validate(self):
		...
		# self.qr_code = get_barcode(self.title)
