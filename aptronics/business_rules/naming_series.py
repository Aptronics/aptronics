from __future__ import unicode_literals

import sys

import frappe
import erpnext.setup.doctype.naming_series

def business_partner_naming_series(doc, method):
    #frappe.logger().info(doc.name)
    if doc.doctype=="Customer":
        doc.naming_series=doc.customer_name[:3].upper() + ".####" #"C-" + doc.customer_name[:3].upper() + ".####"

    if doc.doctype=="Supplier":
        doc.naming_series=doc.supplier_name[:3].upper() + ".####" #"S-" + doc.supplier_name[:3].upper() + ".####"

