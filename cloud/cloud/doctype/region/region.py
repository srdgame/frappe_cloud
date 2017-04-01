# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Region(Document):
	pass


parent_type = {
	"Province": "",
	"City": "Province",
	"County": "City",
	"Town": "County",
}


def query_region(doctype, txt, searchfield, start, page_len, filters):
	filters = filters or {}

	typ = parent_type[filters["type"]] or ""
	if not filters["parent"]:
		return frappe.db.sql("""select name, description from `tabRegion`
			where type = %s and region_parent = %s
			and %s like %s order by name limit %s, %s""" %
			("%s", searchfield, "%s", "%s", "%s"),
			(typ, "%%%s%%" % txt, start, page_len), as_list=1)


def query_child_region(doctype, txt, searchfield, start, page_len, filters):
	filters = filters or {}

	return frappe.db.sql("""select name, description from `tabRegion`
		where type = %s and region_parent = %s
		and %s like %s order by name limit %s, %s""" %
		("%s", "%s", searchfield, "%s", "%s", "%s"),
		(filters["parent"], filters["parent"], "%%%s%%" % txt, start, page_len), as_list=1)

