# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _
from frappe.model.document import Document

class CloudEmployee(Document):
	pass


def on_doctype_update():
	"""Add indexes in `Cloud Employee`"""
	frappe.db.add_index("Cloud Employee", ["company"])


@frappe.whitelist()
def add_employee(user, company):
	comp = frappe.get_value("Cloud Employee", {"user": user}, "company")
	if comp:
		if comp != company:
			throw(_("User in in another company {0}").format(comp))
		return True

	if not frappe.get_value("Cloud Company", {"name": company, "admin": frappe.session.user}):
		throw(_("You not the admin of company {0}").format(company))

	doc = frappe.get_doc({
		"doctype": "Cloud Employee",
		"user": user,
		"company": company
	})
	doc.insert(ignore_permissions=True)
	frappe.db.commit()

	return _("Employee has ben added")


@frappe.whitelist()
def delete_employee(user, company):
	if not frappe.get_value("Cloud Company", {"name": company, "admin": frappe.session.user}):
		throw(_("You not the admin of company {0}").format(company))

	frappe.delete_doc("Cloud Employee", user, ignore_permissions=True)

	return _("Employee has been deleted")


def query_employee(doctype, txt, searchfield, start, page_len, filters):
	return frappe.db.sql("""select distinct employee.name, concat_ws(' ', user.first_name, user.middle_name, user.last_name) 
		from `tabCloud Employee` employee, `tabUser` user 
		where employee.company = %s and employee.name = user.name
		and employee.%s like %s order by employee.name limit %s, %s""" %
		("%s", searchfield, "%s", "%s", "%s"),
		(filters["company"], "%%%s%%" % txt, start, page_len), as_list=1)


def get_permission_query_conditions(user):
	if 'Cloud Manager' in frappe.get_roles(user):
		return ""
	from cloud.cloud.doctype.cloud_company.cloud_company import list_admin_companies

	ent_list = list_admin_companies(user)

	return """(`tabCloud Employee`.company in ({user_ents}))""".format(
		user_ents='"' + '", "'.join(ent_list) + '"')


def has_permission(doc, ptype, user):
	if 'Cloud Manager' in frappe.get_roles(user):
		return True

	if frappe.get_value('Cloud Company', {'admin': user, 'name': doc.company}):
		return True

	return False