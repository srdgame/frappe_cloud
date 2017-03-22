# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class CloudCompanyGroup(Document):
	pass


def get_permission_query_conditions(user):
	if 'Cloud Manager' in frappe.get_roles(user):
		return ""

	ent_list = [d[0] for d in frappe.db.get_values("Cloud Company", {"admin": user}, "name")]

	return """(`tabCloud Company Group`.company in ({user_ents}))""".format(
		user_ents='"' + '", "'.join(ent_list) + '"')


def has_permission(doc, ptype, user):
	if 'Cloud Manager' in frappe.get_roles(user):
		return True

	if frappe.get_value('Cloud Company', {'admin': user, 'name': doc.company}):
		return True

	return False


def list_user_groups(user):
	return frappe.db.get_values("Cloud Company GroupUser", {"user": user}, ["parent", "group", "role"])
