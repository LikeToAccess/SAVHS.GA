window.console = window.console || function(t) {};
if (document.location.search.match(/type=embed/gi)) {
	window.parent.postMessage("resize", "*");
}

// loadJSON = function() {
// 	obj.forEach(function(element) {
// 		var ul = document.getElementById("list");
// 		var menu_type = document.createElement("li");
// 		var lunch_items = document.createElement("li");
// 		var children = ul.children.length + 1
// 		// menu_type.setAttribute("id", "item#"+children)
// 		menu_type.setAttribute("class", "menu_type")
// 		lunch_items.setAttribute("class", "lunch_items")
// 		menu_type.appendChild(document.createTextNode(element.menu_type));
// 		lunch_items.appendChild(document.createTextNode(element.lunch_items));
// 		ul.appendChild(menu_type)
// 		menu_type.appendChild(lunch_items)
// 	});
// }
loadJSON = function() {
	var iterations = 0;
	obj.forEach(function(element) {
		iterations += 1;
		const menu_type_default = document.getElementById("menu_type#" + iterations); menu_type_default.remove();
		var card = document.getElementById("card#" + iterations);
		// console.log(card);
		// console.log(iterations);

		const menu_type = document.createElement("p");
		menu_type.setAttribute("class", "card-text");
		// menu_type.setAttribute("id", "card-text")

		const lunch_items = document.createElement("i");
		lunch_items.setAttribute("class", "smalltext");

		var children = menu_type.children.length + 1
		menu_type.appendChild(document.createTextNode(String(element.menu_type).replaceAll(" - SANB Secondary School", "")));
		const line_break = document.createElement("br");
		menu_type.appendChild(line_break);
		lunch_items.appendChild(document.createTextNode(String(element.lunch_items).replaceAll(",", ", ")));
		card.appendChild(menu_type);
		menu_type.appendChild(lunch_items);

	});
}

var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0');
var yyyy = today.getFullYear();

today = "https://SAVHS.GA/Lunch/Logs/LD_" + yyyy + "-" + mm + '-' + dd + ".json";
current_lunch_link =
