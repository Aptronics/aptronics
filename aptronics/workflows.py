import frappe
from erpnext.stock.utils import get_stock_balance
from frappe.model.workflow import apply_workflow as model_apply_workflow
from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_invoice
from six import string_types
import json

@frappe.whitelist(allow_guest=True)
def apply_workflow(doc, action):
	# print(doc, action)
	if isinstance(doc, string_types):
		doc = frappe.get_doc(json.loads(doc))
	doc = call_custom_workflow_actions(doc, action)
	return model_apply_workflow(doc, action)


custom_workflow_actions_map = {
	"Delivery Note": {
		"Ship Goods": "aptronics.workflows.make_goods_in_transit_stock_entry",
		"Return Goods in Transit": "aptronics.workflows.reverse_goods_in_transit_stock_entry",
		"Delivered and Create Invoice": "aptronics.workflows.deliver_and_make_invoice"
	}
}

def call_custom_workflow_actions(doc, action):
	doc.last_workflow_action = action
	if custom_workflow_actions_map.get(doc.doctype).get(action):
		doc = frappe.call(custom_workflow_actions_map.get(doc.doctype).get(action), doc=doc)
	return doc

# delivery note/ goods in transit custom workflow
def make_goods_in_transit_stock_entry(doc):
	se = frappe.new_doc("Stock Entry")
	gita_wh = frappe.get_cached_value('Company', doc.company, "default_goods_in_transit_warehouse")
	se.stock_entry_type = 'Material Transfer'
	for item in doc.items:
		se.append('items',
		{
			's_warehouse': item.warehouse,
			't_warehouse': gita_wh,
			'qty': item.qty,
			'item_code': item.item_code,
			'item_name': item.item_name,
			'stock_uom': item.stock_uom,
			'uom': item.uom,
			'conversion_factor': 1,
			'basic_rate': item.rate,
			'serial_no': item.serial_no,
			'batch_no': item.batch_no,
			'description': item.description,
		})
		item.warehouse = gita_wh
	se.save()
	se.submit()
	doc.goods_in_transit_stock_entry = se.name
	return doc

# delivery note/ goods in transit custom workflow
def reverse_goods_in_transit_stock_entry(doc):
	se = frappe.get_doc("Stock Entry", doc.goods_in_transit_stock_entry)
	doc.goods_in_transit_stock_entry = ''
	for item in se.items:
		doc.items = []
		print(item.s_warehouse, item.t_warehouse)
		doc.append('items',
		{
			'warehouse': item.s_warehouse,
			'qty': item.qty,
			'item_code': item.item_code,
			'item_name': item.item_name,
			'stock_uom': item.stock_uom,
			'uom': item.uom,
			'conversion_factor': 1,
			'rate': item.basic_rate,
			'serial_no': item.serial_no,
			'batch_no': item.batch_no,
			'description': item.description,
		})
	se.cancel()
	print(doc)
	return doc

# delivery note/ goods in transit custom workflow
def deliver_and_make_invoice(doc):
	return doc

# delivery note/ goods in transit custom workflow
def cancel_se_on_dn_cancel(doc, method):
	if doc.docstatus != 2:
		return doc
	if not doc.goods_in_transit_stock_entry:
		return
	se = frappe.get_doc("Stock Entry", doc.goods_in_transit_stock_entry)
	if se.docstatus == 1:
		return reverse_goods_in_transit_stock_entry(doc)

# delivery note/ goods in transit custom workflow
def delete_se_on_dn_delete(doc, method):
	if not goods_in_transit_stock_entry:
		return
	se = frappe.get_doc("Stock Entry", doc.goods_in_transit_stock_entry)
	if se.docstatus == 1:
		se.cancel()
	se.delete()
	doc.goods_in_transit_stock_entry = ''
	return doc

# sales order
def check_so_backorder_status(so, method):
	so.total_backordered_qty = 0
	for row in so.items:
		if row.projected_qty < row.qty:
			row.backordered_qty = row.qty
			so.total_backordered_qty += abs(row.backordered_qty)
	if so.total_backordered_qty > 1 and so.docstatus == 1:
		so.delivery_status = "Back Ordered"
	print(so.total_backordered_qty)
	return so

# purchase order
def update_so_with_dropship_po(po, method):
	print(po, method)
	for row in po.items:
		if row.get("sales_order"):
			so = frappe.get_doc("Sales Order", row.sales_order)
			so_rows_to_update = [so_row for so_row in so.items if so_row.item_code == row.item_code and so_row.qty == row.qty]
			for so_row in so_rows_to_update:
				if so_row.delivered_by_supplier == 1:
					so_row.drop_ship_purchase_order = po.name
					so_row.purchase_order_date = po.transaction_date
			so.save()
	return po

# purchase order
def unlink_dropship_po(po, method):
	for row in po.items:
		if row.get("sales_order"):
			so = frappe.get_doc("Sales Order", row.sales_order)
			so_rows_to_update = [so_row for so_row in so.items if so_row.drop_ship_purchase_order == po.name]
			for so_row in so_rows_to_update:
				if so_row.delivered_by_supplier == 1:
					so_row.drop_ship_purchase_order = ""
					so_row.purchase_order_date = ""
			so.save()
			po.status = "Drop Shipped"
			po.per_drop_shipped = (row.qty/ so.total_qty) * 100
			frappe.db.set_value("Sales Order", so.name, "delivery_status", "Drop Shipped")
			# frappe.db.set_value("Sales Order", so.name, "per_delivered", drop_ship_per)
	return po
