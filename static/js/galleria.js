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
