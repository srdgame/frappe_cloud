# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _dict, throw, _
from frappe.model.document import Document
from cloud.cloud.doctype.cloud_company.cloud_company import list_admin_companies


class CloudCompanyGroup(Document):
	def validate(self):
		list = _dict()
		for d in self.user_list:
			if list.get(d.user):
				throw(_("Duplicated user found! {0}").format(d.user))
			list[d.user] = d


def get_permission_query_conditions(user):
	if 'Cloud Manager' in frappe.get_roles(user):
		return ""

	ent_list = list_admin_companies(user)

	return """(`tabCloud Company Group`.company in ({user_ents}))""".format(
		user_ents='"' + '", "'.join(ent_list) + '"')


def has_permission(doc, ptype, user):
	if 'Cloud Manager' in frappe.get_roles(user):
		return True

	if frappe.get_value('Cloud Company', {'admin': user, 'name': doc.company}):
		return True

	return False


def list_user_groups(user, check_enable=True):
	groups = []
	appended_groups = []
	for d in frappe.db.get_values("Cloud Company GroupUser", {"user": user}, ["parent", "role", "modified", "creation"]):
		if frappe.get_value("Cloud Company Group", d[0], "enabled"):
			groups.append(_dict({"name": d[0], "role": d[1], "modified": d[2], "creation": d[3], "user": user}))
			appended_groups.append(d[0])
	for comp in list_admin_companies(user):
		for d in frappe.db.get_values("Cloud Company Group", {"company": comp, "enabled": 1}, "name"):
			if d[0] not in appended_groups:
				groups.append(_dict({"name": d[0], "role": "Admin", "user": user}))

	return groups


def list_users(group, check_enable=True):
	users = []
	for d in frappe.db.get_values("Cloud Company GroupUser", {"parent": group}, ["user", "role", "modified", "creation"]):
		users.append(_dict({"name": d[0], "role": d[1], "modified": d[2], "creation": d[3], "group": group}))

	return users
