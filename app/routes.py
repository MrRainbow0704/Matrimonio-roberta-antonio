from flask import (
    render_template,
    redirect,
    url_for,
    session,
    request,
    Response,
    flash,
    send_from_directory,
)
from sqlalchemy import select, update
import json
import os
import secrets
from werkzeug.utils import secure_filename
from . import tools, app


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
    def fetch_invitati() -> list[dict[str, int | str]]:
        with tools.session.begin() as s:
            stmt = select(tools.Invitato).order_by(tools.Invitato.partecipa, tools.Invitato.famiglia)
            invitati = s.scalars(stmt).all()

        # Fai apparire nella lista `i["Allergie"]` solo le allergie presenti.
        for i in invitati:
            i.allergie = [k for k, v in json.loads(i.allergie).items() if v == 1]
            i.partecipa = "Si" if i.partecipa else "No"
            i.famiglia = tools.get_family_from_id(i.famiglia).nome
        return invitati

    def fetch_famiglie() -> list[dict[str, int | str]]:
        with tools.session.begin() as s:
            stmt = select(tools.Famiglia).order_by(tools.Famiglia.nome)
            famiglie = s.scalars(stmt).all()
        return famiglie

    def allowed_file(file: str) -> bool:
        estensioni = (".jpg", ".jpeg", ".jfif", ".pjpeg", ".pjp", ".png")
        return file.lower().endswith(estensioni)

    def fetch_foto() -> list[str]:
        foto = []
        for file in os.listdir(app.config["UPLOAD_FOLDER"]):
            if allowed_file(file):
                url = url_for("uploads", filename=file)
                owner_id = file.split("-")[0]
                owner = tools.get_user_from_id(owner_id)
                famiglia = tools.get_family_from_id(owner.famiglia)
                user = {
                    "nome": f'{owner.nome.capitalize()} {owner.cognome.capitalize()}',
                    "famiglia": famiglia.nome,
                }
                file_size = os.path.getsize(os.path.join(app.config["UPLOAD_FOLDER"], file))
                size = round(file_size / 1024, 2)
                foto.append({"url": url, "user": user, "size": size})
        return foto

    if request.method == "POST":
        if request.form.get("csrf") != session.get("csrf"):
            invitati = fetch_invitati()
            famiglie = fetch_famiglie()
            foto = fetch_foto()
            flash("La richiesta non contiene il CSRF token.", "errore")
            return (
                render_template(
                    "admin.html",
                    invitati=invitati,
                    famiglie=famiglie,
                    foto=foto,
                ),
                403,
            )
        if request.form.get("aggiungi-invitato"):
            nome = request.form.get("nome").lower().strip()
            cognome = request.form.get("cognome").lower().strip()
            famiglia = request.form.get("famiglia").lower().strip()
            if tools.empty_input(nome, cognome, famiglia):
                invitati = fetch_invitati()
                famiglie = fetch_famiglie()
                foto = fetch_foto()
                flash("Assicurati di aver riempito tutti i campi.", "errore")
                return (
                    render_template(
                        "admin.html",
                        invitati=invitati,
                        famiglie=famiglie,
                        foto=foto,
                    ),
                    400,
                )

            if tools.create_user(nome, cognome, famiglia):
                invitati = fetch_invitati()
                famiglie = fetch_famiglie()
                foto = fetch_foto()
                flash("Utente creato con successo.", "ok")
                return (
                    render_template(
                        "admin.html",
                        invitati=invitati,
                        famiglie=famiglie,
                        foto=foto,
                    ),
                    200,
                )

            invitati = fetch_invitati()
            famiglie = fetch_famiglie()
            foto = fetch_foto()
            flash("C'è stato un errore imprevisto.", "errore")
            return (
                render_template(
                    "admin.html",
                    invitati=invitati,
                    famiglie=famiglie,
                    foto=foto,
                ),
                500,
            )
        elif request.form.get("aggiungi-famiglia"):
            nome = request.form.get("nome").lower().strip()
            if tools.empty_input(nome):
                invitati = fetch_invitati()
                famiglie = fetch_famiglie()
                foto = fetch_foto()
                flash("Assicurati di aver riempito tutti i campi.", "errore")
                return (
                    render_template(
                        "admin.html",
                        invitati=invitati,
                        famiglie=famiglie,
                        oto=foto,
                    ),
                    400,
                )

            if tools.create_family(nome):
                invitati = fetch_invitati()
                famiglie = fetch_famiglie()
                foto = fetch_foto()
                flash("Famiglia creata con successo.", "ok")
                return (
                    render_template(
                        "admin.html",
                        invitati=invitati,
                        famiglie=famiglie,
                        foto=foto,
                    ),
                    200,
                )

            invitati = fetch_invitati()
            famiglie = fetch_famiglie()
            foto = fetch_foto()
            flash("C'è stato un errore imprevisto.", "errore")
            return (
                render_template(
                    "admin.html",
                    invitati=invitati,
                    famiglie=famiglie,
                    foto=foto,
                ),
                500,
            )
        elif request.form.get("rimuovi-invitato"):
            invitato = int(request.form.get("invitato"))
            if tools.empty_input(invitato):
                invitati = fetch_invitati()
                famiglie = fetch_famiglie()
                foto = fetch_foto()
                flash("Assicurati di aver riempito tutti i campi.", "errore")
                return (
                    render_template(
                        "admin.html",
                        invitati=invitati,
                        famiglie=famiglie,
                        foto=foto,
                    ),
                    400,
                )

            if tools.delete_user(invitato):
                invitati = fetch_invitati()
                famiglie = fetch_famiglie()
                foto = fetch_foto()
                flash("Utente rimosso con successo.", "ok")
                return (
                    render_template(
                        "admin.html",
                        invitati=invitati,
                        famiglie=famiglie,
                        foto=foto,
                    ),
                    200,
                )

            invitati = fetch_invitati()
            famiglie = fetch_famiglie()
            foto = fetch_foto()
            flash("C'è stato un errore imprevisto.", "errore")
            return (
                render_template(
                    "admin.html",
                    invitati=invitati,
                    famiglie=famiglie,
                    foto=foto,
                ),
                500,
            )
        elif request.form.get("rimuovi-famiglia"):
            famiglia = int(request.form.get("famiglia"))
            if tools.empty_input(famiglia):
                invitati = fetch_invitati()
                famiglie = fetch_famiglie()
                foto = fetch_foto()
                flash("Assicurati di aver riempito tutti i campi.", "errore")
                return (
                    render_template(
                        "admin.html",
                        invitati=invitati,
                        famiglie=famiglie,
                        foto=foto,
                    ),
                    400,
                )

            if tools.delete_family(famiglia):
                invitati = fetch_invitati()
                famiglie = fetch_famiglie()
                foto = fetch_foto()
                flash("Famiglia rimossa con successo.", "ok")
                return (
                    render_template(
                        "admin.html",
                        invitati=invitati,
                        famiglie=famiglie,
                        foto=foto,
                    ),
                    200,
                )

            invitati = fetch_invitati()
            famiglie = fetch_famiglie()
            foto = fetch_foto()
            flash("C'è stato un errore imprevisto.", "errore")
            return (
                render_template(
                    "admin.html",
                    invitati=invitati,
                    famiglie=famiglie,
                    foto=foto,
                ),
                500,
            )
        elif request.form.get("rimuovi-foto"):
            foto = secure_filename(request.form.get("foto"))
            if not allowed_file(foto):
                invitati = fetch_invitati()
                famiglie = fetch_famiglie()
                foto = fetch_foto()
                flash("Something went wrong", "errore")
                return (
                    render_template(
                        "admin.html", invitati=invitati, famiglie=famiglie, foto=foto
                    ),
                    400,
                )

            filepath = os.path.join(app.config["UPLOAD_FOLDER"], foto)
            if not os.path.isfile(filepath):
                invitati = fetch_invitati()
                famiglie = fetch_famiglie()
                foto = fetch_foto()
                flash("Questa foto non esiste.", "errore")
                return (
                    render_template(
                        "admin.html", invitati=invitati, famiglie=famiglie, foto=foto
                    ),
                    400,
                )

            os.remove(filepath)
            invitati = fetch_invitati()
            famiglie = fetch_famiglie()
            foto = fetch_foto()
            flash("Foto eliminata con successo.", "ok")
            return (
                render_template(
                    "admin.html", invitati=invitati, famiglie=famiglie, foto=foto
                ),
                200,
            )

        else:
            invitati = fetch_invitati()
            famiglie = fetch_famiglie()
            foto = fetch_foto()
            flash("Questa richiesta non è valida.", "errore")
            return (
                render_template(
                    "admin.html", invitati=invitati, famiglie=famiglie, foto=foto
                ),
                400,
            )
    else:
        invitati = fetch_invitati()
        famiglie = fetch_famiglie()
        foto = fetch_foto()
        return (
            render_template(
                "admin.html", invitati=invitati, famiglie=famiglie, foto=foto
            ),
            200,
        )


@app.route("/conferma", methods=["GET", "POST"])
def conferma() -> Response:
    def fetch_membri() -> list[tools.Invitato]:
        membri = tools.get_family_members(session["Famiglia"])
        for m in membri:
            m.allergie = [k for k, v in json.loads(m.allergie).items() if v == 1]
        return membri

    if tools.is_logged_in():
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
                    tipo == "bambino" and età is None
                ):
                    membri = fetch_membri()
                    flash("Assicurati di aver riempito tutti i campi.", "errore")
                    return render_template("conferma.html", famiglia=membri), 400
                with tools.session.begin() as s:
                    stmt = update(tools.Invitato).values(
                        tipo=tipo,
                        allergie=json.dumps(allergie),
                        partecipa=int(partecipa),
                        età=età,
                    ).where(tools.Invitato.id == membro)
                    res = s.execute(stmt)
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
                if tools.create_user(nome, cognome, famiglia):
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
        flash("Devi eseguire il login per vedere questa pagina.", "errore")
        return redirect(url_for("accedi"))


@app.route("/accedi", methods=["GET", "POST"])
def accedi() -> Response:
    if tools.is_logged_in():
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

        if tools.login_user(nome, cognome):
            flash("Login eseguito con successo.", "ok")
            return redirect(url_for("conferma"))

        flash("Questa persona non è sulla lista degli invitati.", "errore")
        return render_template("accedi.html"), 403
    else:
        return render_template("accedi.html"), 200


@app.route("/galleria", methods=["GET", "POST"])
def galleria() -> Response:
    def allowed_file(file: str) -> bool:
        estensioni = (".jpg", ".jpeg", ".jfif", ".pjpeg", ".pjp", ".png")
        return file.lower().endswith(estensioni)

    def fetch_foto() -> list[str]:
        foto = []
        for file in os.listdir(app.config["UPLOAD_FOLDER"]):
            if allowed_file(file):
                foto.append(url_for("uploads", filename=file))
        return foto

    if request.method == "POST":
        if not tools.is_logged_in():
            flash("Devi aver eseguito il login per caricare delle immagini.", "errore")
            return redirect(url_for("accedi"))

        if request.form.get("csrf") != session.get("csrf"):
            flash("La richiesta non contiene il CSRF token.", "errore")
            return render_template("accedi.html"), 403

        if "file" not in request.files or request.files["file"].filename == "":
            flash("Non hai selezionato un'immagine.", "errore")
            return redirect(url_for("galleria"))

        if not allowed_file(request.files["file"].filename):
            flash("Questa estensione non è supportata.", "errore")
            return redirect(url_for("galleria"))

        file = request.files["file"]
        ext = request.files["file"].filename.rsplit(".")[-1]
        filename = f'{session["Id"]}-{secrets.token_hex(8)}.{ext}'
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        flash("Immagine caricata con successo.", "ok")
        return render_template("galleria.html", foto=fetch_foto()), 200

    return render_template("galleria.html", foto=fetch_foto()), 200


@app.route("/uploads/<string:filename>")
def uploads(filename: str):
    filename = secure_filename(filename)
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/logout")
def logout() -> Response:
    flash("Logout effettuato con successo.", "ok")
    session.clear()
    return redirect(url_for("accedi"))
