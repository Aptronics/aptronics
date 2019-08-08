from __future__ import unicode_literals

import sys

import frappe

@frappe.whitelist()
def get_actual_cost_by_batch(doc, method):
    # data = str(doc.as_dict())
    #frappe.logger().info(doc.total_actual_cost)
    # frappe.logger().info(method)
    total_actual_cost = 0
    total_gross_profit = 0
    for i in doc.items:
        incoming_rate = frappe.db.sql("""select incoming_rate
			from `tabStock Ledger Entry`
			where voucher_type = "Purchase Receipt" and 
            batch_no = %s and item_code = %s""", (i.batch_no, i.item_code))
        i.actual_cost = frappe.utils.flt(incoming_rate[0][0])
        total_actual_cost = total_actual_cost + (i.actual_cost * i.qty)

        i.gross_profit = i.amount - (i.actual_cost * i.qty)
        total_gross_profit = total_gross_profit + (i.gross_profit)

    doc.total_actual_cost = total_actual_cost
    doc.total_gross_profit = total_gross_profit

def shipped_not_invoiced(doc, method):
    frappe.logger().info(method + " : " + doc.doctype)
    gle = frappe.get_doc("GL Entry", {"voucher_no": doc.name, "account": i.expense_account})
    stock_line = frappe.get_doc("GL Entry", {"voucher_no": doc.name, "account": i.expense_account})

    for i in doc.items:
        sle = frappe.get_doc("Stock Ledger Entry", {"voucher_detail_no": i.name})
        line_total = abs(sle.valuation_rate*sle.actual_qty)
        try:
            gle_rev_cost = frappe.db.sql("""select name
            from `tabGL Entry`
            where voucher_no = %s and 
            account = %s and remarks = %s""", (doc.name,i.expense_account,i.name), as_dict=True)

            if gle_rev_cost:
                frappe.logger().info(gle_rev_cost.name)
            #else:
            if sle.actual_qty < 0:
                gle_rev_cost = frappe.new_doc("GL Entry")
                gle_rev_cost.voucher_type = gle.voucher_type
                gle_rev_cost.to_rename = gle.to_rename
                gle_rev_cost.cost_center = gle.cost_center
                gle_rev_cost.voucher_no = gle.voucher_no
                gle_rev_cost.company = gle.company
                gle_rev_cost.is_advance = gle.is_advance
                gle_rev_cost.docstatus = gle.docstatus
                gle_rev_cost.remarks = i.name
                gle_rev_cost.is_opening = "No"
                gle_rev_cost.posting_date = gle.posting_date
                gle_rev_cost.account_currency = gle.account_currency
                gle_rev_cost.account = "Shipped Not Invoiced - APT"
                gle_rev_cost.debit = line_total
                gle_rev_cost.debit_in_account_currency = line_total
                gle_rev_cost.against = i.expense_account
                gle_rev_cost.credit = 0
                gle_rev_cost.credit_in_account_currency = 0
                gle_rev_cost.insert()

                # gle_rev_cost = frappe.new_doc("GL Entry")
                # gle_rev_cost.voucher_type = gle.voucher_type
                # gle_rev_cost.to_rename = gle.to_rename
                # gle_rev_cost.cost_center = gle.cost_center
                # gle_rev_cost.voucher_no = gle.voucher_no
                # gle_rev_cost.company = gle.company
                # gle_rev_cost.is_advance = gle.is_advance
                # gle_rev_cost.docstatus = gle.docstatus
                # gle_rev_cost.remarks = i.name
                # gle_rev_cost.is_opening = "No"
                # gle_rev_cost.posting_date = gle.posting_date
                # gle_rev_cost.account_currency = gle.account_currency
                # gle_rev_cost.account = i.expense_account
                # gle_rev_cost.debit = 0
                # gle_rev_cost.debit_in_account_currency = 0
                # gle_rev_cost.against = "Shipped Not Invoiced - APT"
                # gle_rev_cost.credit = line_total
                # gle_rev_cost.credit_in_account_currency = line_total
                # gle_rev_cost.insert()
            else:
                # #pass
                # gle_rev_cost = frappe.new_doc("GL Entry")
                # gle_rev_cost.voucher_type = gle.voucher_type
                # gle_rev_cost.to_rename = gle.to_rename
                # gle_rev_cost.cost_center = gle.cost_center
                # gle_rev_cost.voucher_no = gle.voucher_no
                # gle_rev_cost.company = gle.company
                # gle_rev_cost.is_advance = gle.is_advance
                # gle_rev_cost.docstatus = gle.docstatus
                # gle_rev_cost.remarks = i.name
                # gle_rev_cost.is_opening = "No"
                # gle_rev_cost.posting_date = gle.posting_date
                # gle_rev_cost.account_currency = gle.account_currency
                # gle_rev_cost.account = i.expense_account
                # gle_rev_cost.debit = line_total
                # gle_rev_cost.debit_in_account_currency = line_total
                # gle_rev_cost.against = "Shipped Not Invoiced - APT"
                # gle_rev_cost.credit = 0
                # gle_rev_cost.credit_in_account_currency = 0
                # gle_rev_cost.insert()

                gle_rev_cost = frappe.new_doc("GL Entry")
                gle_rev_cost.voucher_type = gle.voucher_type
                gle_rev_cost.to_rename = gle.to_rename
                gle_rev_cost.cost_center = gle.cost_center
                gle_rev_cost.voucher_no = gle.voucher_no
                gle_rev_cost.company = gle.company
                gle_rev_cost.is_advance = gle.is_advance
                gle_rev_cost.docstatus = gle.docstatus
                gle_rev_cost.remarks = i.name
                gle_rev_cost.is_opening = "No"
                gle_rev_cost.posting_date = gle.posting_date
                gle_rev_cost.account_currency = gle.account_currency
                gle_rev_cost.account = "Shipped Not Invoiced - APT"
                gle_rev_cost.debit = 0
                gle_rev_cost.debit_in_account_currency = 0
                gle_rev_cost.against = i.expense_account
                gle_rev_cost.credit = line_total
                gle_rev_cost.credit_in_account_currency = line_total
                gle_rev_cost.insert()

        except:
            frappe.logger().info(sys.exc_info()[0])
    try:
        if gle:
            frappe.db.sql("""delete from `tabGL Entry`
                        where name = %s""", (gle.name))
    except:
        frappe.logger().info(sys.exc_info()[0])


def reversal_shipment_not_invoiced(doc,method):
    frappe.logger().info(method + " : " + doc.doctype)

