from __future__ import unicode_literals

import sys

import frappe

@frappe.whitelist()
def check_email_address(doc, method):
    #data = str(doc.as_dict())
    frappe.logger().info(doc)
    list = ''
    domains = ['aptronics.co.za', 'eoh.com', 'eoh.co.za', 'ioco.tech']
    for i in doc.recipients.split(","):
        if i.split("@")[1] in domains:
            list = list + i + ','

    doc.recipients = list

    list = ''
    for i in doc.cc.split(","):
        if i.split("@")[1] in domains:
            list = list + i + ','

    doc.cc = list

    list = ''
    for i in doc.bcc.split(","):
        if i.split("@")[1] in domains:
            list = list + i + ','

    doc.bcc = list
    #    index = index + 1
    #    if not i.recipient.split("@")[1] in ['aptronics.co.za','eoh.com','eoh.co.za', 'ioco.tech']:
    #        frappe.logger().info('dont send for ' + i.recipient)
