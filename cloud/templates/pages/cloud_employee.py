# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe import _
from cloud.cloud.doctype.cloud_company.cloud_company import list_admin_companies


def is_company_admin(user, company):
	return company in list_admin_companies(user)


def get_context(context):
	# if frappe.form_dict.new:

	name = frappe.form_dict.user or frappe.form_dict.name
	if not name:
		frappe.local.flags.redirect_location = "/me"
		raise frappe.Redirect

	user_roles = frappe.get_roles()
	if 'IOT User' not in user_roles or frappe.session.user == 'Guest':
		raise frappe.PermissionError("Your account is not an IOT User!")
		
	context.no_cache = 1
	context.show_sidebar = True
	# Get target user document object
	doc = frappe.get_doc('Cloud Employee', name)
	# Check for Company permission
	if not is_company_admin(frappe.session.user, doc.get("company")):
		raise frappe.PermissionError("Your account is not company admin!")

	doc.has_permission('read')

	context.parents = [{"title": _("Back"), "route": frappe.get_request_header("referer")}]
	context.user_doc = frappe.get_doc("User", doc.user)
	context.doc = doc
