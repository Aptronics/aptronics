import frappe
from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_invoice, make_sales_return



@frappe.whitelist()
def make_aptronics_sales_invoice(source_name, target_doc=None):
	si = make_sales_invoice(source_name, target_doc)
	for item in si.items:
		warehouse = frappe.get_value('Delivery Note Item', item.dn_detail, 'target_warehouse')
		item.warehouse = warehouse
	return si
