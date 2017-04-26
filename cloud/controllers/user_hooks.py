# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe


def after_insert(doc, method):
	cloud_settings = frappe.get_doc('Cloud Settings', 'Cloud Settings')
	if len(cloud_settings.role_list) > 0:
		roles = [d.role for d in cloud_settings.role_list]
		doc.add_roles(*roles)

