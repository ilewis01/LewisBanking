

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

function initialize_accounts()
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

function load_url(url)
{
	var form = grab("bank_form");
	form.action = url;
	form.submit();
}

function load_list_item(item_id)
{
	// clearSelectedLI_child();

	var acct_name = item_id + "account_number";
	var date_name = item_id + "date";
	var balance_name = item_id + "balance";
	var type_name = item_id + "type";
	var div_name = item_id + "change_class";

	var account_number = grab(acct_name).value;
	var date = grab(date_name).value;
	var balance = grab(balance_name).value;
	var m_type = grab(type_name).value;

	var hid_acct = parent.grab('selected_account_number');
	var hid_date = parent.grab('selected_date');
	var hid_baln = parent.grab('selected_balance');
	var hid_type = parent.grab('selected_type');

	hid_acct.value = account_number;
	hid_date.value = date;
	hid_type.value = m_type;
	hid_baln.value = balance;

	parent.grab('selAcct').innerHTML = account_number;
	parent.grab('selBaln').innerHTML = balance;
	parent.grab('selDate').innerHTML = date;
	parent.grab('selType').innerHTML = m_type;

	// div = grab(div_name);
	// div.style.backgroundColor = "yellow";
	// grab('return_class').value = div.className;
	// var cng = item_id + "change_class";
	// grab('selected_li').value = cng;
	
}

function clearSelectedLI_child()
{
	var current_id = grab('selected_li').value;
	var div = grab(current_id);
	div.removeAttribute('backgroundColor');
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
	grab('w_types').innerHTML = w_type;
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

































