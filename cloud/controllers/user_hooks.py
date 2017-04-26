# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe


def after_insert(doc, method):
	cloud_settings = frappe.get_doc('Cloud Settings', 'Cloud Settings')
	doc.add_roles(cloud_settings.role_list)

