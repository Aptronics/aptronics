const start_icon = '<i class="octicon octicon-package" style="color: rgb(152, 216, 91); font-size: 18px; margin-right: 12px;"></i>';
const cont_icon = '<i class="octicon octicon-package" style="color: rgb(141, 153, 166); font-size: 18px; margin-right: 8px;"></i>';
const term_icon = '<i class="octicon octicon-package" style="color: rgb(255, 160, 10); font-size: 18px; margin-right: 8px;"></i>';

frappe.ui.form.on(cur_frm.doc.doctype, {
	refresh: () => {
		add_bundle_button();
		add_unbundle_button();
		render_bsbt();
	}
});

frappe.ui.form.on(cur_frm.doc.doctype + " Item", {
	items_move: () => {
		frappe.msgprint('Moving items may require re-bundling existing bundles.',	'Warning');
		calc_bsbt(true);
		render_bsbt();
	},
	items_add: () => {
		calc_bsbt();
		render_bsbt();
	},
	items_remove: () => {
		calc_bsbt(true);
		render_bsbt();
	}
});


function add_bundle_button(){
	if($(".grid-add-bundle-button").length > 0){
		return;
	} else {
		let button = '<button type="reset" class="grid-add-bundle-button btn btn-xs btn-success"\
			style="margin-right: 4px;">Bundle Selected Rows<!-- hack to allow firefox include this in tabs --></button> ';
		$('*[data-fieldname="items"]').find('.grid-remove-rows').before(button);
		$('*[data-fieldname="items"]').find('.grid-add-bundle-button').on("click", mark_bsbt);
	}
}

function add_unbundle_button(){
	if($(".grid-add-unbundle-button").length > 0){
		return;
	} else {
		let button = '<button type="reset" class="grid-add-unbundle-button btn btn-xs btn-warning"\
			style="margin-right: 4px;">Unbundle Selected Rows<!-- hack to allow firefox include this in tabs --></button> ';
		$('*[data-fieldname="items"]').find('.grid-remove-rows').before(button);
		$('*[data-fieldname="items"]').find('.grid-add-unbundle-button').on("click", unbundle);
	}
}

function mark_bsbt(){
	calc_bsbt();
	render_bsbt();
	return false;
}

function render_bsbt(){
	let items = cur_frm.doc.items;
	for(let i=0; i < items.length; i++){
		let wrapper = $(cur_frm.fields_dict.items.grid.grid_rows[i].wrapper);
		if(items[i].bsbt == "Bundle Start"){
			if($(wrapper.find('.octicon-package').length)){
				$(wrapper.find('.octicon-package')[0]).remove();
			}
			$(wrapper.find('.grid-row-check')[0]).after(start_icon);
		} else if(items[i].bsbt == "Bundle Continue"){
			if($(wrapper.find('.octicon-package').length)){
				$(wrapper.find('.octicon-package')[0]).remove();
			}
			$(wrapper.find('.grid-row-check')[0]).after(cont_icon);
		} else if(items[i].bsbt == "Bundle Terminate"){
			if($(wrapper.find('.octicon-package').length)){
				$(wrapper.find('.octicon-package')[0]).remove();
			}
			$(wrapper.find('.grid-row-check')[0]).after(term_icon);
		}	else {
			$(wrapper.find('.octicon-package')[0]).remove();
		}
	}
}

function unbundle(){
	let selected = cur_frm.fields_dict.items.grid.get_selected_children();
	for(let i=0; i < selected.length; i++){
		let row_idx = selected[i].idx - 1;
		let wrapper = $(cur_frm.fields_dict.items.grid.grid_rows[row_idx].wrapper);
		selected[i].bsbt = undefined;
		selected[i].__checked = 0;
		$(wrapper.find('.octicon-package')[0]).remove();
	}
	calc_bsbt(true);
	render_bsbt();
	cur_frm.dirty();
}

function deselect_all(){
	$(cur_frm.fields_dict.items.grid.wrapper).find('.grid-row-check:checked').prop('checked', '');
	let items = cur_frm.doc.items;
	for(let i=0; i < items.length; i++){
		items[i].__checked = 0;
	}
}


function calc_bsbt(select_bsbt){
	let items = cur_frm.doc.items;
	if(select_bsbt){
		for(let i=0; i < items.length; i++){
			items[i].bsbt ? items[i].__checked = 1 : items[i].__checked = 0;
			console.log(i, items[i].bsbt, items[i].__checked)
		}
	}
	for(let i=0; i < items.length; i++){
		if(!items[i].__checked)
			continue;
		if(i == 0){ // first one
			items[i].bsbt = 'Bundle Start';
		} else if(i == items.length - 1){ // last one
			if(items[i - 1].__checked){
				items[i].bsbt = 'Bundle Terminate';
			} else if (!items[i - 1].__checked){
				items[i].bsbt = 'Bundle Start';
			}
		} else if(items[i + 1].bsbt == 'Bundle Start'){ // if the next one is a 'bundle start'
			items[i].bsbt = 'Bundle Terminate';
		} else if(!items[i - 1].__checked && items[i + 1].__checked){
			items[i].bsbt = 'Bundle Start';
		} else if(items[i - 1].__checked && !items[i + 1].__checked){
			items[i].bsbt = 'Bundle Terminate';
		} else if(items[i - 1].__checked && items[i + 1].__checked){
			items[i].bsbt = 'Bundle Continue';
		}
	}
	cur_frm.dirty();
	deselect_all();
	return false;
}
