# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Cloud"),
			"items": [
				{
					"type": "doctype",
					"name": "Cloud Company",
					"onboard": 1,
					"description": _("Cloud Company"),
				},
				{
					"type": "doctype",
					"name": "Cloud Company Requisition",
					"onboard": 1,
					"description": _("Cloud Company"),
				},
				{
					"type": "doctype",
					"name": "Cloud Company Group",
					"onboard": 1,
					"description": _("Cloud Company Group"),
				},
				{
					"type": "doctype",
					"name": "Cloud Employee",
					"onboard": 1,
					"description": _("Cloud Employee"),
				},
				{
					"type": "doctype",
					"name": "Cloud Employee Invitation",
					"onboard": 1,
					"description": _("Cloud Employee Invitation"),
				}
			]
		},
		{
			"label": _("Cloud Settings"),
			"items": [
				{
					"type": "doctype",
					"name": "Cloud Settings",
					"onboard": 1,
					"description": _("Cloud Settings"),
				},
				{
					"type": "doctype",
					"name": "Cloud Permission",
					"onboard": 1,
					"description": _("Cloud Permission"),
				},
				{
					"type": "doctype",
					"name": "Cloud User Role",
					"onboard": 1,
					"description": _("Cloud User Role"),
				}
			]
		},
		{
			"label": _("Others"),
			"items": [
				{
					"type": "doctype",
					"name": "Cloud Project",
					"onboard": 1,
					"description": _("Cloud Project"),
				},
				{
					"type": "doctype",
					"name": "Cloud Project Site",
					"onboard": 1,
					"description": _("Cloud Project"),
				},
				{
					"type": "doctype",
					"name": "Region",
					"onboard": 1,
					"description": _("Region"),
				},
				{
					"type": "doctype",
					"name": "Region Address",
					"onboard": 1,
					"description": _("Region Address"),
				}
			]
		}
	]
