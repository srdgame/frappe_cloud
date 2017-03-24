# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _
from frappe.model.document import Document
from cloud.cloud.doctype.cloud_company.cloud_company import list_admin_companies


class CloudProject(Document):
	pass


def get_project_list(doctype, txt, filters, limit_start, limit_page_length=20, order_by="modified desc"):
	ent_list = list_admin_companies(frappe.session.user)

	return frappe.db.sql('''select *
		from `tabCloud Project`
		where
			company in {2}
			order by %(order_by)s
			limit {0}, {1}
		'''.format(limit_start, limit_page_length, "('"+"','".join(ent_list)+"')"),
			{'order_by': order_by},
			as_dict=True,
			update={'doctype':'Cloud Project'})


def get_list_context(context=None):
	return {
		"show_sidebar": True,
		"show_search": True,
		"no_breadcrumbs": True,
		"title": _("Your Projects"),
		"get_list": get_project_list,
		"row_template": "templates/generators/cloud_project_row.html",
	}

def get_permission_query_conditions(user):
	if 'Cloud Manager' in frappe.get_roles(user):
		return ""

	ent_list = list_admin_companies(user)

	return """(`tabCloud Project`.company in ({ent_list}))""".format(
		ent_list='"' + '", "'.join(ent_list) + '"')


def has_permission(doc, ptype, user):
	if 'Cloud Manager' in frappe.get_roles(user):
		return True

	if frappe.get_value('Cloud Company', {'admin': user, 'name': doc.company}):
		return True

	return False


def list_admin_projects(user, check_enable=True):
	ent_list = list_admin_companies(user)
	filters = {"company": ["in", ent_list]}
	if check_enable:
		filters["enabled"] = 1
	return [d[0] for d in frappe.db.get_values("Cloud Project", )]
