import frappe
from frappe.utils import flt

def merge_bundled_items(self, method):
	bundles = {}
	item_meta = frappe.get_meta(self.doctype + " Item")
	count = 0

	copy_fields = ['qty', 'stock_qty']
	sum_fields = ['total_weight', 'amount', 'net_amount']
	rate_fields = [('rate', 'amount'), ('net_rate', 'net_amount'), ('weight_per_unit', 'total_weight')]

	base_fields = [('base_' + f, f) for f in sum_fields if item_meta.has_field('base_' + f)]
	base_fields += [('base_' + f, f) for f in copy_fields if item_meta.has_field('base_' + f)]
	base_fields += [('base_' + t, t) for t, s in rate_fields if item_meta.has_field('base_' + t)]

	# Sum amounts
	in_bundle = 0
	for item in self.items:
		if item.bsbt == 'Bundle Start':
			in_bundle = item.idx

		if not in_bundle or item.bsbt == 'Bundle Start':
			new_bundle = frappe._dict()
			for f in copy_fields:
				new_bundle[f] = item.get(f)
			bundles[item.idx] = new_bundle

		group_item = bundles[in_bundle or item.idx]

		if item.bsbt == 'Bundle Terminate':
			in_bundle = 0

		for f in sum_fields:
			group_item[f] = group_item.get(f, 0) + flt(item.get(f))

		group_item_serial_nos = group_item.setdefault('serial_no', [])
		if item.get('serial_no'):
			group_item_serial_nos += filter(lambda s: s, item.serial_no.split('\n'))

	# Calculate average rates and get serial nos string
	for group_item in bundles.values():
		if group_item.qty:
			for target, source in rate_fields:
				group_item[target] = flt(group_item[source]) / flt(group_item.qty)
		else:
			for target, source in rate_fields:
				group_item[target] = 0

		group_item.serial_no = '\n'.join(group_item.serial_no)

	# Calculate company currency values
	for group_item in bundles.values():
		for target, source in base_fields:
			group_item[target] = group_item.get(source, 0) * self.conversion_rate

	# Remove duplicates and set aggregated values
	to_remove = []
	for item in self.items:
		if item.idx in bundles.keys():
			count += 1
			item.update(bundles[item.idx])
			del bundles[item.idx]
			item.idx = count
		else:
			to_remove.append(item)

	for item in to_remove:
		self.remove(item)

	self.total_qty = sum([d.qty for d in self.items])