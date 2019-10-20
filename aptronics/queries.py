import frappe
from frappe.desk.reportview import get_match_cond, get_filters_cond


def buyer_permissions(doctype, txt, searchfield, start, page_len, filters):
	conditions = []
	return frappe.db.sql("""
		SELECT DISTINCT `tabUser`.name, `tabUser`.full_name
		FROM `tabUser`, `tabHas Role`
		WHERE `tabUser`.enabled = 1
		AND `tabHas Role`.parent = `tabUser`.name
		AND `tabHas Role`.role in ('Purchase Manager', 'Purchase User', 'Purchase Master Manager')
		AND (`tabUser`.{key} like %(txt)s or `tabUser`.full_name like %(txt)s) {fcond} {mcond}
		ORDER BY
			if(locate(%(_txt)s, `tabUser`.name), locate(%(_txt)s, `tabUser`.name), 99999),
			if(locate(%(_txt)s, `tabUser`.full_name), locate(%(_txt)s, `tabUser`.full_name), 99999),
			`tabUser`.idx desc,
			`tabUser`.name, `tabUser`.full_name
		limit %(start)s, %(page_len)s""".format(**{
			'key': searchfield,
			'fcond': get_filters_cond(doctype, filters, conditions),
			'mcond': get_match_cond(doctype)
		}), {
			'txt': "%%%s%%" % txt,
			'_txt': txt.replace("%", ""),
			'start': start,
			'page_len': page_len
		}, debug=1, explain=True)
