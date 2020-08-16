# -*- coding: utf-8 -*-
# Copyright (c) 2020, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
import json
from frappe import _
from frappe.desk.page.setup_wizard.setup_wizard import make_records


def get_setup_stages(args=None):
	stages = [
		{
			'status': _('Setting up cloud company'),
			'fail_msg': _('Failed to setup cloud company'),
			'tasks': [
				{
					'fn': setup_company,
					'args': args,
					'fail_msg': _("Failed to setup cloud company")
				}
			]
		},
		{
			'status': _('Setting cloud defaults'),
			'fail_msg': 'Failed to set cloud defaults',
			'tasks': [
				{
					'fn': setup_defaults,
					'args': args,
					'fail_msg': _("Failed to setup cloud defaults")
				},
			]
		}
	]

	return stages


def setup_company(args):
	records = [
		# Cloud Company
		{
			'doctype': "Cloud Company",
			'comp_name': args.company_name,
			'full_name': args.company_full_name,
			'domain': args.company_domain,
			'admin': args.get("email") or 'dirk@kooiot.com'
		},

		# Company Employee
		{
			"doctype": "Cloud Employee",
			'company': args.company_name,
			'user': args.get("email") or 'dirk@kooiot.com'
		},

		# Company Company Group
		{
			"doctype": "Cloud Company Group",
			'company': args.company_name,
			'group_name': 'root',
			'enabled': 1
		}
	]
	make_records(records)


def setup_defaults(args):
	perms = json.loads(
		open(frappe.get_app_path("cloud", "setup", "setup_wizard", "data", "cloud_permission.json")).read())
	for d in perms:
		d.update({
			"doctype": "Cloud Permission"
		})
		frappe.get_doc(d).insert(ignore_permissions=True)

	roles = json.loads(
		open(frappe.get_app_path("cloud", "setup", "setup_wizard", "data", "cloud_user_role.json")).read())
	for d in roles:
		d.update({
			"doctype": "Cloud User Role"
		})
		frappe.get_doc(d).insert(ignore_permissions=True)

	settings = frappe.get_doc("Cloud Settings")
	settings.set("default_cloud_company", args.company_name)
	settings.append("role_list", {"role": "IOT User"})
	settings.append("role_list", {"role": "App User"})
	settings.save()


# Only for programmatical use
def setup_complete(args=None):
	setup_company(args)
	setup_defaults(args)
