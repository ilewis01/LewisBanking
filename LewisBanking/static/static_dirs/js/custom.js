

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

function initialize_loans()
{
	grab('sort_parent').selectedIndex = 1;
}

function initialize_accounts()
{
	grab('sort_parent').selectedIndex = 3;
}

function initialize_acct_parent(isSearch, status, size)
{
	isSearch = Number(isSearch);
	status = Number(status);
	size = String(size);

	if (isSearch === -1)
	{
		parent.grab('tv_as_search_adv1').innerHTML = "";
		parent.grab('tv_as_search_adv2').innerHTML = "";
		parent.grab('tv_as_results').innerHTML = "";

		if (status === 1)
		{
			var message = "{ <span>All Accounts</span> }";
			parent.grab('ts_all_a').innerHTML = message;
			parent.grab('tv_as_results').innerHTML = "<em>" + size + "</em> Results Found";
		}
		else
		{
			clear_current_list('account');
		}
	}

	else if (isSearch === 1)
	{
		grab('frame_form').action = "/accountResults/";
		if (status === 1)
		{
			parent.grab('list_clear').style.visibility = "visible";
			var search_type = String(parent.grab('send_sType').value);
			var search = String(parent.grab('send_search').value);
			parent.grab('ts_all_a').innerHTML = "";

			if (search_type === 'normal')
			{
				parent.grab('tv_as_search_adv1').innerHTML = "<span style=\"font-size:17px; line-height:50px;\">Search for <span><em>\"" + search + "\"</em></span></span>";
				parent.grab('tv_as_results').innerHTML = "<em>" + size + "</em> Results Found";
				parent.grab('tv_as_search_adv2').innerHTML = "";
			}

			else if (search_type === 'advanced')
			{
				var method = String(parent.grab('send_method').value);
				var search2 = String(parent.grab('send_search2').value);

				if (method === "money")
				{
					parent.grab('tv_as_search_adv1').innerHTML = "ACCOUNT BALANCE:";
					parent.grab('tv_as_search_adv2').innerHTML = "from <em>$" + search + "</em> to <em>$" + search2 + "</em>";
					parent.grab('tv_as_results').innerHTML = "<em>" + size + "</em> Results Found";
				}

				else if (method === 'date')
				{
					search = search.replace(/-/g, "/");
					search2 = search2.replace(/-/g, "/");
					parent.grab('tv_as_search_adv1').innerHTML = "ACCOUNT OPENED:";
					parent.grab('tv_as_search_adv2').innerHTML = "from <em>" + search + "</em> to <em>" + search2 + "</em>";
					parent.grab('tv_as_results').innerHTML = "<em>" + size + "</em> Results Found";
				}
			}
		}
		else
		{
			clear_current_list('/load_account_list/', 10);
		}
	}
	parent.grab('search').value = "";
}

function check_loan_results(isSearch, status, size, location)
{
	isSearch = Number(isSearch);
	status = Number(status);
	size = String(size);

	if (status === -1)
	{
		if (isSearch === -1)
		{
			parent.grab('x0_message').innerHTML = "You currently have <em>0</em> loans";
			parent.visibility(10, 'show');
		}
		else
		{
			parent.grab('x0_message').innerHTML = "<em>0</em> &nbspMatches Found";
			clear_current_list('/load_loan_list/', 10);
		}
	}

	else if (status === 1)
	{
		if (isSearch === -1)
		{
			parent.grab('tv_as_search_adv1').innerHTML = "";
			parent.grab('tv_as_search_adv2').innerHTML = "";
			parent.grab('tv_as_results').innerHTML = "";

			var message = "{ <span>All Loans</span> }";
			parent.grab('ts_all_a').innerHTML = message;
			parent.grab('tv_as_results').innerHTML = "<em>" + size + "</em> Results Found";
		}

		else
		{
			parent.grab('list_clear').style.visibility = "visible";
			grab('frame_form').action = "/load_loan_search_results/";
			parent.grab('ts_all_a').innerHTML = "";
			var search_type = String(parent.grab('send_sType').value);
			var search = String(parent.grab('send_search').value);

			if (search_type === "normal")
			{
				parent.grab('tv_as_search_adv1').innerHTML = "<span style=\"font-size:17px; line-height:50px;\">Search for <span><em>\"" + search + "\"</em></span></span>";
				parent.grab('tv_as_results').innerHTML = "<em>" + size + "</em> Results Found";
				parent.grab('tv_as_search_adv2').innerHTML = "";
			}

			else if (search_type === "advanced")
			{
				var method = String(parent.grab('send_method').value);
				var search2 = String(parent.grab('send_search2').value);

				if (method === 'money')
				{
					parent.grab('tv_as_search_adv1').innerHTML = "TRANSACTIONS:";
					parent.grab('tv_as_search_adv2').innerHTML = "from <em>$" + search + "</em> to <em>$" + search2 + "</em>";
					parent.grab('tv_as_results').innerHTML = "<em>" + size + "</em> Results Found";
				}

				else if (method === "date")
				{
					search = search.replace(/-/g, "/");
					search2 = search2.replace(/-/g, "/");
					parent.grab('tv_as_search_adv1').innerHTML = "DATES:";
					parent.grab('tv_as_search_adv2').innerHTML = "from <em>" + search + "</em> to <em>" + search2 + "</em>";
					parent.grab('tv_as_results').innerHTML = "<em>" + size + "</em> Results Found";
				}
			}
		}
	}
	parent.grab('search').value = "";
}

function clear_current_list(target, z_index)
{
	parent.visibility(Number(z_index), 'show');
	win = parent.grab('iframe_list');
	target = String(target);
	win.src = target;
}

function reset_account_list()
{
	grab('iframe_list').src = '/load_account_list/';
	grab('list_clear').style.visibility = "hidden";
}

function reset_loan_list()
{
	grab('iframe_list').src = '/load_loan_list/';
	grab('list_clear').style.visibility = "hidden";
}

function set_sort_select_loans(select, sort)
{
	if (sort === "account_number")
	{
		select.selectedIndex = 0;
	}

	else if (sort === "balance")
	{
		select.selectedIndex = 1;
	}

	else if (sort === "start_date")
	{
		select.selectedIndex = 2;
	}

	else if (sort === "loan_amount")
	{
		select.selectedIndex = 4;
	}

	else if (sort === "loan_type")
	{
		select.selectedIndex = 5;
	}

	else if (sort === "rate")
	{
		select.selectedIndex = 6;
	}

	else if (sort === "term")
	{
		select.selectedIndex = 7;
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

function load_list_item(index)
{
	var selected_account = grab('selected_index');
	var prev_index = Number(selected_index.value);
	var prev_name = "sel" + String(prev_index) + "_div";
	var prev = grab(prev_name);

	if (prev_index % 2 == 0) {prev.className = "li_clear";}
	else {prev.className = "li_shade";}

	selected_account.value = index;
	var sel_name = "sel" + String(index) + "_div";
	var selected = grab(sel_name);
	selected.className = "li_highlight";

	var m_type = "li" + String(index) + "_type";
	var m_acct = "li" + String(index) + "_account_number";
	var type_val = String(grab(m_type).value);
	var acct_val = String(grab(m_acct).value);
	var message = type_val + " " + acct_val;
	parent.grab('curr_selected').innerHTML = message;
	parent.grab('selected_index').value = index;
}

function load_loan_item(index)
{
	var selected_loan = grab('selected_index');
	var prev_index = Number(selected_index.value);
	var prev_name = "sel" + String(prev_index) + "_div";
	var prev_low_name = "li" + String(prev_index) + "_low_class";
	var prev = grab(prev_name);
	var prev_low = grab(prev_low_name)

	if (prev_index % 2 == 0)
	{
		prev.className = "lo_clear";
		prev_low.className = "right_loan_balance2";
	}
	else 
	{
		prev.className = "lo_shade";
		prev_low.className = "right_loan_balance";
	}

	selected_loan.value = index;
	var sel_name = "sel" + String(index) + "_div";
	var low_name = "li" + String(index) + "_low_class";
	var selected = grab(sel_name);
	var low_go = grab(low_name)
	selected.className = "lo_select";
	low_go.className = "rl_selected";

	var m_type = "li" + String(index) + "_type";
	var m_acct = "li" + String(index) + "_account_number";
	var type_val = String(grab(m_type).value);
	var acct_val = String(grab(m_acct).value);
	var message = type_val + " LOAN " + acct_val;
	parent.grab('curr_selected').innerHTML = message;
	parent.grab('selected_index').value = index;
}

function load_loan(index)
{
	var prefix = "li" + String(index) + "_";
	var div_name = prefix + "change_class";
	var low_name = prefix + "low_class";
	var div = grab(div_name);
	var low = grab(low_name);
	div.className = "lo_select";
	low.className = "rl_selected";
	grab('selected_index').value = index;
	populate_loan_viewer(index);
}

function load_index(index)
{
	var prefix = "li" + String(index) + "_";
	var type_name = prefix + "type";
	var acct_name = prefix + "account_number";
	var type_val = (grab(type_name).value);
	var acct_val = (grab(acct_name).value);
	var message = type_val + " " + acct_val;
	parent.grab('curr_selected').innerHTML = message;
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

function populate_loan_viewer(index)
{
	var t_name = "li" + String(index) + "_type";
	var a_name = "li" + String(index) + "_account_number";
	var b_name = "li" + String(index) + "_format_balance";
	var r_name = "li" + String(index) + "_balance";
	var p_name = "li" + String(index) + "_payment";

	var m_type = String(grab(t_name).value);
	var m_account = String(grab(a_name).value);
	var m_balance = String(grab(b_name).value);
	var real_balance = String(grab(r_name).value);
	var m_paym = grab(p_name).value;

	if (m_type === "0") {m_type = "Personal Loan";}
	else if (m_type === "1") {m_type = "Business Loan";}
	else if (m_type === "2") {m_type = "Student Loan";}

	parent.grab('selType').innerHTML = m_type;
	parent.grab('selAcct').innerHTML = m_account;
	parent.grab('selBaln').innerHTML = m_balance;

	parent.grab('selected_type').value = m_type;
	parent.grab('selected_account_number').value = m_account;
	parent.grab('selected_balance').value = real_balance;
	parent.grab('selected_payment').value = m_paym;
	parent.grab('selected_balancef').value = m_balance;
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

function clearSelectedLo_child(index)
{
	index = Number(index);
	var view = index % 2;
	var div_name = "li" + String(index) + "_change_class";
	var low_name = "li" + String(index) + "_low_class";
	var div = grab(div_name);
	var low = grab(low_name);

	if (view == 0)
	{
		div.className = 'lo_clear';
		low.className = 'right_loan_balance2';

	}
	else
	{
		div.className = 'lo_shade';
		low.className = 'right_loan_balance';
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
	var win = parent.frame('iframe_list');
	var selected_index = String(parent.grab('selected_index').value);

	var prefix = "li" + selected_index + "_";
	var ac_name = prefix + "account_number";
	var tp_name = prefix + "type";
	
	var account_number = win.grab(ac_name).value
	var w_type = win.grab(tp_name).value;

	grab('w_acct').innerHTML = account_number;
	grab('w_types').innerHTML = w_type;
	grab('account_number').value = account_number;
	grab('d_type').value = w_type;
}

function init_payment()
{
	var balance = parent.grab('selected_balancef').value;
	var payment = parent.grab('selected_payment').value;
	var account_number = parent.grab('selected_account_number').value;

	grab('loan_balance').innerHTML = balance;
	grab('min_payment').innerHTML = payment;
	grab('account_number').value = account_number;
	grab('minimim_payment').value = payment;
}

function load_refinance_data()
{
	var account_number = parent.grab('selected_account_number').value;
	grab('account_number').value = account_number;
	grab('bank_form').submit();
}

function g_error(form)
{
	proceed = true;
	var dollars = String(grab('dollars').value);
	var minimum = String(grab('minimim_payment').value);
	var min = "";
	var cents = grab('cents');

	for (var i = 0; i < minimum.length; i++)
	{
		if (minimum.charAt(i) !== ",")
		{
			min += minimum.charAt(i);
		}
	}

	grab('minimim_payment').value = min;

	if (dollars.length === 0 && String(cents.value).length === 0)
	{
		parent.grab('messageContent').innerHTML = "You must enter a valid dollar amount";
		parent.grab("messageHeader").innerHTML = "<span>Errors Detected</span>"
		var e_win = parent.grab('messageWindow');
		e_win.style.height = "260px";
		win_visibility(2, "show");
		proceed = false;
	}

	if (String(cents.value).length === 0)
	{
		cents.value = "00";
	}

	dollars = dollars + "." + String(cents.value);

	if (parseFloat(dollars) < parseFloat(min))
	{
		parent.grab('messageContent').innerHTML = "Payment must be at least $" + String(min);
		parent.grab("messageHeader").innerHTML = "<span>Errors Detected</span>"
		var e_win = parent.grab('messageWindow');
		e_win.style.height = "260px";
		win_visibility(2, "show");
		proceed = false;
	}

	if (proceed === true)
	{
		grab('bank_form').submit();
	}
}


function w_error()
{
	var dollars = String(grab('dollars').value);
	var win = parent.frame('iframe_list');
	var selected_index = String(parent.grab('selected_index').value);
	var b_name = "li" + selected_index + "_balance";
	var balance = String(win.grab(b_name).value);
	balance = parseFloat(balance);
	
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
	parent.grab('selected_index').value = 0;
}

function init_history()
{
	grab('frame2').src = "/view_history0/";
	visibility(6, 'show');
}

function load_history()
{
	var selected_index = String(parent.grab('selected_index').value);
	var win = parent.frame('iframe_list');
	acct_name = "li" + selected_index + "_account_number";
	var account_number = win.grab(acct_name).value;
	grab('account_number').value = account_number;
	grab('load_form').submit();
}

function initialize_account_history(account_type, account_number)
{
	parent.grab('history_type').innerHTML = account_type;
	parent.grab('history_acct').innerHTML = account_number;
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



function normal_search_loans()
{
	var win = frame('iframe_list');
	win.grab('searchType').value = "normal";
	var search = String(grab('search').value);
	win.grab('search').value = search;
	initialize_loan_search();
}

function advanced_search_loans()
{
	var win = frame('iframe_list');
	var method = grab('amt_range').checked;
	var fm_search = "";
	var to_search = "";
	win.grab('searchType').value = "advanced";

	if (method === true)
	{
		method = "money";
		var fm_cents = String(grab('cents_fm').value);
		var to_cents = String(grab('cents_to').value);
		var dollars_fm = String(grab('dollars_fm').value);
		var dollars_to = String(grab('dollars_to').value);

		if (dollars_fm.length === 0)
		{
			dollars_fm = "0";
		}

		if (fm_cents.length === 0) {fm_cents = "00";}
		if (to_cents.length === 0) {to_cents = "00";}

		if (dollars_to.length === 0 || Number(dollars_to) < Number(dollars_fm))
		{
			alert("ERROR: SEND A ERROR MESSAGE TO SCREEN");
		}

		fm_search =  dollars_fm + "." + fm_cents;
		to_search =  dollars_to + "." + to_cents;
	}

	else
	{
		method = "date";
		var mm_fm = String(grab('mm_fm').value);
		var dd_fm = String(grab('dd_fm').value);
		var yy_fm = String(grab('yy_fm').value);
		var mm_to = String(grab('mm_to').value);
		var dd_to = String(grab('dd_to').value);
		var yy_to = String(grab('yy_to').value);
		fm_search = mm_fm + "-" + dd_fm + "-" + yy_fm;
		to_search = mm_to + "-" + dd_to + "-" + yy_to;
	}

	win.grab('searchMethod').value = method;
	win.grab('search').value = fm_search;
	win.grab('search2').value = to_search;
	visibility(3, "hide");
	initialize_loan_search();
}

function initialize_loan_search()
{
	var win = frame('iframe_list');
	var search = String(win.grab('search').value);

	if (search.length !== 0)
	{
		var form = win.grab('frame_form');
		form.action = "/loan_search/";
		form.submit();
	}
}

function load_loan_search()
{
	var searchType = String(parent.grab('searchType').value);
	var search = parent.grab('search').value;
	var size = parent.grab('size').value;
	grab('search').value = search;
	grab('searchType').value = searchType;
	grab('size').value = size;
	
	if (searchType === "advanced")
	{
		var search2 = parent.grab('search2').value;
		var method = parent.grab('date_range').checked;

		if (method === false) {method = "money";}
		else {method = "date";}

		grab('searchMethod').value = method;
		grab('search2').value = search2;
	}

	grab('bank_form').submit();
}

function initialize_account_search()
{
	grab('iframe_list').src = "/account_search/";
}

function initialize_loan_search()
{
	grab('iframe_list').src = "/loan_search/";
}

function load_account_search_data()
{
	var search = parent.grab('send_search').value;
	var search2 = parent.grab('send_search2').value;
	var method = parent.grab('send_method').value;
	var s_type = parent.grab('send_sType').value;
	grab('search').value = search;
	grab('search2').value = search2;
	grab('searchType').value = s_type;
	grab('searchMethod').value = method;
	grab('frame_form').submit();
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

function set_adv_dates(months, days_from, days_to, years, joined)
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
	grab('dd_fm').selectedIndex = Number(joined) - 1
	adv_visibility('money');
}

function reset_adv_win()
{
	grab('amt_range').checked = true;
	adv_visibility("money");
	visibility(3, 'hide');
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

		grab('dollars_fm').value = "";
		grab('dollars_to').value = "";
		grab('cents_fm').value = "";
		grab('cents_to').value = "";

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
}

function normal_loan_search_init()
{
	var search = String(grab('search').value);
	grab('send_search').value = search;
	grab('send_sType').value = "normal";
	grab('searchType').value = "normal";

	if (search.length !== 0)
	{
		initialize_loan_search();
	}
}

function normal_search_init()
{
	var search = String(grab('search').value);
	grab('send_search').value = search;
	grab('send_sType').value = "normal";
	grab('searchType').value = "normal";

	if (search.length !== 0)
	{
		initialize_account_search();
	}
}

function a_adv_search_init()
{
	var proceed = true;
	var s_fm = "";
	var s_to = "";
	var isDate = grab('date_range').checked;
	grab('searchType').value = 'advanced';
	grab('send_sType').value = 'advanced';

	if (isDate === true)
	{
		grab('searchMethod').value = "date";
		grab('send_method').value = "date";
		s_fm += String(grab('mm_fm').value);
		s_fm += "-";
		s_fm += String(grab('dd_fm').value);
		s_fm += "-";
		s_fm += String(grab('yy_fm').value);

		s_to += String(grab('mm_to').value);
		s_to += "-";
		s_to += String(grab('dd_to').value);
		s_to += "-";
		s_to += String(grab('yy_to').value);

		t1 = String(mm_fm.value) + String(dd_fm.value) + String(yy_fm.value);
		t2 = String(mm_to.value) + String(dd_to.value) + String(yy_to.value);

		t1 = Number(t1);
		t2 = Number(t2);

		if (t2 < t1)
		{
			grab('messageContent5').innerHTML = "The upper bound date must be greater than the lower bound date";
			visibility(5, "show");
			proceed = false;
		}

		adv_s_date_fm = convert_js_months_toString(Number(grab('mm_fm').value)) + String(grab('dd_fm').value) + ", " + String(grab('yy_fm').value)
		adv_s_date_to = convert_js_months_toString(Number(grab('mm_to').value)) + String(grab('dd_to').value) + ", " + String(grab('yy_to').value)
	}

	else
	{
		grab('searchMethod').value = "money";
		grab('send_method').value = "money";
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

			if (parseFloat(s_fm) > parseFloat(s_to))
			{
				grab('messageContent5').innerHTML = "The upper bound value must be greater or equal to the lower bound value";
				visibility(5, "show");
				proceed = false;
			}
		}	
	}

	grab('send_search').value = s_fm;
	grab('send_search2').value = s_to;
	grab('search').value = s_fm;
	grab('search2').value = s_to;

	if (proceed === true)
	{
		var now = new Date();
		grab('dollars_fm').value = "";
		grab('dollars_to').value = "";
		grab('cents_fm').value = "";
		grab('dollars_to').value = "";
		reset_adv_win();
		initialize_account_search();
	}
}

function l_adv_search_init()
{
	var proceed = true;
	var s_fm = "";
	var s_to = "";
	var isDate = grab('date_range').checked;
	grab('searchType').value = 'advanced';
	grab('send_sType').value = 'advanced';

	if (isDate === true)
	{
		grab('searchMethod').value = "date";
		grab('send_method').value = "date";
		s_fm += String(grab('mm_fm').value);
		s_fm += "-";
		s_fm += String(grab('dd_fm').value);
		s_fm += "-";
		s_fm += String(grab('yy_fm').value);

		s_to += String(grab('mm_to').value);
		s_to += "-";
		s_to += String(grab('dd_to').value);
		s_to += "-";
		s_to += String(grab('yy_to').value);

		t1 = String(mm_fm.value) + String(dd_fm.value) + String(yy_fm.value);
		t2 = String(mm_to.value) + String(dd_to.value) + String(yy_to.value);

		t1 = Number(t1);
		t2 = Number(t2);

		if (t2 < t1)
		{
			grab('messageContent5').innerHTML = "The upper bound date must be greater than the lower bound date";
			visibility(5, "show");
			proceed = false;
		}

		adv_s_date_fm = convert_js_months_toString(Number(grab('mm_fm').value)) + String(grab('dd_fm').value) + ", " + String(grab('yy_fm').value)
		adv_s_date_to = convert_js_months_toString(Number(grab('mm_to').value)) + String(grab('dd_to').value) + ", " + String(grab('yy_to').value)
	}

	else
	{
		grab('searchMethod').value = "money";
		grab('send_method').value = "money";
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

			if (parseFloat(s_fm) > parseFloat(s_to))
			{
				grab('messageContent5').innerHTML = "The upper bound value must be greater or equal to the lower bound value";
				visibility(5, "show");
				proceed = false;
			}
		}	
	}

	grab('send_search').value = s_fm;
	grab('send_search2').value = s_to;
	grab('search').value = s_fm;
	grab('search2').value = s_to;

	if (proceed === true)
	{
		var now = new Date();
		grab('dollars_fm').value = "";
		grab('dollars_to').value = "";
		grab('cents_fm').value = "";
		grab('dollars_to').value = "";
		reset_adv_win();
		initialize_loan_search();
	}
}

function w_error_uLoan()
{
	var dollars = String(grab('dollars').value);
	var cents = String(grab('cents').value);

	if (cents.length === 0)
	{
		grab('cents').value = "00";
		cents = "00";
	}

	if (dollars.length === 0)
	{
		parent.grab('messageContent').innerHTML = "You must enter a loan amount";
		parent.grab("messageHeader").innerHTML = "<span>Errors Detected</span>"
		var e_win = parent.grab('messageWindow');
		e_win.style.height = "260px";
		win_visibility(2, "show");
	}

	else 
	{
		grab('bank_form').submit();
	}
}

function init_user_loan_input(action, a_list)
{
	var html = "";
	var i = 0;
	action = String(action);

	if (action === "0")
	{
		html += "<select name=\"deposit_account\" id=\"deposit_account\">";

		for (i = 0; i < a_list.length; i++)
		{
			html += "<option value=\"" + String(a_list[i]['value']) + "\">" + String(a_list[i]['option']) + "</option>";
		}

		html += "</select>";
	}

	else if (action === "1")
	{
		html += "<table><tr>";
		html += "<td><div><input type=\"radio\" name=\"account_type\" value=\"False\" checked></div></td>";
		html += "<td><div class=\"l_deny_text_radio\">Checking</div></td>";
		html += "<td><div><input type=\"radio\" name=\"account_type\" value=\"True\"></div></td>";
		html += "<td><div class=\"l_deny_text_radio\">Savings</div></td>";
		html += "</tr></table>";
	}

	grab('loan_decision_input').innerHTML = html;
}

function load_payment_data()
{
	grab('account_number').value = parent.grab('selected_account_number').value;
	grab('bank_form').submit();
}

function load_loan_history()
{
	grab('direction_history').value = "descend";
	grab('sort_history').value = "date";
	grab('dir_text_history').innerHTML = "Descending";
	grab('icon_history').innerHTML = "<i class=\"fa fa-chevron-circle-down\" aria-hidden=\"true\"></i>";
	grab('frame2').src = '/view_loan_history0/';
	visibility(6, 'show');
}

function load_load_id()
{
	grab('account_number').value = parent.grab('selected_account_number').value;
	grab('sort').value = "date";
	grab('direction').value = "descend";
	grab('bank_form').submit()
}

function toggle_carat_history()
{
	var icon = grab('icon_history');
	var title = grab('dir_text_history');
	var hidden = grab('direction_history')
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

function reload_mega_history()
{
	var win = frame('frame2');
	win.grab('sort').value = grab('sort2').value;
	win.grab('direction').value = grab('direction_history').value;
	win.grab('history_form').submit();
}

function load_history_val()
{
	var tp = String(parent.grab('selected_type').value);

	if (tp === "0") {tp = "Personal Loan"; }
	else if (tp === "1") {tp = "Business Loan"; }
	else if (tp === "2") {tp = "Student Loan"; }

	parent.grab('history_type').innerHTML = tp;
	parent.grab('history_acct').innerHTML = parent.grab('selected_account_number').value;
}

function clear_d_search()
{
	parent.grab('search').value = "";
	visibility(7, "hide");
}

function update_parent_phone(phone)
{
	parent.grab('phone_span').innerHTML = phone;
}

function track_pInput()
{
	var btn = grab('btn');
	var p0 	= String(grab('old').value);
	var p1 	= String(grab('password1').value);
	var p2 	= String(grab('password2').value);

	if (p0.length !== 0 && p1.length !== 0 && p2.length !== 0)
	{
		btn.setAttribute('type', 'button');
		btn.setAttribute('onClick', 'javascript: changePasswordButton();')
	}
	else
	{
		btn.removeAttribute('onClick');
		btn.setAttribute('type', 'submit');
	}
}

function changePasswordButton()
{
	var p1 	= String(grab('password1').value);
	var p2 	= String(grab('password2').value);

	if (p1 !== p2) {visibility(1, 'show');}
	else {grab('bank_form').submit();}
}

function init_transaction_history()
{
	grab('sort').value = "date";
	grab('direction').value = "descend";
	grab('frame_form').submit();
}

function sort_h_list()
{
	var win = frame('tFrame');
	var sort = grab('sort_parent').value;
	var direction = grab('direction_parent').value;
	win.grab('sort').value = sort;
	win.grab('direction').value = direction;
	win.grab('frame_form').submit();
}

function init_history_radio() {
	var date_div = grab('delv1');
	var money_div = grab('delv2');
	var search_div = grab('search');
	var normal = grab('normal').checked;
	var date = grab('date').checked;
	var money = grab('money').checked;

	if (normal === true)
	{
		grab('fm_mm').disabled = true;
		grab('fm_dd').disabled = true;
		grab('fm_yy').disabled = true;
		grab('to_mm').disabled = true;
		grab('to_dd').disabled = true;
		grab('to_yy').disabled = true;

		grab('fm_dollar').disabled = true;
		grab('to_dollar').disabled = true;
		grab('fm_cents').disabled = true;
		grab('to_cents').disabled = true;

		grab('fm_dollar').value = "";
		grab('to_dollar').value = "";
		grab('fm_cents').value = "";
		grab('to_cents').value = "";

		date_div.style.opacity = "0.5";
		money_div.style.opacity = "0.5";

		grab('search').disabled = false;
		grab('search').style.opacity = "1.0";

		grab('searchType').value = "normal";
	}

	else if (date === true)
	{
		grab('fm_mm').disabled = false;
		grab('fm_dd').disabled = false;
		grab('fm_yy').disabled = false;
		grab('to_mm').disabled = false;
		grab('to_dd').disabled = false;
		grab('to_yy').disabled = false;

		grab('fm_dollar').disabled = true;
		grab('to_dollar').disabled = true;
		grab('fm_cents').disabled = true;
		grab('to_cents').disabled = true;

		grab('fm_dollar').value = "";
		grab('to_dollar').value = "";
		grab('fm_cents').value = "";
		grab('to_cents').value = "";

		date_div.style.opacity = "1.0";
		money_div.style.opacity = "0.5";

		grab('search').disabled = true;
		grab('search').style.opacity = "0.5";

		grab('searchType').value = "advanced";
		grab('searchMethod').value = "date";
	}

	else if (money === true)
	{
		grab('fm_mm').disabled = true;
		grab('fm_dd').disabled = true;
		grab('fm_yy').disabled = true;
		grab('to_mm').disabled = true;
		grab('to_dd').disabled = true;
		grab('to_yy').disabled = true;

		grab('fm_dollar').disabled = false;
		grab('to_dollar').disabled = false;
		grab('fm_cents').disabled = false;
		grab('to_cents').disabled = false;

		date_div.style.opacity = "0.5";
		money_div.style.opacity = "1.0";

		grab('search').disabled = true;
		grab('search').style.opacity = "0.5";

		grab('searchType').value = "advanced";
		grab('searchMethod').value = "money";
	}
}

function load_premium_dates(years, months, day)
{
	var mm_html = "";
	var yy_html = "";
	var i = 0;
	day = Number(day) - 1;

	for (i = 0; i < months.length; i++)
	{
		mm_html += "<option value=\"" + months[i]['value'] + "\">" + months[i]['option'] + "</option>";
	}

	for (i = 0; i < years.length; i++)
	{
		yy_html += "<option value=\"" + years[i] + "\">" + years[i] + "</option>";
	}

	grab('fm_mm').innerHTML = mm_html;
	grab('to_mm').innerHTML = mm_html;
	grab('fm_yy').innerHTML = yy_html;
	grab('to_yy').innerHTML = yy_html;

	grab('to_mm').selectedIndex = months.length - 1;
	grab('to_yy').selectedIndex = years.length - 1;

	load_days(grab('fm_dd'), grab('fm_mm'), grab('fm_yy'));
	load_days(grab('to_dd'), grab('to_mm'), grab('to_yy'));

	grab('fm_dd').selectedIndex = day;
	grab('to_dd').selectedIndex = grab('to_dd').length - 1;
}

function load_days(div, mm_div, yy_div)
{
	var html = "";
	var mm = Number(mm_div.value);
	var yy = Number(yy_div.value);
	var num_days = fetch_days(mm, yy);

	for (var i = 1; i <= num_days; i++)
	{
		html += "<option value\"" + String(i) + "\">" + String(i) + "</option>";
	}

	div.innerHTML = html;
}


function fetch_days(mm, yy)
{
	var num_days = 31;
	var today = new Date();
	mm = Number(mm);
	yy = Number(yy);

	if (mm === 2)
	{
		num_days = 28;

		if (yy % 4 === 0)
		{
			num_days = 29;
		}
	}

	else if (mm === 4 || mm === 6 || mm === 9 || mm === 11)
	{
		num_days = 30;
	}

	if (mm === (today.getMonth() + 1) && yy === today.getFullYear())
	{
		num_days = today.getDate();
	}
	return num_days
}

function fetch_tsearch_errors()
{
	var proceed = true;
	var message_div = grab('th_error_message');
	var method = "";
	var search_type = "";
	var fm_search = "";
	var to_search = "";
	var search_phrase = "";

	if (grab('normal').checked === true)
	{
		search_type = "normal";
		var search = String(grab('search').value);

		if (search.length === 0)
		{
			message_div.innerHTML = "You must valid enter search criteria"
			visibility(5, 'show');
			proceed = false;
		}
		else
		{
			fm_search = search;
			search_phrase = "Search for: <em>\"" + String(search) + "\"</em";
		}
	}

	else if (grab('date').checked === true)
	{
		method = "date";
		search_type = "advanced";
		var f1 = String(grab('fm_mm').value) + String(grab('fm_dd').value) + String(grab('fm_yy').value);
		var f2 = String(grab('to_mm').value) + String(grab('to_dd').value) + String(grab('to_yy').value);
		f1 = Number(f1);
		f2 = Number(f2);

		if (f2 < f1)
		{
			message_div.innerHTML = "The max date cannot be before the min date";
			visibility(5, 'show');
			proceed = false;
		}

		else
		{
			sp1 = String(grab('fm_mm').value) + "/" + String(grab('fm_dd').value) + "/" + String(grab('fm_yy').value);
			sp2 = String(grab('to_mm').value) + "/" + String(grab('to_dd').value) + "/" + String(grab('to_yy').value);
			fm_search = String(grab('fm_mm').value) + "-" + String(grab('fm_dd').value) + "-" + String(grab('fm_yy').value);
			to_search = String(grab('to_mm').value) + "-" + String(grab('to_dd').value) + "-" + String(grab('to_yy').value);
			search_phrase = "<span>DATES BETWEEN:</span><br><em>" + sp1 + "</em> and <em>" + sp2 + "</em>";
		}
	}

	else if (grab('money').checked === true)
	{
		method = "money";
		search_type = "advanced";
		var fm_dollar 	= grab('fm_dollar');
		var to_dollar 	= grab('to_dollar');
		var fm_cents 	= grab('fm_cents');
		var to_cents 	= grab('to_cents');

		if (String(fm_cents.value).length === 0) {fm_cents.value = "00";}
		if (String(to_cents.value).length === 0) {to_cents.value = "00";}
		if (String(fm_dollar.value).length === 0) {fm_dollar.value = "0";}

		if (String(to_dollar.value).length === 0)
		{
			message_div.innerHTML = "You must enter a valid value for the upper bound"
			visibility(5, 'show');
			proceed = false;
		}

		var fm1 = String(fm_dollar.value) + "." + String(fm_cents.value);
		var fm2 = String(to_dollar.value) + "." + String(to_cents.value);
		fm_search = parseFloat(fm1);
		to_search = parseFloat(fm2);
		search_phrase = "TRANSACTIONS BETWEEN:<br><em>$" + fm_search + "</em> and <em>$" + to_search + "</em>";
		
		if (fm_search > to_search)
		{
			message_div.innerHTML = "The upper bound cannot be smaller than the lower bound";
			visibility(5, 'show');
			proceed = false;
		}
	}

	if (proceed === true)
	{
		grab('search_phrase').value = search_phrase;
		var win = frame('tFrame');
		win.grab('sort').value

		win.grab('searchMethod').value = method;
		win.grab('searchType').value = search_type;
		win.grab('search').value = fm_search;
		win.grab('search2').value = to_search;
		win.grab('frame_form').action = "/load_history_search/";
		win.grab('frame_form').submit();
	}
}

function initialize_transaction_search(isSearch, size)
{
	isSearch = Number(isSearch);
	size = Number(size)

	if (isSearch === -1)
	{		
		parent.grab('ts_all').innerHTML = "<span>{</span> All Transaction History <span>}</span>";
		parent.grab('ts_results').innerHTML = "";
		parent.grab('ts_title').innerHTML = "";
		parent.grab('ts_message').innerHTML = "";
	}
	else if (isSearch === 1)
	{
		if (size === 0)
		{
			parent.grab('ts_all').innerHTML = "";
			parent.grab('ts_results').innerHTML = "<em>0</em> records found for <em>\"" + String(parent.grab('search').value) + "\"</em>";
			parent.grab('ts_message').innerHTML = "<i class=\"fa fa-info-circle\" aria-hidden=\"true\"></i> Click the clear button to continue";
			parent.grab('ts_title').innerHTML = "";
		}
		else
		{
			var phrase = " matches ";
			if (size === 1) {phrase = " match ";}

			parent.grab('ts_results').innerHTML = "<em>" + String(size) + "</em>" + phrase + "found";
			parent.grab('ts_message').innerHTML = "<i class=\"fa fa-info-circle\" aria-hidden=\"true\"></i> Click the clear button to view all";
			parent.grab('ts_title').innerHTML = parent.grab('search_phrase').value;
			parent.grab('ts_all').innerHTML = "";
			grab('frame_form').action = "/load_history_search/";
		}
	}
	parent.grab('search').value = "";
}

function clear_transaction_search()
{
	grab('normal').checked = true;
	init_history_radio();
	grab('tFrame').src = "/t_history_list/";
}

function restart_pr()
{
	parent.grab('prFrame').src = "/pr0/";
}

function restore_pr_window()
{
	var wrapper = parent.grab('passwordRecovery');
	wrapper.className = "passwordRecovery";
	parent.grab('prFrame').src = "/pr0/";
}

function restore_pr_size()
{
	var wrapper = parent.grab('passwordRecovery');
	wrapper.className = "passwordRecovery";
}

function change_pr_size()
{
	var wrapper = parent.grab('passwordRecovery');
	wrapper.className = "passwordRecovery2";
}

function init_loan_list()
{

}








































