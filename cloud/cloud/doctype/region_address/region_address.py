# -*- coding: utf-8 -*-
# Copyright (c) 2017, Dirk Chang and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document


class RegionAddress(Document):
	def is_region_of(self, region):
		if self.town == region:
			return True
		if self.county == region:
			return True
		if self.city == region:
			return True
		if self.province == region:
			return True
		return False


@frappe.whitelist()
def get_address_text(province, city=None, county=None, town=None, address=None):
	province_name = frappe.get_value("Region", province, "region_name") or ""
	city_name = frappe.get_value("Region", city, "region_name") or ""
	county_name = frappe.get_value("Region", county, "region_name") or ""
	town_name = frappe.get_value("Region", town, "region_name") or ""
	return " ".join([province_name, city_name, county_name, town_name, address or ""])