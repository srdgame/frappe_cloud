# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class CloudSettings(Document):
	@staticmethod
	def get_default_company():
		return frappe.db.get_single_value("Cloud Settings", "default_cloud_company")

	@staticmethod
	def get_default_wechat_app():
		return frappe.db.get_single_value("Cloud Settings", "default_wechat_app")