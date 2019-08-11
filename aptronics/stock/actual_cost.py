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
        if incoming_rate:
            i.actual_cost = frappe.utils.flt(incoming_rate[0][0])
            total_actual_cost = total_actual_cost + (i.actual_cost * i.qty)

        i.gross_profit = i.amount - (i.actual_cost * i.qty)
        total_gross_profit = total_gross_profit + (i.gross_profit)

    doc.total_actual_cost = total_actual_cost
    doc.total_gross_profit = total_gross_profit

def shipped_not_invoiced(doc, method):
    frappe.logger().info(method + " : " + doc.doctype)

    for i in doc.items:
        try:
            sle = frappe.get_doc("Stock Ledger Entry", {"voucher_detail_no": i.name})
            line_total = abs(sle.valuation_rate*sle.actual_qty)
            gle = frappe.get_doc("GL Entry", {"voucher_no": doc.name, "account": i.expense_account})
            stock_line = frappe.get_doc("GL Entry", {"voucher_no": doc.name, "account": gle.against})
            stock_line.against = "Shipped Not Invoiced - APT"
            stock_line.save()
        except:
            frappe.logger().info(sys.exc_info()[0])

        try:
            if not sle:
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
                    gle_rev_cost.against = gle.against
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
                    gle_rev_cost.against = gle.against
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

def gl_entry_insert(doc,method):
    frappe.logger().info(method + " : " + str(doc.doctype) + " : " + str(doc.name) + " : " + str(doc.account) + " : " + str(doc.against) + " : " + str(doc.voucher_type) + " : " + str(doc.voucher_no))
    if doc.voucher_type == "Delivery Note":
        if doc.account == "Stock In Hand - APT":
            doc.against = "Shipped Not Invoiced - APT"
        else:
            if doc.against == "Stock In Hand - APT" and doc.account != "Shipped Not Invoiced - APT":
                dnote = frappe.get_doc("Delivery Note", doc.voucher_no)
                done_line = ''
                for i in dnote.items:
                    try:
                        sle = frappe.get_doc("Stock Ledger Entry", {"voucher_detail_no": i.name})
                        line_total = abs(sle.valuation_rate * sle.actual_qty)
                    except:
                        frappe.logger().info(sys.exc_info()[0])

                    try:
                        if sle:
                            gle_rev_cost = frappe.db.sql("""select name
                            from `tabGL Entry`
                            where voucher_no = %s and 
                            account = %s and remarks = %s""", (doc.voucher_no, "Shipped Not Invoiced - APT", i.name), as_dict=True)

                            if not gle_rev_cost:
                                if done_line == '':
                                    doc.account = "Shipped Not Invoiced - APT"
                                    doc.debit = line_total
                                    doc.debit_in_account_currency = line_total
                                    doc.remarks = i.name
                                    done_line = i.name
                                else:
                                    if sle.actual_qty < 0:
                                        gle_rev_cost = frappe.new_doc("GL Entry")
                                        gle_rev_cost.voucher_type = doc.voucher_type
                                        gle_rev_cost.to_rename = doc.to_rename
                                        gle_rev_cost.cost_center = doc.cost_center
                                        gle_rev_cost.voucher_no = doc.voucher_no
                                        gle_rev_cost.company = doc.company
                                        gle_rev_cost.is_advance = doc.is_advance
                                        gle_rev_cost.docstatus = doc.docstatus
                                        gle_rev_cost.remarks = i.name
                                        gle_rev_cost.is_opening = "No"
                                        gle_rev_cost.posting_date = doc.posting_date
                                        gle_rev_cost.account_currency = doc.account_currency
                                        gle_rev_cost.account = "Shipped Not Invoiced - APT"
                                        gle_rev_cost.debit = line_total
                                        gle_rev_cost.debit_in_account_currency = line_total
                                        gle_rev_cost.against = doc.against
                                        gle_rev_cost.credit = 0
                                        gle_rev_cost.credit_in_account_currency = 0
                                        gle_rev_cost.insert()
                                    else:
                                        gle_rev_cost = frappe.new_doc("GL Entry")
                                        gle_rev_cost.voucher_type = doc.voucher_type
                                        gle_rev_cost.to_rename = doc.to_rename
                                        gle_rev_cost.cost_center = doc.cost_center
                                        gle_rev_cost.voucher_no = doc.voucher_no
                                        gle_rev_cost.company = doc.company
                                        gle_rev_cost.is_advance = doc.is_advance
                                        gle_rev_cost.docstatus = doc.docstatus
                                        gle_rev_cost.remarks = i.name
                                        gle_rev_cost.is_opening = "No"
                                        gle_rev_cost.posting_date = doc.posting_date
                                        gle_rev_cost.account_currency = doc.account_currency
                                        gle_rev_cost.account = "Shipped Not Invoiced - APT"
                                        gle_rev_cost.debit = 0
                                        gle_rev_cost.debit_in_account_currency = 0
                                        gle_rev_cost.against = doc.against
                                        gle_rev_cost.credit = line_total
                                        gle_rev_cost.credit_in_account_currency = line_total
                                        gle_rev_cost.insert()

                    except:
                        frappe.logger().info(sys.exc_info()[0])