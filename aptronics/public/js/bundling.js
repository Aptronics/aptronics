const cont_icon = '<i class="octicon octicon-package" style="color: rgb(141, 153, 166); font-size: 18px; margin-right: 8px;"></i>';
const start_icon = '<i class="octicon octicon-package" style="color: rgb(152, 216, 91); font-size: 18px; margin-right: 10px;"></i>';


frappe.ui.form.on("Sales Invoice", {
	refresh: (frm) => {
		add_bundle_button();
		add_unbundle_button();
		render_bsbt();
	}
});

frappe.ui.form.on("Sales Invoice Item", {
	items_move: (frm, cdt, cdn) => {
		console.log('items_move');
		calc_bsbt();
		render_bsbt();
	},
	items_add: (frm, cdn, cdt) => {
		console.log('items_add')
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
}

function calc_bsbt(){
	let selected = [];
	selected = cur_frm.fields_dict.items.grid.get_selected_children();
	let items = cur_frm.doc.items;
	let selected_idx = 0;
	let bundle_start = '';
	for(let i=0; i < items.length; i++){
		if(selected.length == selected_idx){
			break;
		} else if(items[i].name != selected[selected_idx].name){
			if(items[i].bsbt && items[i].bsbt == bundle_start){
				selected_idx++;
				continue;
			}
			bundle_start = '';
			items[i].bsbt = '';
			continue;
		} else if(bundle_start == ''){
			if(items[i].bsbt){
				selected_idx++;
				continue;
			}
			bundle_start = items[i].idx;
			items[i].bsbt = bundle_start;
			selected_idx++;
		} else {
			if(items[i].bsbt){
				selected_idx++;
				continue;
			}
			items[i].bsbt = bundle_start;
			selected_idx++;
		}
	}
}

function render_bsbt(){
	let items = cur_frm.doc.items;
	for(let i=0; i < items.length; i++){
		let wrapper = $(cur_frm.fields_dict.items.grid.grid_rows[i].wrapper);
		if(items[i].bsbt == items[i].idx){
			if($(wrapper.find('.octicon-package').length)){
				$(wrapper.find('.octicon-package')[0]).remove();
			}
			$(wrapper.find('.grid-row-check')[0]).after(start_icon);
		} else if(items[i].bsbt != undefined){
			if($(wrapper.find('.octicon-package').length)){
				$(wrapper.find('.octicon-package')[0]).remove();
			}
			$(wrapper.find('.grid-row-check')[0]).after(cont_icon);
		} else {
			$(wrapper.find('.octicon-package')[0]).remove();
		}
	}
}

function unbundle(){
	let selected = cur_frm.fields_dict.items.grid.get_selected_children();
	for(let i=0; i < selected.length; i++){
		let row_idx = selected[i].idx - 1;
		let wrapper = $(cur_frm.fields_dict.items.grid.grid_rows[row_idx].wrapper);
		selected[i].bsbt = '';
		$(wrapper.find('.octicon-package')[0]).remove();
	}
	selected = [];
}
