// Copyright (c) 2017, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('Region', {
	setup: function(frm) {
		frm.fields_dict['region_parent'].get_query  = function(){
			return {
				query:"cloud.cloud.doctype.region.region.query_region",
				filters: {"type": frm.doc.type}
			};
		};
	},
	refresh: function(frm) {

	}
});
