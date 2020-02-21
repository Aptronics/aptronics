# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "aptronics"
app_title = "Aptronics"
app_publisher = "Aptronics"
app_description = "All applications and modules used at Aptronics"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "hemant@aptronics.co.za"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/aptronics/css/aptronics.css"
app_logo_url = '/assets/aptronics/images/eoh_lettermark.png'
app_include_js = "/assets/js/aptronics.min.js"

website_context = {
	"favicon": '/assets/aptronics/images/favicon.png',
	"splash_image": "/assets/aptronics/images/eoh_wordmark.png"
}

# include js, css files in header of web template
# web_include_css = "/assets/aptronics/css/aptronics.css"
# web_include_js = "/assets/aptronics/js/aptronics.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Delivery Note": "public/js/custom/delivery_note_custom.js",
			"Sales Invoice": "public/js/custom/sales_invoice_custom.js",
			"Purchase Invoice": "public/js/custom/purchase_invoice_custom.js",
			"Purchase Receipt": "public/js/custom/purchase_receipt_custom.js",
			"Purchase Order": "public/js/custom/purchase_order_custom.js",
			"Sales Order": "public/js/custom/sales_order_custom.js",
			"Quotation": "public/js/custom/quotation_custom.js"}

doctype_list_js = {"Sales Order": "public/js/custom/sales_order_list.js",
					"Purchase Order": "public/js/custom/purchase_order_list.js"
					}
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


# before_install = "aptronics.patches.create_delivery_note_workflow.execute"
# after_install = "aptronics"

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
	"Sales Order": {
		"validate": [
			"aptronics.workflows.check_so_backorder_status",
			"aptronics.business_rules.validations.sales_order_unique_by_customer"
		],
		"before_print": "aptronics.bundling.merge_bundled_items"
	},
	"Purchase Order": {
		"before_insert": "aptronics.workflows.reset_doc_title_if_amended",
		"on_submit": "aptronics.workflows.update_so_with_dropship_po",
		"on_cancel": "aptronics.workflows.unlink_dropship_po"
	},
	"Communication": {
		"before_insert": "aptronics.business_rules.email.check_email_address"
	},
	"Customer": {
		"before_insert": "aptronics.business_rules.naming_series.business_partner_naming_series"
	},
	"Supplier": {
		"before_insert": "aptronics.business_rules.naming_series.business_partner_naming_series"
	},
	"Purchase Invoice": {
		"validate": "aptronics.business_rules.validations.purchase_invoice_excluding_price_check"
	},
	"Quotation ": {
		"before_print": "aptronics.bundling.merge_bundled_items"
	},
	"Sales Invoice": {
		"before_print": "aptronics.bundling.merge_bundled_items"
	},
	"File": {
		"on_trash": "aptronics.files.confirm_delete_of_submitted_doc"
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
override_whitelisted_methods = {
	"erpnext.selling.doctype.sales_order.sales_order.make_purchase_order":
	"aptronics.overrides.make_aptronics_purchase_order",
	"erpnext.selling.doctype.delivery_note.delivery_note.make_sales_invoice":
	"aptronics.overrides.make_aptronics_sales_invoice"
}
