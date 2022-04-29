window.console = window.console || function(t) {};
if (document.location.search.match(/type=embed/gi)) {
	window.parent.postMessage("resize", "*");
}

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
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

loadInstagramData = function() {
	var iterations = 0;
	instagramData[0].forEach(function(element) {
		iterations += 1;
	});

	var index = getRandomInt(iterations);

	console.log(iterations);
	console.log(index);
	console.log(instagramData[0][index]);

	var text = instagramData[0][index][0]["text"].replace("congrats!", "Congradulations!");
	const linked_handle = document.createElement("a")
	linked_handle.setAttribute("href", "https://instagram.com/"+text.split("@")[1]);
	linked_handle.setAttribute("style", "font-size: inherit; color: inherit;");
	linked_handle.setAttribute("target", "_blank");
	linked_handle.innerText = "@" + text.split("@")[1];

	randomInstagramImage = document.getElementById("random-instagram-image")
	randomInstagramText = document.getElementById("random-instagram-text")

	randomInstagramImage.setAttribute("src", "https://savhs.ga/savhsseniors2022/"+instagramData[0][index][0]["image_filename"])
	randomInstagramImage.parentElement.setAttribute("href", "https://instagram.com/"+text.split("@")[1])
	randomInstagramText.innerText = text.split("@")[0]
	randomInstagramText.appendChild(linked_handle);
	return instagramData[0][index];
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
	if (
		[
			"https://savhs.ga/account/",
			"https://www.savhs.ga/account/"
		].includes(window.location.href)
	) {
		displayAccountDetails(id, name, imageUrl, email);
	}
	else if (
		[
			"https://www.savhs.ga/",
			"https://savhs.ga/"
		].includes(window.location.href)
	) {
		displayAccountDetails(id, name, imageUrl, email);
		var flapLink = document.getElementById("flap-link");
		flapLink.removeAttribute("class");
		flapLink.removeAttribute("title");
		flapLink.parentElement.removeAttribute("class");
		flapLink.setAttribute("href", "https://savhs.ga/flap/");

		var discordLink = document.getElementById("discord-link");
		discordLink.removeAttribute("class");
		discordLink.removeAttribute("title");
		discordLink.parentElement.removeAttribute("class");
		discordLink.setAttribute("href", "https://discord.gg/BAcDKa3j3j");
	}
	else if (
		[
			"https://www.savhs.ga/flap/",
			"https://savhs.ga/flap/"
		].includes(window.location.href)
	) {
		// displayAccountDetails(id, name, imageUrl, email);
		// console.log("TEST");
		document.getElementById("flap-h1").innerText = "Flap Bird";
		document.getElementById("flap-p").removeAttribute("hidden");
		document.getElementById("container").removeAttribute("hidden");
	}
	var discordNavLink = document.getElementById("discord-nav-link");
	discordNavLink.setAttribute("class", "nav-link");
	discordNavLink.removeAttribute("title");
	discordNavLink.parentElement.setAttribute("class", "nav-item");
	discordNavLink.setAttribute("href", "https://discord.gg/BAcDKa3j3j");

	var loginLink = document.getElementById("login-link");
	loginLink.setAttribute("class", "grey disabled");
	loginLink.setAttribute("title", "Already logged in.");
	loginLink.removeAttribute("href")

	var logoutLink = document.getElementById("logout-link");
	logoutLink.removeAttribute("class");
	logoutLink.removeAttribute("title");
	logoutLink.setAttribute("href", "");
	logoutLink.setAttribute("onclick", "signOut();");
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

function getDomainGroupAssociation(username) {
	console.log(username);
	var groups = [];

	domain_group_memberships.forEach(function(element) {
		for (const [key, value] of Object.entries(element)) {
			for (var i = 0; i < element[key].length; i++) {
				// console.log(element[key][i]);
				// console.log(element[key][i].member.includes("ISD282\\" + username));
				if (element[key][i].member.includes("ISD282\\" + username)) {
					groups.push(element[key][i]);
				}
			}
		}
		// console.log(element.domain_users)
	});

	return groups;
}

function displayAccountDetails(id, name, imageUrl, email) {
	groups = getDomainGroupAssociation(email.replace("@isd282.org", ""));
	for (var i = 0; i < groups.length; i++) {
		console.log(groups[i].group);
		name = name.concat(", ", groups[i].group)
	}

	var username_field = document.getElementById("username");
	username_field.innerText = name;
	username_field.parentNode.removeAttribute("hidden");
	// console.log(name);
}

function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}

function spinWebsite(spins) {
	// var spin = document.getElementById("spin");
	// spin.setAttribute("class", "spin");
	// await sleep(1000);
	// spin.removeAttribute("class");
	document.getElementById("spin").style.transform = "rotate(" + 360 * spins + "deg)";
}

function listenForSpinKeys(spinKeyCodes) {
	var spins = 0;
	document.addEventListener("keydown", function(event) {
		if (spinKeyCodes.includes(event.keyCode)) {
			spins++;
			// if (spins > 100) {spins += spins}
			spinWebsite(spins);
		}
	});
}

listenForSpinKeys([82, 83]);









// function streamVideo(videoFilename) {
// 	var stream = new FileStream(videoFilename, FileMode.Open, FileAccess.Read , FileShare.Read);

// 	// var mediaType = MediaTypeHeaderValue.Parse($"video/{videoFormat}");
// 	mediaType = MediaTypeHeaderValue.Parse("video/mp4")

// 	if (Request.Headers.Range != null)
// 	{
// 		try
// 		{
// 			var partialResponse = Request.CreateResponse(HttpStatusCode.PartialContent);
// 			partialResponse.Content = new ByteRangeStreamContent(stream, Request.Headers.Range, mediaType);

// 			return partialResponse;
// 		}
// 		catch (InvalidByteRangeException invalidByteRangeException)
// 		{
// 			return Request.CreateErrorResponse(invalidByteRangeException);
// 		}
// 	}
// 	else
// 	{
// 		// If it is not a range request we just send the whole thing as normal
// 		var fullResponse = Request.CreateResponse(HttpStatusCode.OK);

// 		fullResponse.Content = new StreamContent(stream);
// 		fullResponse.Content.Headers.ContentType = mediaType;

// 		return fullResponse;
// 	}
// }

// streamVideo("video.mp4");

