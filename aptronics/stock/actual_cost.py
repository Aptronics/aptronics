from __future__ import unicode_literals

import frappe

@frappe.whitelist()
def get_actual_cost_by_batch(doc, method):
    #data = str(doc.as_dict())
    frappe.logger().info(doc.total_actual_cost)
    #frappe.logger().info(method)
    total_actual_cost = 0
    total_gross_profit = 0
    for i in doc.items:
        incoming_rate = frappe.db.sql("""select incoming_rate
			from `tabStock Ledger Entry`
			where voucher_type = "Purchase Receipt" and 
            batch_no = %s and item_code = %s""", (i.batch_no, i.item_code))
        i.actual_cost = frappe.utils.flt(incoming_rate[0][0])
        total_actual_cost = total_actual_cost + (i.actual_cost*i.qty)

        i.gross_profit = i.amount - (i.actual_cost*i.qty)
        total_gross_profit = total_gross_profit + (i.gross_profit)

    doc.total_actual_cost = total_actual_cost
    doc.total_gross_profit = total_gross_profit
