from flask import render_template, redirect, url_for, session, request, Response, flash
import json
from . import tools, app, DB


@app.route("/")
def home() -> Response:
    return render_template("home.html"), 200


@app.route("/contatti")
def contatti() -> Response:
    return render_template("contatti.html"), 200


@app.route("/programma")
def programma() -> Response:
    return render_template("programma.html"), 200


@app.route("/location")
def location() -> Response:
    return render_template("location.html"), 200


@app.route("/lista_nozze")
def lista_nozze() -> Response:
    return render_template("lista_nozze.html"), 200


@app.route("/admin", methods=["GET", "POST"])
@tools.requires_auth
def admin() -> Response:
    def fetch_invitati_famiglie() -> tuple[list[dict[str, int | str]]]:
        with tools.DBHandler(**DB) as dbh:
            invitati = dbh.query("SELECT * FROM Invitati;")
            famiglie = dbh.query("SELECT * FROM Famiglie;")

            # Fai apparire nella lista `i["Allergie"]` solo le allergie presenti.
            for i in invitati:
                i["Allergie"] = [
                    k for k, v in json.loads(i["Allergie"]).items() if v == 1
                ]
                i["Partecipa"] = "Si" if i["Partecipa"] else "No"
                i["Famiglia"] = tools.get_family_from_id(DB, i["Famiglia"])["Nome"]
        return (invitati, famiglie)

    if request.method == "POST":
        if request.form.get("csrf") != session.get("csrf"):
            invitati, famiglie = fetch_invitati_famiglie()
            flash("La richiesta non contiene il CSRF token.", "errore")
            return (
                render_template(
                    "admin.html",
                    invitati=invitati,
                    famiglie=famiglie,
                ),
                403,
            )
        if request.form.get("aggiungi-invitato"):
            nome = request.form.get("nome").lower().strip()
            cognome = request.form.get("cognome").lower().strip()
            famiglia = request.form.get("famiglia").lower().strip()
            if tools.empty_input(nome, cognome, famiglia):
                invitati, famiglie = fetch_invitati_famiglie()
                flash("Assicurati di aver riempito tutti i campi.", "errore")
                return (
                    render_template(
                        "admin.html",
                        invitati=invitati,
                        famiglie=famiglie,
                    ),
                    400,
                )

            if tools.create_user(DB, nome, cognome, famiglia):
                invitati, famiglie = fetch_invitati_famiglie()
                flash("Utente creato con successo.", "ok")
                return (
                    render_template(
                        "admin.html",
                        invitati=invitati,
                        famiglie=famiglie,
                    ),
                    200,
                )

            invitati, famiglie = fetch_invitati_famiglie()
            flash("C'è stato un errore imprevisto.", "errore")
            return (
                render_template(
                    "admin.html",
                    invitati=invitati,
                    famiglie=famiglie,
                ),
                500,
            )
        elif request.form.get("rimuovi-invitato"):
            invitato = int(request.form.get("invitato"))
            if tools.empty_input(invitato):
                invitati, famiglie = fetch_invitati_famiglie()
                flash("Assicurati di aver riempito tutti i campi.", "errore")
                return (
                    render_template(
                        "admin.html",
                        invitati=invitati,
                        famiglie=famiglie,
                    ),
                    400,
                )

            if tools.delete_user(DB, invitato):
                invitati, famiglie = fetch_invitati_famiglie()
                flash("Utente rimosso con successo.", "ok")
                return (
                    render_template(
                        "admin.html",
                        invitati=invitati,
                        famiglie=famiglie,
                    ),
                    200,
                )

            invitati, famiglie = fetch_invitati_famiglie()
            flash("C'è stato un errore imprevisto.", "errore")
            return (
                render_template(
                    "admin.html",
                    errore="C'è stato un errore imprevisto.",
                    invitati=invitati,
                    famiglie=famiglie,
                ),
                500,
            )
        elif request.form.get("aggiungi-famiglia"):
            nome = request.form.get("nome").lower().strip()
            if tools.empty_input(nome):
                invitati, famiglie = fetch_invitati_famiglie()
                flash("Assicurati di aver riempito tutti i campi.", "errore")
                return (
                    render_template(
                        "admin.html",
                        invitati=invitati,
                        famiglie=famiglie,
                    ),
                    400,
                )

            if tools.create_family(DB, nome):
                invitati, famiglie = fetch_invitati_famiglie()
                flash("Famiglia creata con successo.", "ok")
                return (
                    render_template(
                        "admin.html",
                        invitati=invitati,
                        famiglie=famiglie,
                    ),
                    200,
                )

            invitati, famiglie = fetch_invitati_famiglie()
            flash("C'è stato un errore imprevisto.", "errore")
            return (
                render_template(
                    "admin.html",
                    invitati=invitati,
                    famiglie=famiglie,
                ),
                500,
            )
        elif request.form.get("rimuovi-famiglia"):
            famiglia = int(request.form.get("famiglia"))
            if tools.empty_input(famiglia):
                invitati, famiglie = fetch_invitati_famiglie()
                flash("Assicurati di aver riempito tutti i campi.", "errore")
                return (
                    render_template(
                        "admin.html",
                        invitati=invitati,
                        famiglie=famiglie,
                    ),
                    400,
                )

            if tools.delete_family(DB, famiglia):
                invitati, famiglie = fetch_invitati_famiglie()
                flash("Famiglia rimossa con successo.", "ok")
                return (
                    render_template(
                        "admin.html",
                        invitati=invitati,
                        famiglie=famiglie,
                    ),
                    200,
                )

            invitati, famiglie = fetch_invitati_famiglie()
            flash("C'è stato un errore imprevisto.", "errore")
            return (
                render_template(
                    "admin.html",
                    invitati=invitati,
                    famiglie=famiglie,
                ),
                500,
            )
        else:
            invitati, famiglie = fetch_invitati_famiglie()
            flash("Questa richiesta non è valida.", "errore")
            return (
                render_template("admin.html", invitati=invitati, famiglie=famiglie),
                400,
            )
    else:
        invitati, famiglie = fetch_invitati_famiglie()
        return render_template("admin.html", invitati=invitati, famiglie=famiglie), 200


@app.route("/conferma", methods=["GET", "POST"])
def conferma() -> Response:
    def fetch_membri() -> list[dict[str, int | str]]:
        membri = tools.get_family_members(DB, session["Famiglia"])
        for m in membri:
            m["Allergie"] = [k for k, v in json.loads(m["Allergie"]).items() if v == 1]
        return membri

    if tools.is_logged_in(DB):
        if request.method == "POST":
            if request.form.get("csrf") != session.get("csrf"):
                membri = fetch_membri()
                flash("La richiesta non contiene il CSRF token.", "errore")
                return render_template("conferma.html", famiglia=membri), 403

            if request.form.get("membro"):
                membro = request.form.get("membro")
                tipo = request.form.get("tipo")
                partecipa = request.form.get("partecipa")
                if tipo == "bambino":
                    età = request.form.get("età")
                else:
                    età = None
                allergeni = [
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
                ]

                allergie = {
                    a: (1 if request.form.get(f"allergie-{a}") else 0)
                    for a in allergeni
                }
                if tools.empty_input(membro, tipo, partecipa, allergie) or (
                    tipo == "bambino" and età == None
                ):
                    membri = fetch_membri()
                    flash("Assicurati di aver riempito tutti i campi.", "errore")
                    return render_template("conferma.html", famiglia=membri), 400
                with tools.DBHandler(**DB) as dbh:
                    res = dbh.query(
                        "UPDATE Invitati SET Tipo=%s, Allergie=%s, Partecipa=%s, Età=%s WHERE Id=%s;",
                        (tipo, json.dumps(allergie), partecipa, età, membro),
                    )
                if res != False:
                    membri = fetch_membri()
                    flash("Membro aggiornato con successo.", "ok")
                    return render_template("conferma.html", famiglia=membri), 200

                membri = fetch_membri()
                flash("C'è stato un errore imprevisto.", "errore")
                return render_template("conferma.html", famiglia=membri), 500

            elif request.form.get("nuovo"):
                nome = request.form.get("nome").lower().strip()
                cognome = request.form.get("cognome").lower().strip()
                if tools.empty_input(nome, cognome):
                    membri = fetch_membri()
                    flash("Assicurati di aver riempito tutti i campi.", "errore")
                    return render_template("conferma.html", famiglia=membri), 400

                famiglia = session["Famiglia"]
                if tools.create_user(DB, nome, cognome, famiglia):
                    membri = fetch_membri()
                    flash("Membro aggiunto con successo.", "ok")
                    return render_template("conferma.html", famiglia=membri), 200

                membri = fetch_membri()
                flash("C'è stato un errore imprevisto.", "errore")
                return render_template("conferma.html", famiglia=membri), 200

            membri = fetch_membri()
            flash("Questa richiesta non è valida.", "errore")
            return render_template("conferma.html", famiglia=membri), 400
        else:
            membri = fetch_membri()
            return render_template("conferma.html", famiglia=membri), 200
    else:
        return redirect(url_for("accedi"))


@app.route("/accedi", methods=["GET", "POST"])
def accedi() -> Response:
    if tools.is_logged_in(DB):
        return redirect(url_for("home"))

    if request.method == "POST":
        if request.form.get("csrf") != session.get("csrf"):
            flash("La richiesta non contiene il CSRF token.", "errore")
            return render_template("accedi.html"), 403

        nome = request.form.get("nome").lower().strip()
        cognome = request.form.get("cognome").lower().strip()
        if tools.empty_input(nome, cognome):
            flash("Assicurati di aver riempito tutti i campi.", "errore")
            return render_template("accedi.html"), 400

        if tools.login_user(DB, nome, cognome):
            flash("Login eseguito con successo.", "ok")
            return redirect(url_for("conferma"))

        flash("Questa persona non è sulla lista degli invitati.", "errore")
        return render_template("accedi.html"), 500
    else:
        return render_template("accedi.html"), 200


@app.route("/logout")
def logout() -> Response:
    flash("Logout effettuato con successo.", "ok")
    session.clear()
    return redirect(url_for("accedi"))
