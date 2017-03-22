# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _
from frappe.model.document import Document

class CloudEmployee(Document):
	pass


def add_employee(user, company):
	if frappe.get_value("Cloud Employee", {"company": company, "user": user}):
		return True
	if not frappe.get_value("Cloud Company", {"name": company, "admin": frappe.session.user}):
		throw(_("You not the admin of company {0}").format(company))

	doc = frappe.get_doc({
		        "doctype": "Cloud Employee",
		        "user": user,
		        "login_name": "iMbEhIDE"  # login_name
	})
	doc.insert(ignore_permissions=True)
	frappe.db.commit()

	return _("Employee has ben added")