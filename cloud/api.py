# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import os
import requests
from frappe import throw, msgprint, _
from werkzeug.utils import secure_filename
from cloud.doctype.cloud_settings.cloud_settings import CloudSettings


def valid_auth_code(auth_code=None):
	if 'Guest' != frappe.session.user:
		return
	auth_code = auth_code or frappe.get_request_header("AuthorizationCode")
	if not auth_code:
		throw(_("AuthorizationCode is required in HTTP Header!"))
	frappe.logger(__name__).debug(_("AuthorizationCode as {0}").format(auth_code))

	user = CloudSettings.get_on_behalf(auth_code)
	if not user:
		throw(_("Authorization Code is incorrect!"))
	# form dict keeping
	form_dict = frappe.local.form_dict
	frappe.set_user(user)
	frappe.local.form_dict = form_dict


@frappe.whitelist(allow_guest=True)
def list_statistics_companies():
	'''
	Cloud statistics enabled when company owner has created its user auth code
	:return:
	'''
	valid_auth_code()

	list = []
	companies = frappe.get_all("Cloud Company", fields=["name", "admin", "domain", "enabled"])
	for comp in companies:
		auth_code = frappe.get_value("IOT User Api", comp.admin, "authorization_code")
		if auth_code and comp.enabled == 1:
			list.append({
				'company': comp.name,
				'auth_code': auth_code,
				'database': comp.domain,
				'enable': 1,
			})
		else:
			list.append({
				'company': comp.name,
				'auth_code': 'UNKNOWN',
				'database': comp.domain,
				'enable': 0,
			})

	return list

