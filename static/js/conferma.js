function selezionaAdulto(id) {
	const cls = `solo-bambino-${id}`;
	let elements = document.getElementsByClassName(cls);
	for (let e of elements) {
		console.log(e);
		e.hidden = true;
	}
}

function selezionaBambino(id) {
	const cls = `solo-bambino-${id}`;
	let elements = document.getElementsByClassName(cls);
	for (let e of elements) {
		console.log(e);
		e.hidden = false;
	}
}

function pressed() {
	const a = document.getElementById("file-selector");
	const fileLabel = document.getElementById("file-selector-label");
	if (a.value == "") {
		fileLabel.innerHTML = "Choose file";
	} else {
		var theSplit = a.value.split("\\");
		fileLabel.innerHTML = theSplit[theSplit.length - 1];
	}
}
