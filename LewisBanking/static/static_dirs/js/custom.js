

//	grab(string): Returns the html element "data"
function grab(data) 
{
	data = String(data);
	var element = document.getElementById(data);
	return element;
}

function frame(frame_id)
{
	return window.frames[frame_id]
}

function pframe(element)
{
	return parent.window.frames[0];
}

function load_page(url, form_name)
{
	form = grab(form_name);
	form.action = url;
	form.submit();
}

function visibility(z_index, mode)
{
	z_index = String(z_index);
	mode = String(mode)
	var name = "z" + z_index;
	var div = grab(name);

	if (mode === 'show')
	{
		div.className = "fadeIn";
		div.style.zIndex = z_index;
	}

	else if (mode === "hide")
	{
		div.className = "fadeOut";
	}

}

function visibility2(z_index, mode)
{
	z_index = String(z_index);
	mode = String(mode)
	var name = "z" + z_index;
	var div = grab(name);

	if (mode === 'show')
	{
		div.className = "fadeIn2";
		div.style.zIndex = z_index;
	}

	else if (mode === "hide")
	{
		div.className = "fadeOut2";
	}

}

function load_popWin(z_div, index, target, width, height, message_type) 
{
	target.style.width = width;
	target.style.height = height;

	if (message_type === 'terms')
	{
		load_terms_html();
	}

	else if (message_type === 'errors')
	{
		load_error_html();
	}

	z_div.style.zIndex = index;
	z_div.className = "fadeIn";
}

function load_terms_html()
{
	var html = "<div class=\"termAgree2\">You agree to the following:</div>";
	html += "<ul>";
	html += "<li>This is not a real bank</li>";
	html += "<li>We will not receive any money from you</li>";
	html += "<li>You will not receive any money from us</li>";
	html += "<li>This is only a Python coding project</li>";
	html += "</ul>";
	grab('messageContent').innerHTML = html;

	grab("messageHeader").innerHTML = "Terms of Service"
}

function load_error_html()
{
	// grab('fname').value = "Loading Errors";
}

function entry_error(target, mode, max_length)
{
	var value = String(target.value);

	if (mode === "text")
	{
		target.value = text_only(value);
	}

	else if (mode === "number")
	{
		target.value = number_only(value, max_length);
	}

	else if (mode === "money")
	{
		target.value = money_only(value, max_length);
	}
}

function number_only(value, max_length)
{
	var edited = "";
	var v = "";

	for (var i = 0; i < max_length; i++)
	{
		v = value.charAt(i);

		if (v==="1" || v==="2" || v==="3" || v==="4" || v==="5" || v==="6" || v==="7" || v==="8" || v=="9" || v==="0")
		{
			edited += v;
		}
	}

	return edited;
}

function text_only(value)
{
	var edited = "";
	var v = "";

	for (var i = 0; i < value.length; i++)
	{
		v = value.charAt(i);

		if (v!=="0" && v!=="1" && v!=="2" && v!=="3" && v!=="4" && v!=="5" && v!=="6" && v!=="7" && v!=="8" && v!=="9")
		{
			edited += v;
		}
	}

	return edited;
}

function money_only(value, max_length)
{
	var edited = "";
	var v = "";

	for (var i = 0; i < max_length; i++)
	{
		v = value.charAt(i);

		if (v==="1" || v==="2" || v==="3" || v==="4" || v==="5" || v==="6" || v==="7" || v==="8" || v=="9" || v==="0" || v===".")
		{
			edited += v;
		}
	}

	return edited;
}

function switchAccountSubmit()
{
	var data = [];
	var button = grab('creBtn');
	var proceed = true;

	data.push(String(grab('fname').value));
	data.push(String(grab('lname').value));
	data.push(String(grab('email').value));
	data.push(String(grab('email2').value));
	data.push(String(grab('password1').value));
	data.push(String(grab('password2').value));	
	data.push(String(grab('phone1').value));
	data.push(String(grab('phone2').value));
	data.push(String(grab('phone3').value));
	data.push(String(grab('deposit').value));
	data.push(String(grab('answer1').value));
	data.push(String(grab('answer2').value));

	for (var i = 0; i < data.length; i++)
	{
		if (data[i].length === 0)
		{
			proceed = false;
			break;
		}
	}

	if (proceed === true)
	{
		button.setAttribute('type', 'button');
		button.setAttribute('onClick', "javascript: field_validation_account();")
	}

	else
	{
		button.setAttribute('type', 'submit');
		button.removeAttribute('onClick');
	}
}

function switchALoanSubmit()
{
	var data = [];
	var button = grab('creBtn');
	var proceed = true;

	data.push(String(grab('fname').value));
	data.push(String(grab('lname').value));
	data.push(String(grab('email').value));
	data.push(String(grab('phone1').value));
	data.push(String(grab('phone2').value));
	data.push(String(grab('phone3').value));
	data.push(String(grab('dollars').value));

	for (var i = 0; i < data.length; i++)
	{
		if (data[i].length === 0)
		{
			proceed = false;
			break;
		}
	}

	if (proceed === true)
	{
		button.setAttribute('type', 'button');
		button.setAttribute('onClick', "javascript: field_validation_loan();")
	}

	else
	{
		button.setAttribute('type', 'submit');
		button.removeAttribute('onClick');
	}
}

function switchALoanSubmit2()
{
	var data = [];
	var button = grab('creBtn');
	var proceed = true;

	data.push(String(grab('email2').value));
	data.push(String(grab('password1').value));
	data.push(String(grab('password2').value));
	data.push(String(grab('answer1').value));
	data.push(String(grab('answer2').value));

	for (var i = 0; i < data.length; i++)
	{
		if (data[i].length === 0)
		{
			proceed = false;
			break;
		}
	}

	if (proceed === true)
	{
		button.setAttribute('type', 'button');
		button.setAttribute('onClick', "javascript: field_validation_loan2();")
	}

	else
	{
		button.setAttribute('type', 'submit');
		button.removeAttribute('onClick');
	}
}

function field_validation_account()
{
	var data = [];
	var proceed = true;
	var email = grab('email');
	var emai2 = grab('email2');
	var pass1 = grab('password1');
	var pass2 = grab('password2');
	var depos = grab('deposit');
	var cents = grab('cents');
	
	if (String(pass1.value) !== String(pass2.value))
	{
		proceed = false;
		data.push("The passwords do not match");
	}

	if (String(email.value) !== String(emai2.value))
	{
		proceed = false;
		data.push("The email addresses do not match");
	}

	if (Number(depos.value) < 5)
	{
		proceed = false;
		data.push("The initial deposit amount must be at least $5.00")
	}

	if (proceed === true)
	{
		if (String(cents.value).length === 0)
		{
			cents.value = "00";
		}

		var button = grab('creBtn');
		button.setAttribute('type', 'submit');
		button.removeAttribute('onClick');
		button.click();
	}
	else
	{
		grab('messageContent').innerHTML = get_error_html(data);
		grab("messageHeader").innerHTML = "<span>Errors Detected</span>"
		load_popWin(grab("z1"), 1, grab("messageWindow"), "400px", "250px", "errors");
	}
}

function field_validation_loan()
{
	var data = [];
	var proceed = true;
	var select = grab("loanTerm");
	var dollars = grab('dollars');
	var cents = grab('cents');
	
	if (select.selectedIndex === 0)
	{
		proceed = false;
		data.push("You must choose a loan term");
	}

	if (Number(dollars.value) < 100)
	{
		proceed = false;
		data.push("You must request at least $100.00")
	}

	if (proceed === true)
	{
		if (String(cents.value).length === 0)
		{
			cents.value = "00";
		}

		var button = grab('creBtn');
		button.setAttribute('type', 'submit');
		button.removeAttribute('onClick');
		button.click();
	}
	else
	{
		grab('messageContent').innerHTML = get_error_html(data);
		grab("messageHeader").innerHTML = "<span>Errors Detected</span>"
		load_popWin(grab("z1"), 1, grab("messageWindow"), "400px", "250px", "errors");
	}
}

function field_validation_loan2()
{
	var data = [];
	var proceed 	= true;
	var select 		= grab("account_type");
	var email1 		= grab('email');
	var email2 		= grab('email2');
	var password1 	= grab('password1');
	var password2 	= grab('password2');
	
	if (select.selectedIndex === 0)
	{
		proceed = false;
		data.push("You must select an account type");
	}

	if (String(password1.value) !== String(password2.value))
	{
		proceed = false;
		data.push("The passwords do not match");
	}

	if (String(email1.value) !== String(email2.value))
	{
		proceed = false;
		data.push("The email addresses do not match");
	}

	if (proceed === true)
	{
		var button = grab('creBtn');
		button.setAttribute('type', 'submit');
		button.removeAttribute('onClick');
		button.click();
	}
	else
	{
		grab('messageContent').innerHTML = get_error_html(data);
		grab("messageHeader").innerHTML = "<span>Errors Detected</span>"
		load_popWin(grab("z2"), 2, grab("messageWindow"), "400px", "250px", "errors");
	}
}

function get_error_html(error_list)
{
	var html = "<ul>";

	for (var i = 0; i < error_list.length; i++)
	{
		html += "<li>" + error_list[i] + "</li>";
	}

	html += "</ul>";
	return html;
}

function initialize_accounts(selected_index)
{
	var win = frame('iframe_list');
	var sort = String(win.grab('sort').value);
	var hidden = win.grab('direction');
	var direction = String(hidden.value);
	var select = grab('sort_parent');
	var dir_text = grab('dir_text');
	var icon = grab('icon');

	set_sort_select(select, sort);
	set_direction(icon, dir_text, hidden, direction);

	var acct_no = win.grab('li0_account_number').value;
	var balance = win.grab('li0_balance').value;
	var date = win.grab('li0_date').value;
	var type = win.grab('li0_type').value;

	grab('selected_account_number').value = acct_no;
	grab('selected_date').value = date;
	grab('selected_balance').value = balance;
	grab('selected_type').value = type;

	grab('selAcct').innerHTML = acct_no;
	grab('selBaln').innerHTML = balance;
	grab('selDate').innerHTML = date;
	grab('selType').innerHTML = type;

	grab('selected_index').value = selected_index;
}

function set_sort_select(select, sort)
{
	if (sort === "account_number")
	{
		select.selectedIndex = 0;
	}

	else if (sort === "isSavings")
	{
		select.selectedIndex = 1;
	}

	else if (sort === "balance")
	{
		select.selectedIndex = 2;
	}

	else if (sort === "date")
	{
		select.selectedIndex = 3;
	}
}

function set_direction(icon, header, hidden, direction)
{
	if (direction === "descend")
	{
		hidden.value = "descend";
		header.innerHTML = "Descending";
		icon.innerHTML = "<i class=\"fa fa-chevron-circle-down\" aria-hidden=\"true\"></i>";
	}

	else if (direction === "ascend")
	{
		hidden.value = "ascend";
		header.innerHTML = "Ascending";
		icon.innerHTML = "<i class=\"fa fa-chevron-circle-up\" aria-hidden=\"true\"></i>";
	}
}

function toggle_dropdown()
{
	var menu = grab("drop_menu");
	var current = String(menu.className);
	var on_state = "dropdown-on";
	var off_state = "dropdown-off";

	if (current === on_state)
	{
		menu.className = off_state;
	}

	else if (current === off_state)
	{
		menu.className = on_state;
	}
}

function load_welcome()
{
	grab('text1').style.borderRight = "1px solid #666666";
	grab('text2').style.borderRight = "1px solid #666666";
	grab('text3').style.borderRight = "1px solid #666666";
	grab('text4').style.borderRight = "1px solid #666666";
}

function set_base_select(btn, text)
{
	grab(btn).className = "btn-selected";
	grab(text).className = "btn-selected-text";

	if (String(text) === "text1")
	{
		grab('text2').style.borderRight = "1px solid #666666";
		grab('text3').style.borderRight = "1px solid #666666";
		grab('text4').style.borderRight = "1px solid #666666";
	}

	else if (String(text) === "text2")
	{
		grab('text3').style.borderRight = "1px solid #666666";
		grab('text4').style.borderRight = "1px solid #666666";
	}

	else if (String(text) === "text3")
	{
		grab('text1').style.borderRight = "1px solid #666666";
		grab('text4').style.borderRight = "1px solid #666666";
	}

	else if (String(text) === "text4")
	{
		grab('text1').style.borderRight = "1px solid #666666";
		grab('text2').style.borderRight = "1px solid #666666";
	}

	else if (String(text) === "text5")
	{
		grab('text1').style.borderRight = "1px solid #666666";
		grab('text2').style.borderRight = "1px solid #666666";
		grab('text3').style.borderRight = "1px solid #666666";
	}

	else
	{
		grab('text1').style.borderRight = "1px solid #666666";
		grab('text2').style.borderRight = "1px solid #666666";
		grab('text3').style.borderRight = "1px solid #666666";
		grab('text4').style.borderRight = "1px solid #666666";
	}
}

function load_url(url)
{
	var form = grab("bank_form");
	form.action = url;
	form.submit();
}

function load_list_item(item_id, index)
{
	var prev_index = grab('selected_index').value;
	clearSelectedLI_child(prev_index);
	load_index(index);	
}

function load_index(index)
{
	var prefix = "li" + String(index) + "_";
	var div_name = prefix + "change_class";
	var div = grab(div_name);
	div.className = "li_highlight";
	grab('selected_index').value = index;
	populate_viewer(index);
}

function populate_viewer(index)
{
	var t_name = "li" + String(index) + "_type";
	var b_name = "li" + String(index) + "_balance";
	var d_name = "li" + String(index) + "_date";
	var a_name = "li" + String(index) + "_account_number";
	var m_type = grab(t_name).value;
	var m_balc = grab(b_name).value;
	var m_date = grab(d_name).value;
	var m_acct = grab(a_name).value;
	parent.grab('selType').innerHTML = m_type;
	parent.grab('selBaln').innerHTML = m_balc;
	parent.grab('selDate').innerHTML = m_date;
	parent.grab('selAcct').innerHTML = m_acct;

	parent.grab('selected_type').value = m_type;
	parent.grab('selected_balance').value = m_balc;
	parent.grab('selected_date').value = m_date;
	parent.grab('selected_account_number').value = m_acct;
}

function clearSelectedLI_child(index)
{
	index = Number(index);
	var view = index % 2;
	var div_name = "li" + String(index) + "_change_class";
	var div = grab(div_name);

	if (view == 0)
	{
		div.className = 'li_clear';
	}
	else
	{
		div.className = 'li_shade';
	}
}

function toggle_carat()
{
	var icon = grab('icon');
	var title = grab('dir_text');
	var hidden = grab('direction_parent')
	var current = String(hidden.value);

	if (current === "descend")
	{
		title.innerHTML = "Ascending";
		icon.innerHTML = "<i class=\"fa fa-chevron-circle-up\" aria-hidden=\"true\"></i>"
		hidden.value = "ascend";
	}

	else if (current === "ascend")
	{
		title.innerHTML = "Descending";
		icon.innerHTML = "<i class=\"fa fa-chevron-circle-down\" aria-hidden=\"true\"></i>";
		hidden.value = "descend";
	}
}

function set_frame_list()
{
	var win = frame('iframe_list');
	var sort = win.grab('sort');
	var direction = win.grab('direction');

	sort.value = grab('sort_parent').value;
	direction.value = grab('direction_parent').value;

	win.grab('frame_form').submit();
}

function load_frame(action)
{
	grab('frame1').setAttribute('src', action);
	visibility(1, "show");
}

function win_visibility(z_index, mode)
{
	z_index = String(z_index);
	mode = String(mode)
	var name = "z" + z_index;
	var div = parent.grab(name);

	if (mode === 'show')
	{
		div.className = "fadeIn";
		div.style.zIndex = z_index;
	}

	else if (mode === "hide")
	{
		div.className = "fadeOut";
	}
}

function init_withdrawal()
{
	var account_number = parent.grab('selected_account_number').value;
	var w_type = parent.grab('selected_type').value;

	grab('w_acct').innerHTML = account_number;
	grab('type').innerHTML = w_type;
	grab('account_number').value = account_number;
	grab('d_type').value = w_type;
}

function init_delete_W()
{
	var account_number = parent.grab('selected_account_number').value;
	var w_type = parent.grab('selected_type').value;

	grab('w_acct').innerHTML = account_number;
	grab('w_types').innerHTML = w_type;
	grab('account_number').value = account_number;
	grab('d_type').value = w_type;
}

function w_error()
{
	var dollars = String(grab('dollars').value);
	var balance = Number(parent.grab('selected_balance').value);
	
	if (dollars.length === 0)
	{
		parent.grab('messageContent').innerHTML = "You must enter a withdrawal amount";
		parent.grab("messageHeader").innerHTML = "<span>Errors Detected</span>"
		var e_win = parent.grab('messageWindow');
		e_win.style.height = "260px";
		win_visibility(2, "show");
	}

	else if (Number(dollars) > balance)
	{
		parent.grab('messageContent').innerHTML = "You do have sufficient funds to proceed with this transaction. Please choose a lower amount.";
		parent.grab("messageHeader").innerHTML = "<span>Errors Detected</span>"
		var e_win = parent.grab('messageWindow');
		e_win.style.height = "260px";
		win_visibility(2, "show");
	}

	else {
		grab('bank_form').submit();
	}
}

function t_error()
{
	var dollars = String(grab('t_dollars').value);
	var cents = String(grab('t_cents').value);
	var errors = [];

	if (cents.length == 0) {grab('t_cents').value = "00"; cents = "00";}

	if (dollars === "0" && cents === "00")
	{
		errors.push("You must transfer at least $0.01");
	}

	if (dollars.length === 0)
	{
		errors.push("You must enter a transfer amount");
	}

	if (grab('from_account').selectedIndex == 0)
	{
		errors.push("You must selected an account to transfer from")
	}

	if (grab('to_account').selectedIndex == 0)
	{
		errors.push("You must selected an account to transfer to")
	}

	if (errors.length !== 0)
	{
		parent.grab('messageContent').innerHTML = get_error_html(errors);
		parent.grab("messageHeader").innerHTML = "<span>Errors Detected</span>";
		var e_win = parent.grab('messageWindow');
		e_win.style.height = "260px";
		e_win.style.width = "400px";
		win_visibility(2, "show");
	}
	else
	{
		var form = grab('transfer_form');
		form.action = "/transfer/";
		form.submit();
	}
}

function w_error_add()
{
	var dollars = String(grab('dollars_w').value);
	
	if (dollars.length === 0)
	{
		parent.grab('messageContent').innerHTML = "You must enter a deposit amount";
		parent.grab("messageHeader").innerHTML = "<span>Errors Detected</span>"
		var e_win = parent.grab('messageWindow');
		e_win.style.height = "260px";
		win_visibility(2, "show");
	}

	else {
		var cents = String(grab('cents_w').value);

		if (cents.length === 0)
		{
			grab('cents_w').value = "00";
		}
		grab('bank_form').submit();
	}
}

function reload_li_list()
{
	var win = parent.window.frames['iframe_list'];
	win.grab('frame_form').submit();
	win_visibility(1, 'hide');
}

function init_history(url)
{
	var btn = grab('hi_btn');
	btn.innerHTML = "View All";
	btn.setAttribute('onCLick', 'javascript: view_all();')
	grab('tv_head').innerHTML = "Viewing History:";
	grab('selType2').innerHTML = grab('selected_type').value;
	grab('selAcct2').innerHTML = grab('selected_account_number').value;
	// grab('active_div').style.visibility = "hidden";
	// grab('selDate').style.visibility = "hidden";

	var iframe = grab('iframe_list');
	iframe.src = url;

	grab('active_div').innerHTML = "";
	grab('selDate').innerHTML = "";
}

function view_all()
{
	var btn = grab('hi_btn');
	display_tv();
	btn.innerHTML = "View Selected Account's History";
	btn.setAttribute('onCLick', "javascript: load_account_sort_options(\'1\'); init_history(\'/view_history0/\');");
	var iframe = grab('iframe_list');
	iframe.src = "/load_account_list/";
	grab('icon').style.visibility = "visible";
	grab('sort_label').style.visibility = "visible";
	grab('sort_parent').style.visibility = "visible";
	grab('dir_text').style.visibility = "visible";
	load_account_sort_options(0)
}

function display_tv()
{
	html =  "<div class=\"Selcted_Item\" id=\"tv_head\" style=\"margin-top:3.5%;\"><span id=\"selType\"></span> <span id=\"selAcct\"></span></div>"
	html += "<div class=\"divider\"></div>"
	html += "<div class=\"inner_class si1\"><span id=\"selType2\"></span> <span id=\"selAcct2\"></span></div>"
	html += "<div class=\"inner_class si2\" id=\"active_div\">Active Since <span id=\"selDate\"></span></div>"
	html += "<div class=\"inner_class si3\">Available Now:<br><span>$</span><span id=\"selBaln\"></span></div>"
	html += "<div class=\"selected-item-content\"></div>"
	grab('tv_builder').innerHTML = html;
}

function load_history()
{
	var selected = parent.grab('selected_account_number').value;
	grab('selected_account').value = selected;
	grab('load_form').submit();
}

function initialize_account_history(options)
{
	alert('initializing')
	var select = parent.grab('sort_parent');

	for (var i = 0; i < options.length; i++)
	{
		alert(select[0]);
	}
}

function loadTransferSelect(changed)
{
	grab('selected_fm').value = grab('from_account').selectedIndex;
	grab('selected_to').value = grab('to_account').selectedIndex;

	grab('transfer_form').submit()
}

function loadFromSelected()
{
	grab('selected_fm').value = grab('from_account').value;
	grab('selected_dollars').value = grab('t_dollars').value;
	grab('selected_cents').value = grab('t_cents').value;

	grab('transfer_form').submit();
}

function loadToSelected()
{
	grab('selected_to').value = grab('to_account').value;
	grab('selected_dollars').value = grab('t_dollars').value;
	grab('selected_cents').value = grab('t_cents').value;

	grab('transfer_form').submit();
}

function load_dynamic_selectes(fm_list, to_list)
{
	var from_select = grab('from_account');
	var to_select = grab('to_account');
	var value_fm = grab('selected_fm').value;
	var value_to = grab('selected_to').value;
	var index_fm = 0;
	var index_to = 0;

	build_aft_list(fm_list, from_select);
	build_aft_list(to_list, to_select);

	for (var i = 0; i < fm_list.length; i++)
	{
		if (String(value_fm) === String(fm_list[i]))
		{
			index_fm = i + 1;
			break;
		}
	}

	for (var i = 0; i < to_list.length; i++)
	{
		if (String(value_to) === String(to_list[i]))
		{
			index_to = i + 1;
			break;
		}
	}

	from_select.selectedIndex = index_fm;
	to_select.selectedIndex = index_to;
}

function build_aft_list(fm_list, target)
{
	var html = "<option value=\"0\">Select</option>";

	for (var i = 0;  i < fm_list.length; i++)
	{
		html += "<option value=\"" + fm_list[i] + "\">" + fm_list[i] + "</option>";
	}

	target.innerHTML = html;
}

function load_dynamic_sel(a, b)
{
	a = Number(a);
	b = Number(b);
	sel_from = grab('from_account');
	sel_to = grab('to_account');
	index_a = get_select_index(a, sel_from);
	index_b = get_select_index(b, sel_to);

	sel_from.selectedIndex = index_a;
	sel_to.selectedIndex = index_b;
}

function get_select_index(value, select)
{
	value = String(value);
	index = 0;

	for (var i = 1; i < select.length; i++)
	{
		var v = String(select[i].value);

		if (v === value)
		{
			index = i;
			break
		}
	}
	return index;
}

function load_account_sort_options(mode)
{
	var view_div = grab('view_mode');
	var view_mode = String(view_div.value);
	var html = null;
	mode = String(mode);

	if (mode !== view_mode)
	{
		view_div.value = mode;
		grab('select_builder').innerHTML = get_sort_options_html(mode);
	}
}

function get_sort_options_html(mode)
{
	mode = String(mode);
	html = "<select name=\"sort_parent\" id=\"sort_parent\" onChange=\"javascript: set_frame_list();\">";

	if (mode === "0")
	{
		html += "<option value=\"account_number\">Account Number</option>";
		html += "<option value=\"isSavings\">Account Type</option>";
		html += "<option value=\"balance\">Balance</option>";
		html += "<option value=\"date\">Date Opened</option>";
	}

	else if (mode === "1")
	{
		html += "<option value=\"date\">Transaction Date</option>";
		html += "<option value=\"action\">Transaction Type</option>";
		html += "<option value=\"b_balance\">Starting Balance</option>";
		html += "<option value=\"e_balance\">Ending Balance</option>";
	}

	html += "</select>";
	return html
}

function normal_search()
{
	grab('searchType').value = "normal";
	initialize_account_search();
}

function initialize_account_search()
{
	var search = String(grab('search').value);
	var searchType = String(grab('searchType').value)

	if (search.length !== 0)
	{
		grab('frame1').src = "/account_search/";
	}
}

function load_a_search_data()
{
	var search = parent.grab('search').value;
	var searchType = String(parent.grab('searchType').value);
	grab('search').value = search;
	grab('searchType').value = searchType;

	if (searchType === 'advanced')
	{
		var search2 = parent.grab('search2').value
		var advType = parent.grab('advType').value
		grab('search2').value = search2;
		grab('advType').value = advType
	}

	grab('search_form').submit();
}

function account_search_test()
{
	var match = String(grab('match').value);
	var search = String(grab('search').value);
	var advType = String(grab('advType').value);
	var form = grab('search_form');

	if (match === "False")
	{
		form.action = "/accountResults/";
		form.submit();
		win_visibility(1, "show");
	}
	else
	{
		parent.grab('iframe_list').src = "/final_a_loader/";
	}
}

function final_a_loader()
{
	var search = parent.grab('search').value;
	var search2 = parent.grab('search2').value;
	var searchType = parent.grab('searchType').value;
	var advType = parent.grab('advType').value;
	grab('search').value = search;
	grab('search2').value = search2;
	grab('searchType').value = searchType;
	grab('advType').value = advType;
	parent.grab('sort_parent').style.visibility = "hidden";
	parent.grab('sort_label').style.visibility = "hidden";
	parent.grab('dir_text').style.visibility = "hidden";
	parent.grab('icon').style.visibility = "hidden";
	parent.grab('hi_btn').innerHTML = "View All";
	parent.grab('hi_btn').setAttribute('onCLick', 'javascript: view_all();')
	grab('search_form').submit();
}

function set_display_search()
{	
	var html = "<div>Search for: <span id=\"s_search\"></span></div>";
	var html = "<div><span id='s_count'></span> <span id='s_phrase'> Found</span></div>";
	parent.grab('tv_builder').innerHTML = html;
}

function set_search_setting()
{
	no_results = grab('count').value;
	phrase = grab('phrase').value;
	search = String(parent.grab('search').value);
	searchType = String(parent.grab('searchType').value);
	
	if (searchType === 'advanced')
	{
		search = String(parent.grab('adv_search_crit').value);
	}

	html = "<div class=\"sr0\">Search Results:</div>";
	html += "<div class=\"sr1\">Search for: <span><em>\"" + search + "\"</em></span></div>";
	html += "<div class=\"sr2\"><span><em>(" + no_results + ") </em></span> <span>" + phrase + " </span>Found</div>";
	parent.grab('tv_builder').innerHTML = html;
	parent.grab('search').value = "";
}

function set_adv_dates(months, days_from, days_to, years)
{
	var i = 0;
	html = "";
	today = new Date();
	today = today.getDate();

	for (i = 0; i < months.length; i++)
	{
		html += "<option value=\"" + months[i]['value'] + "\">" + months[i]['option'] + "</option>";
	}

	grab('mm_fm').innerHTML = html;
	grab('mm_to').innerHTML = html;
	html = "";

	for (i = 0; i < days_from.length; i++)
	{
		html += "<option value=\"" + days_from[i] + "\">" + days_from[i] + "</option>";
	}

	grab('dd_fm').innerHTML = html;
	html = "";

	for (i = 0; i < days_to.length; i++)
	{
		html += "<option value=\"" + days_to[i] + "\">" + days_to[i] + "</option>";
	}

	grab('dd_to').innerHTML = html;
	html = "";

	for (i = 0; i < years.length; i++)
	{
		html += "<option value=\"" + years[i] + "\">" + years[i] + "</option>";
	}

	grab('yy_fm').innerHTML = html;
	grab('yy_to').innerHTML = html;

	grab('mm_to').selectedIndex = months.length - 1;
	grab('yy_to').selectedIndex = years.length - 1;
	grab('dd_to').selectedIndex = today - 1;
}

function adv_visibility(mode)
{
	var money_visibility_adv = grab('money_visibility_adv');
	var date_visibility_adv = grab('date_visibility_adv');

	if (mode === "date")
	{
		money_visibility_adv.style.opacity = "0.5";
		date_visibility_adv.style.opacity = "1.0";

		grab("dollars_fm").disabled = true;
		grab("dollars_to").disabled = true;
		grab("cents_fm").disabled = true;
		grab("cents_to").disabled = true;

		grab("mm_fm").disabled = false;
		grab("mm_to").disabled = false;
		grab("dd_fm").disabled = false;
		grab("dd_to").disabled = false;
		grab("yy_fm").disabled = false;
		grab("yy_to").disabled = false;

	}
	else if (mode === "money")
	{
		money_visibility_adv.style.opacity = "1.0";
		date_visibility_adv.style.opacity = "0.5";

		grab("mm_fm").disabled = true;
		grab("mm_to").disabled = true;
		grab("dd_fm").disabled = true;
		grab("dd_to").disabled = true;
		grab("yy_fm").disabled = true;
		grab("yy_to").disabled = true;

		grab("dollars_fm").disabled = false;
		grab("dollars_to").disabled = false;
		grab("cents_fm").disabled = false;
		grab("cents_to").disabled = false;
	}
	grab('advType').value = mode;
}

function a_adv_search_init()
{
	var proceed = true;
	var s_fm = "";
	var s_to = "";
	var isDate = grab('date_range').checked;
	parent.grab('searchType').value = 'advanced';

	if (isDate === true)
	{
		s_fm += String(grab('yy_fm').value);
		s_fm += "-";
		s_fm += String(grab('mm_fm').value);
		s_fm += "-";
		s_fm += String(grab('dd_fm').value);

		s_to += String(grab('yy_to').value);
		s_to += "-";
		s_to += String(grab('mm_to').value);
		s_to += "-";
		s_to += String(grab('dd_to').value);

		adv_s_date_fm = convert_js_months_toString(Number(grab('mm_fm').value)) + String(grab('dd_fm').value) + "/" + String(grab('yy_fm').value)
		adv_s_date_to = convert_js_months_toString(Number(grab('mm_to').value)) + String(grab('dd_to').value) + "/" + String(grab('yy_to').value)
		parent.grab('adv_search_crit').value = adv_s_date_fm + " - " + adv_s_date_to
	}

	else
	{
		var fm_cents = String(grab('cents_fm').value);
		var to_cents = String(grab('cents_to').value);
		var fm_dollars = String(grab('dollars_fm').value);
		var to_dollars = String(grab('dollars_to').value);

		if (to_dollars.length === 0)
		{
			grab('messageContent5').innerHTML = "You must enter an ending search amount";
			visibility(5, "show");
			proceed = false;
		}

		else 
		{
			if (to_cents.length === 0) {to_cents = "00";}
			if (fm_cents.length === 0) {fm_cents = "00";}
			if (fm_dollars.length === 0) {fm_dollars = "0";}

			s_fm = fm_dollars + "." + fm_cents;
			s_to = to_dollars + "." + to_cents;
			parent.grab('adv_search_crit').value = "$" + s_fm + " - $" + s_to
		}	
	}

	if (proceed === true)
	{
		var now = new Date();
		grab('search').value = s_fm;
		grab('search2').value = s_to;
		grab('dollars_fm').value = "";
		grab('dollars_to').value = "";
		grab('cents_fm').value = "";
		grab('dollars_to').value = "";
		grab('mm_fm').selectedIndex = 0;
		grab('dd_fm').selectedIndex = 0;
		grab('yy_fm').selectedIndex = 0;
		grab('mm_to').selectedIndex = (grab('mm_to').length) - 1;
		grab('dd_to').selectedIndex = now.getDate() - 1;
		grab('yy_to').selectedIndex = 0;
		visibility(3, 'hide');
		initialize_account_search();
	}
}

function convert_js_months_toString(month)
{
	if (month === 1)
	{
		month = "01/";
	}
	else if (month === 2)
	{
		month = "02/";
	}
	else if (month === 3)
	{
		month = "03/";
	}
	else if (month === 4)
	{
		month = "04/";
	}
	else if (month === 5)
	{
		month = "05/";
	}
	else if (month === 6)
	{
		month = "06/";
	}
	else if (month === 7)
	{
		month = "07/";
	}
	else if (month === 8)
	{
		month = "08/";
	}
	else if (month === 9)
	{
		month = "09/";
	}
	else if (month === 10)
	{
		month = "10/";
	}
	else if (month === 12)
	{
		month = "11/";
	}
	else if (month === 11)
	{
		month = "12/";
	}
	return month;
}



































