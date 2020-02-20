# Copyright (c) 2013, Aptronics and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from dateutil.parser import parse as parse_date
from calendar import monthrange
from erpnext.accounts.utils import get_balance_on
from frappe.utils.safe_exec import safe_exec, get_safe_globals


def execute(filters=None):
	doc = frappe.get_doc("Report", "Aptronics Profit and Loss Statement")
	data = []
	month_start = parse_date("{} {}".format(filters.current_period, filters.fiscal_year))
	month_start = month_start.replace(day=1)
	month_end = month_start.replace(
		day=(monthrange(month_start.year, month_start.month)[1])
	)
	fiscal_year_start = frappe.get_value("Fiscal Year", filters.fiscal_year, "year_start_date")
	for row in doc.report_rows:
		if not row.subtotal:
			current_period = get_total_for_account(
				filters.company, row.account, month_start, month_end
			)
			year_to_date = get_total_for_account(
				filters.company, row.account, fiscal_year_start, month_end
			)
		else:
			year_to_date = 0
			current_period = 0
		data.append(frappe._dict({
			"account": "<strong> {} </strong>".format(row.row_label) if row.subtotal else row.account,
			"current_period": current_period,
			"year_to_date": year_to_date
		}))
	exec_globals = get_safe_globals()
	exec_globals.__builtins__['sum'] = __builtins__['sum']
	exec_globals.__builtins__['format'] = __builtins__['format']
	for row in doc.report_rows:
		if row.subtotal and row.formula:
			loc = {"filters": frappe._dict(filters), 'data': data}
			safe_exec(row.formula, None, loc)
	return get_columns(), data


def get_total_for_account(company, account, start_date, end_date):
	root_type = frappe.get_value("Account", account, 'root_type')
	total = frappe.db.sql("""
		SELECT SUM(credit) AS credit,
		SUM(debit) AS debit
		FROM `tabGL Entry`
		WHERE company = %(company)s
		AND account = %(account)s
		AND posting_date >= %(start_date)s
		AND posting_date <= %(end_date)s
		""",
		{
			'company': company,
			'account': account,
			'start_date': start_date,
			'end_date': end_date,
		},
		as_dict=True
	)
	if not total[0].get('credit') and not total[0].get('debit'):
		return 0.0
	elif root_type == 'Income':
		return total[0].get('credit', 0.0) - total[0].get('debit', 0.0)
	elif total:
		return total[0].get('debit', 0.0) - total[0].get('credit', 0.0)


def get_columns():
	return [
		{
			"fieldname": "account",
			"label": "Account",
			"fieldtype": "Data",
			"options": "Account",
			"width": 300
		}, {
			"fieldname": "current_period",
			"label": "Period",
			"fieldtype": "Currency",
			"width": 300
		}, {
			"fieldname": "year_to_date",
			"label": "Year to Date",
			"fieldtype": "Currency",
			"width": 300
		}]
