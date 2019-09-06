import frappe

def get_gl_entries(self, warehouse_account=None):
	gl_entries = self._original_get_gl_entries(self, warehouse_account)
	return make_cogs_entry(self, gl_entries)

def make_cogs_entry(self, gl_entries):
	if frappe.get_cached_value('Stock Settings', 'Stock Settings', 'cogs_on_invoice'):
		return gl_entries
	goods_in_transit_account = frappe.get_cached_value('Company', self.company, 'goods_in_transit_account')
	if not goods_in_transit_account:
		frappe.throw(frappe._('Goods in Transit Account must be set in Company for this transaction'))
	cogs_account = frappe.get_cached_value('Company', self.company, 'default_expense_account')
	if grand_total:
		grand_total_in_company_currency = flt(grand_total * self.conversion_rate,
			self.precision("grand_total"))
		print([self[d] for d in self.items()])
	return gl_entries
		# gl_entries.append(
		#     self.get_gl_dict({
		#         "account": self.debit_to,
		#         "party_type": "Customer",
		#         "party": self.customer,
		#         "due_date": self.due_date,
		#         "against": self.against_income_account,
		#         "debit": grand_total_in_company_currency,
		#         "debit_in_account_currency": grand_total_in_company_currency \
		#             if self.party_account_currency==self.company_currency else grand_total,
		#         "against_voucher": self.return_against if cint(self.is_return) and self.return_against else self.name,
		#         "against_voucher_type": self.doctype,
		#         "cost_center": self.cost_center
		#     }, self.party_account_currency)
		# )
	# for item in self.items:
	#     cogs_amount = 0
	#     if item.delivery_note:
	#         goods_in_transit_account = frappe.get_cached_value('Company', self.company, 'goods_in_transit_account')
	#
	#         # Check and validate if Delivery Note Item's expense account = goods_in_transit_account
	#         if ________:
	#             stock_value_difference = flt(frappe.db.sql("""select stock_value_difference
	#                  from `tabStock Ledger Entry` where voucher_type='Delivery Note' and voucher_detail_no = %s",
	#             [item.delivery_note, goods_in_transit_account]))
	#             cogs_amount += stock_value_difference
	#
	#         # Get total cogs_amount_already_posted_in_si
	#         # Make sure cogs_amount + cogs_amount_already_posted_in_si < total_goods_in_transit_in_dn
	#         # Create COGS gles with amount: min(total_goods_in_transit_in_dn, cogs_amount + cogs_amount_already_posted_in_si)
