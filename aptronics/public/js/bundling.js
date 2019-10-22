const cont_icon = '<i class="octicon octicon-package" style="color: rgb(141, 153, 166); font-size: 18px; margin-right: 8px;"></i>';
const start_icon = '<i class="octicon octicon-package" style="color: rgb(152, 216, 91); font-size: 18px; margin-right: 10px;"></i>';
const term_icon = '<i class="octicon octicon-package" style="color: rgb(255, 160, 10); font-size: 18px; margin-right: 10px;"></i>';

frappe.ui.form.on(cur_frm.doc.doctype, {
	refresh: () => {
		add_bundle_button();
		add_unbundle_button();
		render_bsbt();
	}
});

frappe.ui.form.on(cur_frm.doc.doctype + " Item", {
	items_move: (frm, cdt, cdn) => {
		console.log('items_move');
		calc_bsbt();
		render_bsbt();
	},
	items_add: (frm, cdn, cdt) => {
		add_bundle_button();
		add_unbundle_button();
		render_bsbt();
	},
	items_remove: (frm, cdt, cdn) => {
		calc_bsbt();
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
	cur_frm.refresh_field('items');
}

function calc_bsbt(){
	let items = cur_frm.doc.items;
	items = mark_selected(items, cur_frm.fields_dict.items.grid.get_selected_children());
	for(let i=0; i < items.length; i++){
		if(items[i]._selected == 0){
			continue;
		} else if(i == 0){ // if i == 0, bundle start
			items[i].bsbt = 'Bundle Start';
		} else if(items[i -1]._selected == 0){ // if i -1 is not selected: bundle start
			items[i].bsbt = 'Bundle Start';
		}	else {
			if(i == items.length - 1){
				items[i].bsbt = 'Bundle Terminate';
			} else if(items[i + 1]._selected == 0){
				items[i].bsbt = 'Bundle Terminate';
			} else if(items[i + 1].bsbt == 'Bundle Start'){
				items[i].bsbt = 'Bundle Terminate';
			} else if(items[i - 1]._selected == 1){
				items[i].bsbt = 'Bundle Continue';
			}
		}
	}
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
		$(wrapper.find('.octicon-package')[0]).remove();
	}
	selected = [];
}

function mark_selected(items, selected){
	let selected_idx = 0;
	for(let i=0; i < items.length; i++){
		if(selected_idx == selected.length){
			items[i]._selected = 0;
		} else if(items[i].name != selected[selected_idx].name){
			items[i]._selected = 0;
		}	else {
			items[i]._selected = 1;
			selected_idx++;
		}
	}
	return items;
}


// if(selected.length == selected_idx){
// 	break;
// } else if(items[i].name != selected[selected_idx].name){
// 	if(items[i].bsbt && items[i].bsbt == bundle_start){
// 		selected_idx++;
// 		continue;
// 	}
// 	bundle_start = '';
// 	items[i].bsbt = 'Bundle Start';
// 	continue;
// } else if(bundle_start == ''){
// 	if(items[i].bsbt){
// 		selected_idx++;
// 		continue;
// 	}
// 	bundle_start = items[i].idx;
// 	items[i].bsbt = 'Bundle Start';
// 	selected_idx++;
// } else if(selected_idx){
// 	if(items[i].bsbt){
// 		selected_idx++;
// 		continue;
// 	}
// 	bundle_start = items[i].idx;
// 	items[i].bsbt = 'Bundle Start';
// 	selected_idx++;
// } else {
// 	if(items[i].bsbt){
// 		selected_idx++;
// 		continue;
// 	}
// 	items[i].bsbt = 'Bundle Continue';
// 	selected_idx++;
// }
// }
