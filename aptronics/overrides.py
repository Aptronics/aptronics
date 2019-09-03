import frappe

def get_gl_entries(self, warehouse_account=None):
    from erpnext.accounts.general_ledger import merge_similar_entries
    gl_entries = []
    self.make_customer_gl_entry(gl_entries)
    self.make_tax_gl_entries(gl_entries)
    self.make_item_gl_entries(gl_entries)
    gl_entries = merge_similar_entries(gl_entries)
    self.make_loyalty_point_redemption_gle(gl_entries)
    self.make_pos_gl_entries(gl_entries)
    self.make_gle_for_change_amount(gl_entries)
    make_cogs_entry(self, gl_entries) # this is the extra one
    self.make_write_off_gl_entry(gl_entries)
    self.make_gle_for_rounding_adjustment(gl_entries)
    return gl_entries

def make_cogs_entry(self, gl_entries):
    if frappe.get_cached_value('Stock Settings', 'Stock Settings', 'cogs_on_invoice'):
        return
    goods_in_transit_account = frappe.get_cached_value('Company', self.company, 'goods_in_transit_account')
    if not goods_in_transit_account:
        frappe.throw(frappe._('Goods in Transit Account must be set in Company for this transaction'))
    cogs_account = frappe.get_cached_value('Company', self.company, 'default_expense_account')
    if grand_total:
        grand_total_in_company_currency = flt(grand_total * self.conversion_rate,
            self.precision("grand_total"))
        print([self[d] for d in self.items()])
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
