from __future__ import unicode_literals

import sys

import frappe
from frappe.utils import now_datetime, cint, cstr
import erpnext.setup.doctype.naming_series


def business_partner_naming_series(doc, method):
    # frappe.logger().info(doc.name)
    if doc.doctype == "Customer":
        doc.naming_series = "C-" + doc.customer_name[:3].upper() + ".####"  # doc.customer_name[:3].upper() + ".####" #

    if doc.doctype == "Supplier":
        doc.naming_series = "S-" + doc.supplier_name[:3].upper() + ".####"  # doc.supplier_name[:3].upper() + ".####" #


@frappe.whitelist(allow_guest=False)
def update_series(series, current_value):
    frappe.logger().info("series: " + series + " = " + str(current_value))
    current = frappe.db.sql("SELECT `current` FROM `tabSeries` WHERE `name`=%s FOR UPDATE", (series,))
    if current and current[0][0] is not None:
        current = current[0][0]
        frappe.logger().info("yes, update it")
        frappe.db.sql("UPDATE `tabSeries` SET `current` = %s WHERE `name`=%s", (current_value, series))
        current = cint(current) + 1
    else:
        frappe.logger().info("no, create it")
        frappe.db.sql("INSERT INTO `tabSeries` (`name`, `current`) VALUES (%s, %s)", (series,current_value))
        current = current_value
    return current

    # if series:
    #     prefix = series.split('.')[0]
    #     frappe.logger().info(str(prefix))
    #
    #     if not frappe.db.exists('Series', series):
    #         frappe.logger().info("No series: " + str(series))
    #         frappe.db.sql("insert into tabSeries (name, current) values (%s, 0)", (series))
    #
    #     frappe.db.sql("update `tabSeries` set current = %s where name = %s",
    #                   (current_value, series))
    #     frappe.logger().info("Series Updated Successfully")
    #     frappe.logger().info(str(series))
    #     frappe.logger().info(str(current_value))
    #     return True
    # # else:
    #     frappe.logger().info("Series Not Updated - Please select prefix first")
    #     frappe.logger().info(str(series))
    #     frappe.logger().info(str(current_value))
    #     return False  # msgprint(_("Please select prefix first"))
