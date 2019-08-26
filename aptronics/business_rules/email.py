from __future__ import unicode_literals

import sys

import frappe

@frappe.whitelist()
def check_email_address(doc, method):
    data = str(doc.as_dict())
    frappe.logger().info(doc.recipients)
    for i in doc.recipients:
        if i.recipient.split("@")[1] in ['aptronics.co.za','eoh.com','eoh.co.za', 'ioco.tech']:
            pass
        else:
            frappe.logger().info('Dont send for ' + i.recipient)