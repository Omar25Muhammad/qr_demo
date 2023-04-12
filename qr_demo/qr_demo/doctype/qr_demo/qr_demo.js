// Copyright (c) 2022, ALYF GmbH and contributors
// For license information, please see license.txt

frappe.ui.form.on('QR Demo', {
	refresh: function (frm) {
		frm.set_query('price_list', function (frm) {
			return {
				filters: { selling: 1 }
			}
		});
	},
		
	item_code: function (frm) {
		if (frm.doc.item_code)
			frm.call({
				doc: frm.doc,
				method: "the_barcode",
				callback: function (r) {
					console.log(r.message);
					// frm.doc.item_barcode = r.message
					// frm.refresh_fields('item_barcode')
					if (r.message != -1)
						frm.call({
							method: "qr_demo.qr_code.get_barcode",
							args: { data: r.message },
							callback: function (rt) {
								console.log(rt.message)
								frm.doc.qr_code = rt.message;
								frm.refresh_fields();
							}
						})
					else {
						frappe.msgprint('الباركود يجب أن يبدء بـ66 وبطول 7 أرقام')
						frm.doc.item_code = '';
						frm.doc.qr_image = '';
						frm.refresh_fields();
					}
				}
			})
	},
		
	price_list: function (frm) {
		if (frm.doc.item_code) {
				frm.call({
					doc: frm.doc,
					args: {price_list: frm.doc.price_list},
					method: "the_price",
					callback: function (response) { 
						console.log(response.message)
					}
				})
			}
		}
});
