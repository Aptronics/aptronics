from __future__ import unicode_literals

import frappe

@frappe.whitelist()
def get_actual_cost_by_batch(doc, method):
    data = str(doc.as_dict())
    print(doc)
    print(method)
    