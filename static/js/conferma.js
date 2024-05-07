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

function send(data) {
	const csrfToken = document.getElementById("csrf").innerText
	const args = { csrf: csrfToken, membro: 1, data: data };
	return fetch("/conferma", {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify(args),
	});
}

function submit(e) {
	const forms = document.getElementsByClassName("user-form");
	data = [];
	for (let i = 0; i < forms.length; i++) {
		const formId = forms[i].id;
		const id = formId.split("-")[1];

		let nome = document.querySelector(`#membro-${id}>h3`).innerText;

		let partecipa = document.querySelector(
			`#${formId} input[name="partecipa"]:checked`
		);
		if (partecipa !== null) {
			partecipa = partecipa.value;
		}

		let tipo = document.querySelector(
			`#${formId} input[name="tipo"]:checked`
		);
		if (tipo !== null) {
			tipo = tipo.value;
		}

		let età = document.querySelector(
			`#${formId} input[name="età"]:checked`
		);
		if (età !== null) {
			età = età.value;
		}

		let allergie = [];
		const allergeni = [
			"anidride-solforosa",
			"arachidi",
			"crostacei",
			"frutta-a-guscio",
			"glutine",
			"latte",
			"lupini",
			"molluschi",
			"pesce",
			"sedano",
			"senape",
			"sesamo",
			"soia",
			"uova",
		];
		for (let j = 0; j < allergeni.length; j++) {
			const allergia = allergeni[j];
			a = document.querySelector(
				`#${formId} input[name="allergie-${allergia}"]:checked`
			);
			if (a != null) {
				allergie.push(allergia);
			}
		}

		data.push({
			id: id,
			nome: nome,
			tipo: tipo,
			partecipa: partecipa,
			età: età,
			allergie: allergie,
		});
	}
	send(data)
		.then((r) => r.text())
		.then((t) => {
			document.getElementsByTagName("html")[0].innerHTML = t;
		});
}
