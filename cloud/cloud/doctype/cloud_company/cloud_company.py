# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class CloudCompany(Document):

	def on_update(self):
		org_admin = frappe.db.get_value("Cloud Company", {"name": self.name}, "admin")
		if org_admin != self.admin:
			user = frappe.get_doc('User', org_admin)
			user.remove_roles('Cloud User')
		user = frappe.get_doc('User', self.admin)
		user.add_roles('Cloud User')

	def on_trash(self):
		user = frappe.get_doc('User', self.admin)
		user.remove_roles('Cloud User')


def get_permission_query_conditions(user):
	if 'Cloud Manager' in frappe.get_roles(user):
		return ""

	return '''(`tabCloud Company`.admin = "{0}")'''.format(user)


def has_permission(doc, ptype, user):
	if 'Cloud Manager' in frappe.get_roles(user):
		return True

	return doc.admin == user


def list_admin_companies(user):
	if 'Cloud User' not in frappe.get_roles(user):
		return []
	return [d[0] for d in frappe.db.get_values("Cloud Company", {"admin": user}, "name")]