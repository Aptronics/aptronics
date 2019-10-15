frappe.form.link_formatters['User'] = (value, doc) => {
	if(doc.buyer && doc.buyer_name) {
		return doc.buyer_name + ': ' + doc.buyer;
	} else {
		return value;
	}
}
