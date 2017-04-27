# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def after_insert(doc, method):
	cloud_settings = frappe.get_doc('Cloud Settings', 'Cloud Settings')
	if len(cloud_settings.role_list) > 0:
		roles = [d.role for d in cloud_settings.role_list]
		doc.add_roles(*roles)

