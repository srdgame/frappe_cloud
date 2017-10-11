# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _dict, throw, _
from frappe.model.document import Document


class Region(Document):
	def validate(self):
		if self.type != "Province" and not self.region_parent:
			throw(_("Region Parent is required!"))

		brothers = [d[0] for d in frappe.db.get_values('Region', {"region_parent": self.region_parent, "name":("!=", self.name)}, "region_name")]
		if self.region_name in brothers:
			throw(_("Duplicated Region Name Found"))

		self.description = self.region_name
		rgn = self.region_parent
		while rgn:
			self.description = frappe.get_value("Region", rgn, "region_name") + " " + self.description
			rgn = frappe.get_value("Region", rgn, "region_parent")


parent_type = {
	"Province": "",
	"City": "Province",
	"County": "City",
	"Town": "County",
}


@frappe.whitelist()
def query_region(doctype, txt, searchfield, start, page_len, filters):
	typ = parent_type[filters.get("type")] or ""
	return frappe.db.sql("""select name, description from `tabRegion`
		where type = %s
		and %s like %s order by name limit %s, %s""" %
		("%s", searchfield, "%s", "%s", "%s"),
		(typ, "%%%s%%" % txt, start, page_len), as_list=1)


@frappe.whitelist()
def query_child_region(doctype, txt, searchfield, start, page_len, filters):

	parent = filters.get("parent")
	type = filters.get("type")
	if not parent:
		return frappe.db.sql("""select name, description from `tabRegion`
			where type = %s
			and %s like %s order by name limit %s, %s""" %
			("%s", searchfield, "%s", "%s", "%s"),
			(type, "%%%s%%" % txt, start, page_len), as_list=1)

	return frappe.db.sql("""select name, description from `tabRegion`
		where type = %s and region_parent = %s
		and %s like %s order by name limit %s, %s""" %
		("%s", "%s", searchfield, "%s", "%s", "%s"),
		(type, parent, "%%%s%%" % txt, start, page_len), as_list=1)

