// Copyright (c) 2017, Dirk Chang and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cloud Project Site', {
	setup: function (frm) {
		frm.fields_dict['address'].grid.get_field("province").get_query = function (doc, cdt, cdn) {
			return {
				query: "cloud.cloud.doctype.region.region.query_child_region",
				filters: {"type": "Province"}
			};
		};
		frm.fields_dict['address'].grid.get_field("city").get_query = function (doc, cdt, cdn) {
			var d = locals[cdt][cdn];
			return {
				query: "cloud.cloud.doctype.region.region.query_child_region",
				filters: {"type": "City", "parent": d.province}
			};
		};
		frm.fields_dict['address'].grid.get_field("county").get_query = function (doc, cdt, cdn) {
			var d = locals[cdt][cdn];
			return {
				query: "cloud.cloud.doctype.region.region.query_child_region",
				filters: {"type": "County", "parent": d.city}
			};
		};
		frm.fields_dict['address'].grid.get_field("town").get_query = function (doc, cdt, cdn) {
			var d = locals[cdt][cdn];
			return {
				query: "cloud.cloud.doctype.region.region.query_child_region",
				filters: {"type": "Town", "parent": d.county}
			};
		};
		frm.fields_dict['address'].grid.cannot_add_rows = true;
	},
	refresh: function(frm) {
		if (frm.doc.naming_series == 'CELL-') {
			frm.set_read_only();
		}
	},
	update_address: function(frm, row) {
		frappe.call({
			type: "GET",
			method: "cloud.cloud.doctype.region_address.region_address.get_address_text",
			args: row,
			callback: function (r, rt) {
				if (r.message) {
					frm.set_value("address_text", r.message)
				}
			}
		});
	}
});


frappe.ui.form.on('Region Address', {
	province: function (doc, cdt, cdn) {
		var d = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "city", "");
		frappe.model.set_value(cdt, cdn, "county", "");
		frappe.model.set_value(cdt, cdn, "town", "");
		cur_frm.events.update_address(cur_frm, d);
	},
	city: function (doc, cdt, cdn) {
		var d = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "county", "");
		frappe.model.set_value(cdt, cdn, "town", "");
		cur_frm.events.update_address(cur_frm, d);
	},
	county: function (doc, cdt, cdn) {
		var d = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "town", "");
		cur_frm.events.update_address(cur_frm, d);
	},
	town: function (doc, cdt, cdn) {
		var d = locals[cdt][cdn];
		cur_frm.events.update_address(cur_frm, d);
	},
	address: function (doc, cdt, cdn) {
		var d = locals[cdt][cdn];
		cur_frm.events.update_address(cur_frm, d);
	}
});