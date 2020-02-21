import frappe
from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_invoice
from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_return as make_return_delivery
from erpnext.selling.doctype.sales_order.sales_order import make_purchase_order


@frappe.whitelist()
def make_aptronics_sales_invoice(source_name, target_doc=None):
	si = make_sales_invoice(source_name, target_doc)
	for item in si.items:
		warehouse = frappe.db.get_value('Delivery Note Item',
			item.dn_detail, 'target_warehouse')
		if warehouse:
			item.warehouse = warehouse
	return si


@frappe.whitelist()
def make_aptronics_purchase_order(source_name, target_doc=None):
	po = make_purchase_order(source_name, for_supplier, selected_items, target_doc)
	if po:
		po.customer, po.customer_name, po.buyer = frappe.get_value('Sales Order', source_name,
			['customer', 'customer_name', 'buyer'])
	return po


@frappe.whitelist()
def make_aptronics_return_delivery(source_name, target_doc=None):
	dn = make_return_delivery(source_name, target_doc)
	for item in dn.items:
		warehouse, target_warehouse = item.warehouse, item.target_warehouse
		item.warehouse, item.target_warehouse = target_warehouse, warehouse
	return dn
