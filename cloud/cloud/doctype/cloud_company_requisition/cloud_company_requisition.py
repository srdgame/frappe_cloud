# -*- coding: utf-8 -*-
# Copyright (c) 2019, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import throw
from frappe.model.document import Document


class CloudCompanyRequisition(Document):
	def validate(self):
		if self.docstatus == 0:
			if frappe.db.exits("Cloud Company", {"comp_name": self.comp_name, "name": ('!=', self.name)}):
				throw("company_duplicated_comp_name")

			if frappe.db.exits("Cloud Company", {"full_name": self.full_name, "name": ('!=', self.name)}):
				throw("company_duplicated_full_name")

			if frappe.db.exits("Cloud Company", {"domain": self.domain, "name": ('!=', self.name)}):
				throw("company_duplicated_domain")

		'''
		if self.domain != self.admin.split("@")[1]:
			throw("company_domain_must_be_same_as_admin_email_domain")
		'''

		if frappe.db.exists("Cloud Company Requisition",
							{"comp_name": self.comp_name, "docstatus": ('!=', '1'), "name": ('!=', self.name)}):
			throw('company_requisition_duplicated_comp_name')

		if frappe.db.exists("Cloud Company Requisition",
							{"full_name": self.full_name, "docstatus": ('!=', '1'), "name": ('!=', self.name)}):
			throw('company_requisition_duplicated_full_name')

		if frappe.db.exists("Cloud Company Requisition",
							{"domain": self.domain, "docstatus": ('!=', '1'), "name": ('!=', self.name)}):
			throw('company_requisition_duplicated_domain')

		if frappe.db.exists("Cloud Company Requisition",
							{"credit_code": self.credit_code, "docstatus": ('!=', '1'), "name": ('!=', self.name)}):
			throw('company_requisition_duplicated_credit_code')

		if frappe.db.exists("Cloud Company Requisition",
							{"telephone": self.telephone, "docstatus": ('!=', '1'), "name": ('!=', self.name)}):
			throw('company_requisition_duplicated_telephone')

	def on_submit(self):
		data = {
			"doctype": "Cloud Company",
			"comp_name": self.comp_name,
			"full_name": self.full_name,
			"domain": self.domain,
			"admin": self.admin,
			"address": self.address,
			"contact": self.telephone,
			"enabled": 1,
			"wechat": 0
		}
		frappe.get_doc(data).insert()

