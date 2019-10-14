import frappe
from frappe import _

def sales_order_unique_by_customer(doc,method):
    #exists = frappe.db.sql("SELECT `name` FROM `tabSales Order` WHERE `customer_name`={0} and `po_no`={1} and (name !=%s or `amended_by`!=%s",format(doc.customer_name, doc.po_no.upper(), doc.name))
    #frappe.logger().info('exitst: ' + str(exists))
    #if exists:
     #   frappe.throw(_("Sales order not unique for customer: {0} for order number: {1}").format(doc.customer_name, doc.po_no.upper()))

    if doc.po_no and doc.customer:
        so = frappe.db.sql("select name from `tabSales Order` \
    		where ifnull(po_no, '') = %s and name != %s and docstatus < 2\
    		and customer = %s", (doc.po_no, doc.name, doc.customer))
        if so and so[0][0]:
            frappe.throw(
                _("Warning: Sales Order {0} already exists against Customer's Purchase Order {1}").format(so[0][0],
                                                                                                          doc.po_no))

def purchase_invoice_excluding_price_check(doc,method):
    if doc.validate_excluding_invoice_total <> doc.total:
        frappe.throw(_("Please check Totals."))