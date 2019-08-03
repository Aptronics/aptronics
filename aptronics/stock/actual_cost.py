from __future__ import unicode_literals

import frappe

@frappe.whitelist()
def get_actual_cost_by_batch(doc, method):
    data = str(doc.as_dict())
    frappe.logger().info(doc.total_actual_cost)
    frappe.logger().info(method)
    total_actual_cost = 0
    for i in doc.items:
        frappe.logger().info(i.batch_no)
        incoming_rate = frappe.db.sql("""select incoming_rate
			from `tabStock Ledger Entry`
			where batch_no = %s and item_code = %s""", (i.batch_no, i.item_code))
        total_actual_cost = total_actual_cost + frappe.utils.flt(incoming_rate[0][0])*i.qty

    doc.total_actual_cost = total_actual_cost