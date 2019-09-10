import frappe
from frappe import _
from frappe.utils import flt

def get_gl_entries(self, warehouse_account=None):
	print('patched')
	gl_entries = self._original_get_gl_entries(warehouse_account)
	return make_cogs_entry(self, gl_entries)

def make_cogs_entry(self, gl_entries):
	if not frappe.get_cached_value('Stock Settings', 'Stock Settings', 'cogs_on_invoice'):
		print('cogs_on_invoice not enabled')
		return gl_entries
	goods_in_transit_account = frappe.get_cached_value('Company', self.company, 'goods_in_transit_account')
	if not goods_in_transit_account:
		frappe.throw(frappe._('Goods in Transit Account must be set in Company for this transaction'))
	cogs_account = frappe.get_cached_value('Company', self.company, 'default_expense_account')
	cogs_amount = 0
	for item in self.items:
		if not item.delivery_note:
			continue
		dni_account = frappe.get_value('Delivery Note Item', item.dn_detail, 'expense_account')
		if dni_account != goods_in_transit_account:
			continue
		stock_value_difference = frappe.get_value('Stock Ledger Entry',
			{'voucher_detail_no': item.dn_detail}, 'stock_value_difference')
		cogs_amount += stock_value_difference
		print(cogs_amount)
	# get list of invoices with entries against goods in transit, voucher_no
	# Get total cogs_amount_already_posted_in_si
	# Make sure cogs_amount + cogs_amount_already_posted_in_si < total_goods_in_transit_in_dn
	# Create COGS gles with amount: min(total_goods_in_transit_in_dn, cogs_amount + cogs_amount_already_posted_in_si)
	return gl_entries


def get_cogs_amount_already_posted_in_si(self):
	# lookup sales invoice item
	pass
	# handle two+ invoices for 1 delivery note



def check_expense_account(self, item):
	if not item.get("expense_account"):
		frappe.throw(_("Expense or Difference account is mandatory for Item {0} as it impacts overall stock value").format(item.item_code))
	if frappe.get_value('Stock Settings', 'Stock Settings', 'cogs_on_invoice') == '1':
		is_stock_account = frappe.db.get_value("Account", item.get("expense_account"), "report_type")=="Balance Sheet"
		if not is_stock_account:
			frappe.throw(_("Expense / Difference account ({0}) must be a 'Stock' account, perhaps Goods in Transit?")
				.format(item.get("expense_account")))
		if is_stock_account and not item.get("cost_center"):
			frappe.throw(_("{0} {1}: Cost Center is mandatory for Item {2}").format(
				_(self.doctype), self.name, item.get("item_code")))
	else:
		is_expense_account = frappe.db.get_value("Account", item.get("expense_account"), "report_type")=="Balance Sheet"
		if frappe.db.get_value("Account", item.get("expense_account"), "report_type") != "Profit and Loss":
			frappe.throw(_("Expense / Difference account ({0}) must be a 'Profit or Loss' account")
				.format(item.get("expense_account")))
		if is_expense_account and not item.get("cost_center"):
			frappe.throw(_("{0} {1}: Cost Center is mandatory for Item {2}").format(
				_(self.doctype), self.name, item.get("item_code")))
