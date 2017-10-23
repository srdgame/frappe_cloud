# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import time


def after_insert(doc, method):
	frappe.enqueue('cloud.controllers.user_hooks.insert_user_roles', user=doc.name, sleep=3)


def insert_user_roles(user, sleep=None):
	if sleep:
		time.sleep(sleep)
	cloud_settings = frappe.get_doc('Cloud Settings', 'Cloud Settings')
	doc = frappe.get_doc("User", user)
	if len(cloud_settings.role_list) > 0:
		roles = [d.role for d in cloud_settings.role_list]
		doc.add_roles(*roles)

