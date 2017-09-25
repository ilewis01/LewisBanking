

//	grab(string): Returns the html element "data"
function grab(data) 
{
	data = String(data);
	var element = document.getElementById(data);
	return element;
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
		data.push("You must an account type");
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

function runTest()
{

}










