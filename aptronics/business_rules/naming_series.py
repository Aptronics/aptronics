from __future__ import unicode_literals

import sys

import frappe
import erpnext.setup.doctype.naming_series

def business_partner_naming_series(doc, method):
    #frappe.logger().info(doc.name)
    if doc.doctype=="Customer":
        doc.naming_series="C-" + doc.customer_name[:3].upper() + ".####" #doc.customer_name[:3].upper() + ".####" #

    if doc.doctype=="Supplier":
        doc.naming_series="S-" + doc.supplier_name[:3].upper() + ".####" # doc.supplier_name[:3].upper() + ".####" #


@frappe.whitelist(allow_guest=False)
def update_series(series, current_value):
	if series:
		prefix = series.split('.')[0]
		frappe.logger().info(str(prefix))
		frappe.logger().info(str(series))
		if not frappe.db.exists('Series', series):
			frappe.db.sql("insert into tabSeries (name, current) values (%s, 0)", (series))

		frappe.db.sql("update `tabSeries` set current = %s where name = %s",
			(current_value, prefix))
		frappe.logger().info("Series Updated Successfully")
		frappe.logger().info(str(series))
		frappe.logger().info(str(current_value))
		return True
	else:
		frappe.logger().info("Series Not Updated - Please select prefix first")
		frappe.logger().info(str(series))
		frappe.logger().info(str(current_value))
		return False #msgprint(_("Please select prefix first"))
