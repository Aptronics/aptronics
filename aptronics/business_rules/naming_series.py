from __future__ import unicode_literals

import sys

import frappe
import erpnext.setup.doctype.naming_series

def business_partner_naming_series(doc, method):
    frappe.logger().info(doc)
    if doc.doctype=="Customer":
        doc.naming_series="C-" + doc.customer_name[:3] + ".####"

    if doc.doctype=="Supplier":
        doc.naming_series="S-" + doc.supplier_name[:3] + ".####"

