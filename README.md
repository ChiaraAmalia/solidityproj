# :leaves: Foot Print Calculator :leaves:

Il nostro progetto consente di tenere traccia del footprint di un prodotto a partire dalla materia prima del quale e composto e considerando la lavorazione necessaria alla sua produzione.

 ## Indice
 1. Come installare il programma;
 2. A cosa serve il programma;
 3. ...

## Come installare il programma

## Prerequisiti

Il nostro progetto sfrutta le seguenti tecnologie:

- [node.js] 
- Docker
- quorum-wizard


<!--## Installation

Dillinger requires [Node.js](https://nodejs.org/) v10+ to run.

Install the dependencies and devDependencies and start the server.

```sh
cd dillinger
npm i
node app
```

For production environments...

```sh
npm install --production
NODE_ENV=production node app
```


```sh
karma test
```-->



### Docker

Il nostro **foot print calculator** è davvero facile da installare ed utilizzare. Sfrutta docker per la gestione in locale dei nodi della blockchain.

Come prima cosa bisogna installare docker per fare ciò basta seguire le indicazioni riportate nel seguente link: [Come installare docker](https://docs.docker.com/desktop/windows/install/)  

### NodeJS
Per prima cosa bisogna eseguire il download di NodeJS, cliccando sul seguente link:[Download NodeJS](https://nodejs.org/it/) e seguire poi le istruzioni dell'installer.

### Quorum-wizard

Per installare quorum-wizard basterà aprire il terminale di windows ed eseguire i seguenti comandi:

```sh
npx quorum-wizard 
```
E seguire le indicazioni, e quando viene richiesto di scegliere tra docker-compose e Kubernetes, scegliere **docker-compose**.

```sh
cd networks/<nome_network>/
start.cmd
```
This will create the dillinger image and pull in the necessary dependencies.
Be sure to swap out `${package.json.version}` with the actual
version of Dillinger.

Once done, run the Docker image and map the port to whatever you wish on
your host. In this example, we simply map port 8000 of the host to
port 8080 of the Docker (or whatever port was exposed in the Dockerfile):

```sh
docker run -d -p 8000:8080 --restart=always --cap-add=SYS_ADMIN --name=dillinger <youruser>/dillinger:${package.json.version}
```

> Note: `--capt-add=SYS-ADMIN` is required for PDF rendering.

Verify the deployment by navigating to your server address in
your preferred browser.

```sh
127.0.0.1:8000
```

## Autori
:computer: Margherita Galeazzi -> https://github.com/MargheritaGaleazzi

:computer: Chiara Amalia Caporusso -> https://github.com/ChiaraAmalia

:computer: Simone Scalella -> 

:computer: Zhang Yihang -> 

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen.

[node.js]: <http://nodejs.org>
