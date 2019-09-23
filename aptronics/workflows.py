import frappe
from frappe.model.workflow import apply_workflow as model_apply_workflow
from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_invoice
from six import string_types
import json

@frappe.whitelist(allow_guest=True)
def apply_workflow(doc, action):
	print(doc, action)
	if isinstance(doc, string_types):
		doc = frappe.get_doc(json.loads(doc))
	doc = call_custom_workflow_actions(doc, action)
	return model_apply_workflow(doc, action)


custom_workflow_actions_map = {
	"Delivery Note": {
		"Ship Goods": "aptronics.workflows.make_goods_in_transit_stock_entry",
		"Return Goods in Transit": "aptronics.workflows.reverse_goods_in_transit_stock_entry",
		"Deliver and Create Invoice": "aptronics.workflows.deliver_and_make_invoice",
	}
}

def call_custom_workflow_actions(doc, action):
	doc.last_workflow_action = action
	if custom_workflow_actions_map.get(doc.doctype).get(action):
		doc = frappe.call(custom_workflow_actions_map.get(doc.doctype).get(action), doc=doc)
	return doc

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
	se.save()
	se.submit()
	doc.goods_in_transit_stock_entry = se.name
	return doc


def reverse_goods_in_transit_stock_entry(doc):
	se = frappe.get_doc("Stock Entry", doc.goods_in_transit_stock_entry)
	doc.goods_in_transit_stock_entry = ''
	for item in se.items:
		doc.items = []
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
	return doc

def deliver_and_make_invoice(doc):
	return doc


def cancel_se_on_dn_cancel(doc, method):
	if doc.docstatus != 2:
		return doc
	if not doc.goods_in_transit_stock_entry:
		return
	se = frappe.get_doc("Stock Entry", doc.goods_in_transit_stock_entry)
	if se.docstatus == 1:
		try:
			se.cancel()
			doc.goods_in_transit_stock_entry = ''
			return doc
		except:
			pass

def delete_se_on_dn_delete(doc, method):
	if not goods_in_transit_stock_entry:
		return
	se = frappe.get_doc("Stock Entry", doc.goods_in_transit_stock_entry)
	if se.docstatus == 1:
		se.cancel()
	se.delete()
	doc.goods_in_transit_stock_entry = ''
	return doc
