// Copyright (c) 2022, ALYF GmbH and contributors
// For license information, please see license.txt

let barcode = '';
let original_barcode = '';

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
					{
						original_barcode = r.message
						console.log('The original: ' + original_barcode)
						barcode = r.message.replace(r.message[0], '9')
						frm.call({
							method: "qr_demo.qr_code.get_barcode",
							args: { data: barcode },
							callback: function (rt) {
								r.message = r.message + '1' 
								console.log(typeof(r.message))
								console.log(r.message)
								console.log(rt.message)
								frm.doc.qr_code = rt.message;
								frm.refresh_fields();
							}
						})
				}
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
		// console.log('ok')
		// console.log(frm.doc.price_list)
		if ((frm.doc.item_code) && (frm.doc.uom)) {
				frm.call({
					doc: frm.doc,
					method: "the_price",
					args: {price_list: frm.doc.price_list, item_barcode: original_barcode, uom: frm.doc.uom},
					callback: function (response) { 
						console.log(original_barcode)
							console.log(response.message)
							frm.doc.item_price = response.message
							frm.refresh_fields()
						
						
					}
				})
		}
		else {
			frm.doc.price_list = ''
			frappe.msgprint('الرجاء التأكّد من اختيار كل من الصنف ووحدة الكمية')
			frm.refresh_fields()
		}
	},
	after_save: function (frm) {
		frm.call({
							method: 'qr_demo.qr_code.scan_barcode',
							args: { doc: frm.doc.name },
							callback: function (ft) {
								console.log(ft.message)
							frm.call({
								method: 'qr_demo.qr_code.add_barcode',
								args: { barcode: ft.message, docname: frm.doc.item_code },
								callback: function (f) {
									console.log(f.message)
								}
							});

								
							}
						});
	}
});
