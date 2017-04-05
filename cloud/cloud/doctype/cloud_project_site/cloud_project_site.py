# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _
from frappe.model.document import Document
from cloud.cloud.doctype.cloud_project.cloud_project import list_admin_projects


class CloudProjectSite(Document):
	pass


def get_project_list(doctype, txt, filters, limit_start, limit_page_length=20, order_by="modified desc"):
	prj_list = list_admin_projects(frappe.session.user)

	return frappe.db.sql('''select *
		from `tabCloud Project Site`
		where
			project in {2}
			order by %(order_by)s
			limit {0}, {1}
		'''.format(limit_start, limit_page_length, "('"+"','".join(prj_list)+"')"),
			{'order_by': order_by},
			as_dict=True,
			update={'doctype':'Cloud Project Site'})


def get_list_context(context=None):
	return {
		"show_sidebar": True,
		"show_search": True,
		"no_breadcrumbs": True,
		"title": _("Your Project Sites"),
		"get_list": get_project_list,
		"row_template": "templates/generators/cloud_project_site_row.html",
	}


def get_permission_query_conditions(user):
	if 'Cloud Manager' in frappe.get_roles(user):
		return ""

	prj_list = list_admin_projects(frappe.session.user)

	return """(`tabCloud Project Site`.project in ({prj_list}))""".format(
		prj_list='"' + '", "'.join(prj_list) + '"')


def has_permission(doc, ptype, user):
	if 'Cloud Manager' in frappe.get_roles(user):
		return True

	prj_list = list_admin_projects(user)

	return doc.project in prj_list


def list_admin_sites(user, check_enable=True):
	projects = list_admin_projects(user)
	if len(projects) == 0:
		return []
	filters = {"project": ["in", projects]}
	if check_enable:
		filters["enabled"] = 1
	return [d[0] for d in frappe.db.get_values("Cloud Project Site", filters=filters)]