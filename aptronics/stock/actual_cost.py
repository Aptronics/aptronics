from __future__ import unicode_literals

import frappe

@frappe.whitelist()
def get_actual_cost_by_batch(doc, method):
    data = str(doc.as_dict())
    #frappe.logger().info(doc.total_actual_cost)
    #frappe.logger().info(method)
    total_actual_cost = 0
    total_gross_profit = 0
    for i in doc.items:
        total_actual_cost = total_actual_cost + (i.actual_cost*qty)
        total_gross_profit = total_gross_profit + (i.gross_profit)

    doc.total_actual_cost = total_actual_cost
    doc.total_gross_profit = total_gross_profit

def get_actual_cost_by_batch_on_item(doc, method):
    data = str(doc.as_dict())
    #frappe.logger().info(doc.total_actual_cost)
    #frappe.logger().info(method)
    actual_cost = 0
    frappe.logger().info(doc.batch_no)
    incoming_rate = frappe.db.sql("""select incoming_rate
			from `tabStock Ledger Entry`
			where batch_no = %s and item_code = %s""", (doc.batch_no, doc.item_code))
    actual_cost = actual_cost + frappe.utils.flt(incoming_rate[0][0])*i.qty

    doc.actual_cost = actual_cost
    doc.gross_profit = doc.amount - (doc.actual_cost*doc.qty)