# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from cloud.cloud.doctype.cloud_settings.cloud_settings import CloudSettings

class CloudCompany(Document):

	def on_update(self):
		org_admin = frappe.db.get_value("Cloud Company", {"name": self.name}, "admin")
		if org_admin != self.admin:
			self.run_method("on_admin_remove", user=org_admin)
		self.run_method("on_admin_insert", user=self.admin)

	def on_trash(self):
		self.run_method("on_admin_remove", user=self.admin)

	def on_admin_insert(self, user):
		user = frappe.get_doc('User', user)
		user.add_roles('Cloud User')

	def on_admin_remove(self, user):
		user = frappe.get_doc('User', user)
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
	return [d[0] for d in frappe.db.get_values("Cloud Company", {"admin": user, "enabled": 1}, "name")]


def list_user_companies(user):
	clist = []
	for d in frappe.db.get_values("Cloud Company", {"admin": user, "enabled": 1}, "name"):
		clist.append(d[0])
	for d in frappe.db.get_values("Cloud Employee", {"user": user}, "company"):
		if frappe.db.get_value("Cloud Company", d[0], "enabled") == 1:
			clist.append(d[0])

	return clist

def list_users(company):
	if frappe.db.get_value("Cloud Company", company, "enabled") != 1:
		return

	users = []
	for d in frappe.db.get_values("Cloud Company Group", {"company":company}, "name"):
		for d in frappe.db.get_values("Cloud Company GroupUser", {"parent": d[0]}, "user"):
			users.append(d[0])

	return users


def get_domain(company):
	return frappe.get_value("Cloud Company", company, "domain")


def get_wechat_app(company):
	app = CloudSettings.get_default_wechat_app()
	if frappe.db.get_value("Cloud Company", company, "wechat") == 1:
		app = frappe.db.get_value("Cloud Company", company, "wechat_app") or app

	return app