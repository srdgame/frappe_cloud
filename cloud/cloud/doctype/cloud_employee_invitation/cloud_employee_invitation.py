# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class CloudEmployeeInvitation(Document):
	def on_submit(self):
		data = {
			"doctype": "Cloud Employee",
			"company": self.company,
			"user": self.user
		}
		frappe.get_doc(data).insert(ignore_permissions=True)


def get_permission_query_conditions(user):
	if 'Cloud Manager' in frappe.get_roles(user):
		return ""
	from cloud.cloud.doctype.cloud_company.cloud_company import list_admin_companies

	if 'Cloud Admin' in frappe.get_roles(user):
		ent_list = list_admin_companies(user)

		return """(`tabCloud Employee Invitation`.company in ({user_ents}))""".format(
			user_ents='"' + '", "'.join(ent_list) + '"')
	else:
		return '''(`tabCloud Employee Invitation`.user = '{user}')'''.format(user=user)


def has_permission(doc, ptype, user):
	if 'Cloud Manager' in frappe.get_roles(user):
		return True

	if frappe.get_value('Cloud Company', {'admin': user, 'name': doc.company}):
		return True

	if doc.user == user:
		if ptype in ['create', 'cancel']:
			return False
		else:
			return True

	return False