# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version
from frappe import _

app_name = "cloud"
app_title = "Cloud"
app_publisher = "Dirk Chang"
app_description = "Cloud App Common Base"
app_icon = "fa fa-users"
app_color = "green"
app_email = "dirk.chang@symid.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/cloud/css/cloud.css"
# app_include_js = "/assets/cloud/js/cloud.js"

# include js, css files in header of web template
# web_include_css = "/assets/cloud/css/cloud.css"
# web_include_js = "/assets/cloud/js/cloud.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "cloud.utils.get_home_page"

# Website Route Rules
website_route_rules = [
	{"from_route": "/cloud_companies", "to_route": "Cloud Company"},
	{"from_route": "/cloud_companies/<path:name>", "to_route": "cloud_company",
		"defaults": {
			"doctype": "Cloud Company",
			"parents": [{"title": _("Cloud Companies"), "name": "cloud_companies"}]
		}
	},
	{"from_route": "/cloud_company_groups/<path:name>", "to_route": "cloud_company_group",
		"defaults": {
			"doctype": "Cloud Company Group",
			"parents": [{"title": _("Cloud Companies"), "name": "cloud_company_groups"}]
		}
	},
]

portal_menu_items = [
	{"title": _("Cloud Companies"), "route": "/cloud_companies", "reference_doctype": "Cloud Company",
		"role": "Cloud User"},
	{"title": _("Cloud Employees"), "route": "/cloud_employees", "reference_doctype": "Cloud Employee",
		"role": "Cloud User"}
]

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "cloud.install.before_install"
# after_install = "cloud.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "cloud.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

permission_query_conditions = {
	"Cloud Company": "cloud.cloud.doctype.cloud_company.cloud_company.get_permission_query_conditions",
	"Cloud Company Group": "cloud.cloud.doctype.cloud_company_group.cloud_company_group.get_permission_query_conditions",
}

has_permission = {
	"Cloud Company": "cloud.cloud.doctype.cloud_company.cloud_company.has_permission",
	"Cloud Company Group": "cloud.cloud.doctype.cloud_company_group.cloud_company_group.has_permission",
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"cloud.tasks.all"
# 	],
# 	"daily": [
# 		"cloud.tasks.daily"
# 	],
# 	"hourly": [
# 		"cloud.tasks.hourly"
# 	],
# 	"weekly": [
# 		"cloud.tasks.weekly"
# 	]
# 	"monthly": [
# 		"cloud.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "cloud.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "cloud.event.get_events"
# }

