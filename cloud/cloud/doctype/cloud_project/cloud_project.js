// Copyright (c) 2017, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cloud Project', {
	setup: function(frm) {
		frm.fields_dict["group"].get_query = function(doc){
			return {
				filters: {"company": doc.company}
			};
		};
	},
	refresh: function(frm) {

	},
	company: function (frm) {
		frm.set_value("group", null);
	}
});
