import frappe
from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_invoice
from erpnext.selling.doctype.sales_order.sales_order import make_purchase_order

@frappe.whitelist()
def make_aptronics_sales_invoice(source_name, target_doc=None):
	si = make_sales_invoice(source_name, target_doc)
	for item in si.items:
		warehouse = frappe.get_value('Delivery Note Item', item.dn_detail, 'target_warehouse')
		item.warehouse = warehouse
	return si


@frappe.whitelist()
def make_aptronics_purchase_order(source_name, for_supplier=None, selected_items=[], target_doc=None):
	po = make_purchase_order(source_name, for_supplier, selected_items, target_doc)
	po.customer, po.customer_name, po.buyer = frappe.get_value('Sales Order',
	source_name, ['customer', 'customer_name', 'buyer'])
	return po
