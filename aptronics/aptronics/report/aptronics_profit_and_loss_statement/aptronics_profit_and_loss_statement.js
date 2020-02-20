// Copyright (c) 2016, Aptronics and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Aptronics Profit and Loss Statement"] = {
	"filters": get_filters()
};
function get_filters(){
	let filters = [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"fiscal_year",
			"label": __("Fiscal Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"default": frappe.defaults.get_user_default("fiscal_year"),
			"reqd": 1
		},
		{
			"fieldname":"current_period",
			"label": __("Current Period"),
			"fieldtype": "Select",
			"options": moment().locale(frappe.boot.lang)._locale._months.map(m => __(m)), // translate months
			"default": __(moment().subtract(1, "month").locale(frappe.boot.lang).format('MMMM')), // set default month back one
			"reqd": 1
		},
		{
			"fieldname": "cost_center",
			"label": __("Cost Center"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Cost Center', txt, {
					company: frappe.query_report.get_filter_value("company")
				});
			}
		}
	]

	erpnext.dimension_filters.forEach((dimension) => {
		filters.push({
			"fieldname": dimension["fieldname"],
			"label": __(dimension["label"]),
			"fieldtype": "Link",
			"options": dimension["document_type"]
		});
	});

	return filters;
}
