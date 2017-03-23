# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw, _
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


def get_company_list(doctype, txt, filters, limit_start, limit_page_length=20, order_by="modified desc"):
	return frappe.db.sql('''select *
		from `tabCloud Company`
		where
			admin = %(user)s
			order by %(order_by)s
			limit {0}, {1}
		'''.format(limit_start, limit_page_length),
			{'user':frappe.session.user, 'order_by': order_by},
			as_dict=True,
			update={'doctype':'Cloud Company'})


def get_list_context(context=None):
	return {
		"show_sidebar": True,
		"show_search": True,
		"no_breadcrumbs": True,
		"title": _("Your Companies"),
		#"introduction": _('The Cloud Companies those you can manage!'),
		"get_list": get_company_list,
		"row_template": "templates/generators/cloud_company_row.html",
	}

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
	comp = frappe.db.get_value("Cloud Employee", {"user": user}, "company")
	if frappe.db.get_value("Cloud Company", comp, "enabled") == 1:
		clist.append(comp)

	return clist

def list_users(company):
	if frappe.db.get_value("Cloud Company", company, "enabled") != 1:
		return

	users = []
	for d in frappe.db.get_values("Cloud Company Group", {"company":company}, "name"):
		for d in frappe.db.get_values("Cloud Company GroupUser", {"parent": d[0]}, "user"):
			users.append(d[0])

	return users


def list_groups(company):
	return [d[0] for d in frappe.db.get_values("Cloud Company Group", {"company": company})]


def list_groups_obj(company):
	return frappe.get_all('Cloud Company Group', filters={"company": company}, fields=["name", "group_name", "enabled", "modified"])


def get_domain(company):
	return frappe.get_value("Cloud Company", company, "domain")


def get_wechat_app(company):
	app = CloudSettings.get_default_wechat_app()
	if frappe.db.get_value("Cloud Company", company, "wechat") == 1:
		app = frappe.db.get_value("Cloud Company", company, "wechat_app") or app

	return app