# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "aptronics"
app_title = "Aptronics Applications"
app_publisher = "Aptronics"
app_description = "All applications and modules used at Aptronics"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "hemant@aptronics.co.za"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/aptronics/css/aptronics.css"
# app_include_js = "/assets/aptronics/js/aptronics.js"

# include js, css files in header of web template
# web_include_css = "/assets/aptronics/css/aptronics.css"
# web_include_js = "/assets/aptronics/js/aptronics.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "aptronics.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "aptronics.install.before_install"
# after_install = "aptronics.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "aptronics.notifications.get_notification_config"

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

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
 	"Sales Invoice": {
 		"before_save": "aptronics.stock.actual_cost.get_actual_cost_by_batch",
 #		"on_submit": "aptronics.stock.actual_cost.reversal_shipment_not_invoiced",
	},
  #"Delivery Note": {
	#	"on_submit": "aptronics.stock.actual_cost.shipped_not_invoiced",
	#},
	#"GL Entry": {
	#	"before_insert":"aptronics.stock.actual_cost.gl_entry_insert"
	#},
	#"Stock Ledger Entry":{
	#	"before_insert":"aptronics.stock.actual_cost.update_lot"
	#},
	#"Batch": {
	#	"before_insert": "aptronics.stock.actual_cost.update_lot"
	#}
	"Communication": {
		"before_insert" : "aptronics.business_rules.email.check_email_address"
	},
	"Customer":{
		"autoname":"aptronics.business_rules.naming_series.business_partner_naming_series"
	}
 }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"aptronics.tasks.all"
# 	],
# 	"daily": [
# 		"aptronics.tasks.daily"
# 	],
# 	"hourly": [
# 		"aptronics.tasks.hourly"
# 	],
# 	"weekly": [
# 		"aptronics.tasks.weekly"
# 	]
# 	"monthly": [
# 		"aptronics.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "aptronics.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "aptronics.event.get_events"
# }

