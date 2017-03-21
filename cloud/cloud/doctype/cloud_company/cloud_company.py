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
