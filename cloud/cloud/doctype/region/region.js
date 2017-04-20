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
		if(frm.doc.type != "Town") {
			frm.add_custom_button(__('Create Sub Region'), function () {
				frappe.model.with_doctype('Region', function() {
					var mr = frappe.model.get_new_doc('Region');
					mr.region_parent = frm.doc.name;
					if (frm.doc.type == "Province") { mr.type = "City"}
					if (frm.doc.type == "City") { mr.type = "County"}
					if (frm.doc.type == "County") { mr.type = "Town"}
					frappe.set_route('Form', mr.doctype, mr.name);
				});
			});

			frm.custom_buttons[__("Create Sub Region")].removeClass("btn-default");
			frm.custom_buttons[__("Create Sub Region")].addClass("btn-primary");
		}
	}
});
