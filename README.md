# Matrimonio Roberta e Antonio

Questa repository contiene i file sorgente del sito creato da me (Marco Simone) per il matrimonio dei miei genitori (Roberta e Antonio).

Il backend del sito è scritto in Python usando la libreria `Flask` che abilita l'utilizzo del template engine `Jinja` per generare dinamicamente i file HTML.

Il frontend del sito è scritto con una combinazione di CSS3 e JavaScript vanilla e [Bootstrap 5.3](https://getbootstrap.com).

Per comunicare con il database il sito usa la libreria `mysql.connector` per Python e quindi richiede l'utilizzo di un database MySQL o MariaDB.

Per funzionare correttamente, il sito richiede 
la configurazione di un file `.env` seguendo la falsariga del file `.env.template` contenuto nella repo oltre all'installazione dei moduli per Python elencati in `requirements.txt`, installabili con il semplice comando: 
```sh
pip install -r requirements.txt
```

Il codice è formattato utilizzando il formatter [Black](https://github.com/psf/black)