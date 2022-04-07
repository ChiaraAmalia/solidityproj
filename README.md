# :leaves: Foot Print Calculator :leaves:

Il nostro progetto consente di tenere traccia del footprint di un prodotto a partire dalla materia prima del quale e composto e considerando la lavorazione necessaria alla sua produzione.

 ## Indice
 1. [Come installare il programma;](#come-installare-il-programma)
 2. [Come utilizzare il programma;](#uso)

## Come installare il programma

### Prerequisiti

- node.js
- Docker
- python


### NodeJS
Per prima cosa bisogna eseguire il download di NodeJS, cliccando sul seguente link:[Download NodeJS](https://nodejs.org/it/) e seguire poi le istruzioni dell'installer.


### Docker

Il nostro **foot print calculator** è davvero facile da installare ed utilizzare. Sfrutta docker per la gestione in locale dei nodi della blockchain.

Come prima cosa bisogna installare docker per fare ciò basta seguire le indicazioni riportate nel seguente link: [Come installare docker](https://docs.docker.com/desktop/windows/install/)  



### Python
Il programma per funzionare necessita di python, per istallarlo, seguire le istruzioni riportate nel seguente link: [download and install python](https://www.python.org/downloads/)

### Creazione ambiente virtuale con dipendenze metodo 1
```sh
python venv <nome_ambiente>
cd <nome_ambiente>/Scripts/activate
activate
cd../../
pip install -r requirements.txt
```

### Creazione ambiente virtuale con dipendenze se hai Anaconda3
```sh
python -m venv <nome_ambiente>
cd <nome_ambiente>/Scripts/
activate
cd../../
pip install -r requirements.txt
```
Se usi terminale di vscode riavvia il terminale dopo l'esecuzione di activate

### Far partire la BlockChain
Nella cartella scaricata da GitHub aprire il prompt ed eseguire i seguenti comandi, per creare la BlockChain:
```sh
cd 3-nodes-footprintBlockchain
docker compose up
 ```
 
<p align="center">
  <img width="1020" src="https://github.com/Accout-Personal/solidityproj/blob/master/img/gif_docker.gif">
</p>
 
In seguito si può chiudere il terminale, riaprirlo, ed attivare la BlockChain con i comandi:
```sh
cd 3-nodes-footprintBlockchain
start.cmd
 ```

### Eseguire il programma
```sh
python path/to/file/init_prod.py 
```
### Se hai Anaconda 3
occore passare nel directory del file prima di eseguirlo
```sh
cd path/to/file/
python init_prod.py 
```

<p align="center">
  <img width="1020" src="https://github.com/Accout-Personal/solidityproj/blob/master/img/gif_app.gif">
</p>

```sh
python path/to/file/main.py 
```
<p align="center">
  <img width="1020" src="https://github.com/Accout-Personal/solidityproj/blob/master/img/gif_main.gif">
</p>

<!--### Quorum-wizard

Per installare quorum-wizard basterà aprire il terminale di windows ed eseguire i seguenti comandi:

```sh
npx quorum-wizard 
```
E seguire le indicazioni, e quando viene richiesto di scegliere tra docker-compose e Kubernetes, scegliere **docker-compose**.

```sh
cd networks/<nome_network>/
start.cmd
```-->

## Uso

All'avvio del programma viene mostrata una schermata di login. In questa si può scegliere tra i 3 account quello di interesse. Tra le parentesi è scritto il ruolo che tale account ha.
<p align="center">
  <img width="700" src="https://github.com/Accout-Personal/solidityproj/blob/master/img/login.jpg">
</p>
Ogni account ha un solo ruolo per garantire la separazione dei privilegi.
I ruoli sono 3:

 1. **Consumatore**
 2. **Trasformatore** (trasforma la materia prima in prodotto finito)
 3. **Produttore** (produce la materia prima)
 

Dopo aver selezionato l'account con cui procedere, le operazioni possibili saranno differenti.

- Il produttore potrà:
  - [Aggiungere una materia prima](#aggiungi-materia-prima)
 
 <p align="center">
  <img src="https://github.com/Accout-Personal/solidityproj/blob/master/img/produttore.jpg">
</p>

 - Il trasformatore potrà:
	 - [Vedere lotti materie prime](#vedere-lotti-materie-prime)
	 - [Vedere lotti materia per nome](#vedere-lotti-materia-per-nome)
	 - [Vedere informazioni di una materia per nome](#vedere-informazioni-materia-prima)
	 - [Acquistare una materia prima](#acquistare-materie-prime)
	 - [Vedere dettagli materia acquistata](#vedere-dettagli-materia-acquistata)
	 - [Aggiungere prodotto finito](#aggiungere-prodotto-finito)

<p align="center">
  <img src="https://github.com/Accout-Personal/solidityproj/blob/master/img/trasformatore.jpg">
</p>

 - Il consumatore potrà:
 	- [Vedere i lotti dei prodotti](#vedere-lotti-prodotti)
	 - [Vedere lotti prodotto per nome](#vedere-lotti-prodotto-per-nome)
	 - [Vedere footprint di un prodotto](#vedere-footprint-prodotto)
	 - [Vedere informazioni di una materia per nome](#vedere-informazioni-prodotto)
	 - [Acquistare un prodotto](#acquistare-prodotti)
	 - [Vedere dettagli prodotto acquistato](#vedere-dettagli-prodotto-acquistato)

<p align="center">
  <img src="https://github.com/Accout-Personal/solidityproj/blob/master/img/consumatore.jpg">
</p>


### Aggiungi materia prima

Scegliendo questa opzione, apparirà un'interfaccia nella quale si dovrà inserire:
- nome della materia prima;
- quantità (numero, maggiore di 0);
- footprint (numero, maggiore di 0).

L'inserimento di una nuova materia prima potrà essere effettuato solo dal produttore altrimenti non sarà consentito l'inserimento e si riceverà il seguente messaggio di errore: 
> "solo il produttore puo' produrre la materia prima."

La quantita della materia prima ed il suo footprint devono essere maggiori di 0, altrimenti si riceverà il seguente messaggio di errore:
> "la quantita'/il footprint deve essere maggiore di 0."

### Vedere lotti materie prime

Scegliendo questa opzione, apparirà una finestra contenente tutti i lotti delle materie prime disponibili.

Visionare tutti i lotti delle materie prime è possibili solo per il trasformatore altrimenti, se colui che ne richiede la visione non è il traformatore questa non sarà consentita e si riceverà il seguente messaggio di errore: 
> "solo il trasformatore puo' vedere tutti i lotti delle materie prime inserite dal produttore."

Se non ci sono materie prime nel magazzino del produttore, verrà segnalato il seguente errore:
> "Non sono presenti materie prime"

### Vedere lotti materia per nome

Scegliendo questa opzione, apparirà una finestra contenente tutti i lotti della materia prima della quale dovrà inserire il nome.

Visionare tutti i lotti delle materie prime è possibile solo per il trasformatore altrimenti, se colui che ne richiede la visione non è il traformatore questa non sarà consentita e si riceverà il seguente messaggio di errore: 
> "solo il trasformatore puo' vedere tutti i lotti associati ad una materia prima"

### Vedere informazioni materia prima

Scegliendo questa opzione, il trasformatore potrà avere tutte le informazioni di una materia prima, presente nel magazzino del venditore, della quale dovrà inserire il lotto.

Visionare le informazioni di una materia prima è possibile solo per il trasformatore altrimenti, se colui che ne richiede la visione non è il traformatore questa non sarà consentita e si riceverà il seguente messaggio di errore: 
> "solo il trasformatore puo' vedere le informazioni relative ad un lotto di una materia prima inserito dal produttore."

Se si inserisce un lotto che non esiste, si riceve il seguente messaggio:
> "il lotto inserito e' inesistente."

### Acquistare materie prime

Scegliendo questa opzione, apparirà una finestra contenente tutte le materie prime disponibili (con le relative informazioni) nella quale si dovrà inserire:
- la quantità da acquistare.

L'acquisto di una materia prima potrà essere effettuato solo dal trasformatore altrimenti non sarà consentito e si riceverà il seguente messaggio di errore: 
> "solo il trasformatore puo' aquistare la materia prima."

La quantita della materia prima da acquistare deve essere maggiore di 0, altrimenti si riceverà il seguente messaggio di errore:
> "la quantita' deve essere maggiore di 0."

La materia prima da acquistare deve esistere (essere presente nel magazzino del produttore), altrimenti si riceverà il seguente messaggio di errore:
> "la materia prima e' inesistente"

La quantità di materia prima da acquistare deve essere minore di quella presente in magazzino, altrimenti si riceverà il seguente messaggio di errore:
> "scorta non sufficente."

### Vedere dettagli materia acquistata

Scegliendo questa opzione, il trasformatore potrà avere tutte le informazioni di una materia prima, che ha acquistato, della quale dovrà inserire il lotto.

Visionare le informazioni di una materia prima è possibile solo per il trasformatore altrimenti, se colui che ne richiede la visione non è il traformatore questa non sarà consentita e si riceverà il seguente messaggio di errore: 
> "solo il trasformatore puo' vedere le informazioni relative ad un lotto di una materia prima acquistato dal trasformatore."

Se si inserisce un lotto che non esiste, si riceve il seguente messaggio:
> "il lotto inserito e' inesistente."

### Aggiungere prodotto finito

Scegliendo questa opzione, apparirà un'interfaccia nella quale si dovrà inserire:
- nome della prodotto;
- lotti delle materie prime utilizzate (divisi da una virgola);
- quantità utilizzata di ogni materia prima (divisi da virgola);
- quantità di prodotto finito realizzata;
- footprint della produzione del prodotto finito.

L'inserimento di un prodotto finito potrà essere effettuato solo dal trasformatore altrimenti non sarà consentito l'inserimento e si riceverà il seguente messaggio di errore: 
> "solo il trasformatore puo' aggiungere un prodotto."

La quantita del prodotto ed il suo footprint devono essere maggiori di 0, altrimenti si riceverà il seguente messaggio di errore:
> "la quantita' prodotta deve essere un valore positivo e diverso da zero."
> "il footprint del prodotto deve essere un valore positivo e diverso da zero."

Le materie prime che si utilizzano per la produzione di un prodotto devono essere presenti nel magazzino del produttore, e in quantità adeguata, altrimenti l'inserimento non sarà effettuato e si riceverà uno dei seguenti messaggi di errore:
> "il lotto _nomelotto_  e' inesistente"
> "la quantita' nel magazzino per il lotto _nomelotto_ non e' sufficiente"

### Vedere lotti prodotti

Scegliendo questa opzione, apparirà una finestra contenente tutti i lotti dei prodotti disponibili.

Visionare tutti i lotti dei prodotti è possibile solo per il consumatore altrimenti, se colui che ne richiede la visione non è il consumatore questa non sarà consentita e si riceverà il seguente messaggio di errore: 
> "solo il consumatore puo' vedere tutti i lotti dei prodotti inseriti dal trasformatore."

Se non ci sono prodotti nel magazzino del trasformatore, verrà segnalato il seguente errore:
> "Non sono presenti prodotti"

### Vedere lotti prodotto per nome

Scegliendo questa opzione, apparirà una finestra contenente tutti i lotti del prodotto del quale si dovrà inserire il nome.

Visionare tutti i lotti dei prodotti è possibile solo per il trasformatore altrimenti, se colui che ne richiede la visione non è il traformatore questa non sarà consentita e si riceverà il seguente messaggio di errore: 
> "solo il consumatore puo' vedere tutti i lotti associati ad un prodotto."

### Vedere footprint prodotto

Scegliendo questa opzione, apparirà una finestra per l'inserimento del lotto del quale si vuole conoscere il footprint, una volta inserito si potrà visionare il footprint.

Visionare il footprint di un prodotto è possibile solo per il consumatore altrimenti, se colui che ne richiede la visione non è il consumatore questa non sarà consentita e si riceverà il seguente messaggio di errore: 
> "solo il consumatore puo' vedere il footprint del prodotto finito."

Se il lotto non fosse presente nel magazzino del trasformatore si riceverà il seguente messaggio:
> "Tale lotto non e' presente in magazzino"

### Vedere informazioni prodotto

Scegliendo questa opzione, il consumatore potrà avere tutte le informazioni di un prodotto, presente nel magazzino del trasformatore, del quale dovrà inserire il lotto.

Visionare le informazioni di unprodotto è possibile solo per il consumatore altrimenti, se colui che ne richiede la visione non è il consumatore questa non sarà consentita e si riceverà il seguente messaggio di errore: 
> "solo il consumatore puo' vedere le informazioni relative ad un lotto di un prodotto inserito dal trasformatore."

Se si inserisce un lotto che non esiste, si riceve il seguente messaggio:
> "il lotto inserito e' inesistente."

### Acquistare prodotti

Scegliendo questa opzione, apparirà una finestra contenente tutti i prodotti disponibili (con le relative informazioni) nella quale si dovrà inserire:
- la quantità da acquistare.

L'acquisto di una prodotto prima potrà essere effettuato solo dal consumatore altrimenti non sarà consentito e si riceverà il seguente messaggio di errore: 
> "solo il consumatore puo' acquistare un prodotto."

La quantita del prodotto da acquistare deve essere maggiore di 0, altrimenti si riceverà il seguente messaggio di errore:
> "la quantita' acquistata deve essere un valore positivo diverso da zero."

La materia prima da acquistare deve esistere (essere presente nel magazzino del trasformatore), altrimenti si riceverà il seguente messaggio di errore:
> "il lotto inserito e' insesistente."

La quantità di prodotto da acquistare deve essere minore di quella presente in magazzino, altrimenti si riceverà il seguente messaggio di errore:
> "la quantita' inserita e' piu' grande della quantita' disponibile."

<!--### Vedere dettagli prodotto acquistato-->

## Autori
:computer: Margherita Galeazzi -> https://github.com/MargheritaGaleazzi

:computer: Chiara Amalia Caporusso -> https://github.com/ChiaraAmalia

:computer: Simone Scalella -> https://github.com/Simone-Scalella

:computer: Zhang Yihang ->  https://github.com/Accout-Personal

