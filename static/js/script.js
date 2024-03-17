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
