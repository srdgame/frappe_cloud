// Copyright (c) 2017, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cloud Project Site', {
	refresh: function(frm) {
		if (frm.doc.naming_series == 'CELL-') {
			frm.set_read_only();
		}
	}
});
