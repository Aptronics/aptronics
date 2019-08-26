from __future__ import unicode_literals

import sys

import frappe

@frappe.whitelist()
def check_email_address(doc, method):
    #data = str(doc.as_dict())
    frappe.logger().info(doc)
    #for i in doc.recipients:
    #    index = index + 1
    #    if not i.recipient.split("@")[1] in ['aptronics.co.za','eoh.com','eoh.co.za', 'ioco.tech']:
    #        frappe.logger().info('dont send for ' + i.recipient)
