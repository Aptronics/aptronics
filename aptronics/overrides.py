import frappe
from frappe import _
from frappe.utils import flt, cint

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
	for item in self.items:
		cogs_amount = 0
		if not item.delivery_note:
			continue
		dni_account = frappe.get_value('Delivery Note Item', item.dn_detail, 'expense_account')
		if dni_account != goods_in_transit_account:
			continue
		total_goods_in_transit_in_dn = get_total_goods_in_transit_in_dn(self, item.delivery_note)
		stock_value_difference = frappe.get_value('Stock Ledger Entry',
			{'voucher_detail_no': item.dn_detail}, 'stock_value_difference')
		cogs_amount += abs(stock_value_difference)
		already_posted = get_cogs_amount_already_posted_in_si(self, item.dn_detail)
		if (cogs_amount + already_posted) < total_goods_in_transit_in_dn:
			frappe.throw(frappe._('The Total COGS amount for this invoice exceeds the amount posted in the Goods in Transit account'))
		gl_entries = append_cogs_to_gle(self, item, gl_entries, total_goods_in_transit_in_dn)
	return gl_entries

def get_total_goods_in_transit_in_dn(self, delivery_note):
	goods_in_transit_account = frappe.get_cached_value('Company', self.company, 'goods_in_transit_account')
	total_gita = frappe.db.sql("""
		SELECT SUM(debit_in_account_currency) as total_gita FROM `tabGL Entry`
		WHERE `tabGL Entry`.voucher_type = 'Delivery Note'
		AND `tabGL Entry`.voucher_no = %(delivery_note)s
		AND `tabGL Entry`.account = %(gita)s
		""", {'delivery_note': delivery_note,
		'gita': goods_in_transit_account},
		as_dict=True)[0].get('total_gita')
	return total_gita if total_gita else 0.0


def get_cogs_amount_already_posted_in_si(self, dn_detail):
	# switch to item-wise account lookup
	cogs_account = frappe.get_cached_value('Company', self.company, 'default_expense_account')
	frappe.db.sql("""
	SELECT name FROM `tabSales Invoice Item`
	WHERE `tabSales Invoice Item`.dn_detail = %(dn_detail)s
	AND docstatus = 1
	""", {'dn_detail': dn_detail}, as_dict=True)
	cogs_amount = frappe.db.sql("""
		SELECT SUM(credit_in_account_currency) as cogs_amount FROM `tabGL Entry`
		WHERE `tabGL Entry`.voucher_type = 'Sales Invoice'
		AND `tabGL Entry`.voucher_no = %(si)s
		AND `tabGL Entry`.account = %(cogs)s
		""", {'si': self.name, 'cogs': cogs_account},
		as_dict=True)[0].get('cogs_amount')
	return cogs_amount if cogs_amount else 0.0

def append_cogs_to_gle(self, item, gl_entries, total_goods_in_transit_in_dn):
	goods_in_transit_account = frappe.get_cached_value('Company', self.company, 'goods_in_transit_account')
	gl_entries.append(
	    self.get_gl_dict({
	        "account": goods_in_transit_account,
	        "debit": total_goods_in_transit_in_dn,
	        "credit_in_account_currency": total_goods_in_transit_in_dn,
	        "against_voucher": self.return_against if cint(self.is_return) and self.return_against else self.name,
	        "against_voucher_type": self.doctype,
	        "cost_center": self.cost_center,
			"remarks": _("Transfer from " + goods_in_transit_account + " to " + item.expense_account)
	    }, self.party_account_currency)
	)
	gl_entries.append(
	   self.get_gl_dict({
		   "account": item.expense_account,
		   "debit": total_goods_in_transit_in_dn,
		   "credit_in_account_currency": total_goods_in_transit_in_dn,
		   "against_voucher": self.return_against if cint(self.is_return) and self.return_against else self.name,
		   "against_voucher_type": self.doctype,
		   "cost_center": self.cost_center,
		   "remarks": _("Transfer from " + goods_in_transit_account + " to " + item.expense_account)
	   }, self.party_account_currency)
	)
	return gl_entries


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
