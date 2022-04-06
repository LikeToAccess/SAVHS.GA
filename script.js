window.console = window.console || function(t) {};
if (document.location.search.match(/type=embed/gi)) {
	window.parent.postMessage("resize", "*");
}

loadJSON = function() {
	var iterations = 0;
	obj.forEach(function(element) {
		iterations += 1;
		if (element.menu_type) {
			const menu_type_default = document.getElementById("menu_type#" + iterations); menu_type_default.remove();
			var card = document.getElementById("card#" + iterations);

			const menu_type = document.createElement("p");
			menu_type.setAttribute("class", "card-text");

			const lunch_items = document.createElement("i");
			lunch_items.setAttribute("class", "smalltext");

			var children = menu_type.children.length + 1
			menu_type.appendChild(document.createTextNode(String(element.menu_type).replaceAll(" - SANB Secondary School", "")));
			const line_break = document.createElement("br");
			menu_type.appendChild(line_break);
			lunch_items.appendChild(document.createTextNode(String(element.lunch_items).replaceAll(",", ", ")));
			card.appendChild(menu_type);
			menu_type.appendChild(lunch_items);
		}
	});
}

loadLunch = function() {
	var today = new Date();
	var dd = String(today.getDate()).padStart(2, '0');
	var mm = String(today.getMonth() + 1).padStart(2, '0');
	var yyyy = today.getFullYear();

	var current_lunch_link_url = "logs/LD_" + yyyy + "-" + mm + '-' + dd + ".json";
	var current_lunch_link = document.getElementById("current_lunch_json");
	var current_lunch_script = document.getElementById("current_lunch_script");
	current_lunch_link.setAttribute("href", current_lunch_link_url);
	current_lunch_script.setAttribute("src", current_lunch_link_url + ".js");
}

function onSignIn(googleUser) {
	var profile = googleUser.getBasicProfile();
	var id = profile.getId();
	var name = profile.getName();
	var imageUrl = profile.getImageUrl();
	var email = profile.getEmail();
	console.log('ID: ' + id); // Do not send to your backend! Use an ID token instead.
	console.log('Name: ' + name);
	console.log('Image URL: ' + imageUrl);
	console.log('Email: ' + email); // This is null if the 'email' scope is not present.
}

if (window.location.href == "https://savhs.ga/lunch/") {
	loadLunch();
}

function signOut() {
	var auth2 = gapi.auth2.getAuthInstance();
	auth2.signOut().then(function () {
		console.log('User signed out.');
	});
}

// console.log('ID: ' + id); // Do not send to your backend! Use an ID token instead.
// console.log('Name: ' + name);
// console.log('Image URL: ' + imageUrl);
// console.log('Email: ' + email); // This is null if the 'email' scope is not present.
