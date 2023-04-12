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
	

	@frappe.whitelist()
	def the_price(self, price_list, item_barcode, uom):
		item_prices = frappe.db.sql("""
        SELECT ip.price_list_rate, ip.uom
        FROM `tabItem Price` ip
        LEFT JOIN `tabItem Barcode PL` ibp ON ibp.parent = ip.name
        WHERE ip.price_list = %s AND ibp.barcode = %s
    """, (price_list, item_barcode))
		
		item_prices = list(set(item_prices))

		the_price = [value for value, unit in item_prices if unit == uom][0]

		return the_price
	

	def validate(self):
		...
		# self.qr_code = get_barcode(self.title)
