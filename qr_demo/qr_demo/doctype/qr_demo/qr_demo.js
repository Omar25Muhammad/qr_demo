// Copyright (c) 2022, ALYF GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('QR Demo', {
	// refresh: function(frm) {

	// },
		item_code: function (frm) {
		if (frm.doc.item_code)
			frm.call({
				doc: frm.doc,
				method: "the_barcode",
				callback: function (r) {
					console.log(r.message)
					// frm.doc.item_barcode = r.message
					// frm.refresh_fields('item_barcode')

					frm.call({
						method: "qr_demo.qr_code.get_barcode",
						args: { data: r.message },
						callback: function (rt) {
							console.log(rt.message)
							frm.doc.qr_code = rt.message
							frm.refresh_fields()
						}
					})
				}
			})
	},
});
