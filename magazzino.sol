// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;
pragma abicoder v2;

/**
 * @title Magazzino delle materie prime
 * @dev Gestione del magazzino delle materie prime
 */

 contract Magazzino {

    uint256 numMateriePrime;
    uint256 numProdotti;

    //mapping(address => bool) approvals;

    //attributi materia prima
    struct MateriaPrima {
        uint256 id;
        string lottoMateriaPrima;
        string nomeMateriaPrima;
        address indirizzoProduttore;
        uint256 quantitaMagazzino;
        uint256 footprintMateriaPrima; //foot print per kg della materia prima
        bool contenuto;
    }

    //attributi magazzino del trasformatore
    struct MagazzinoTrasformatore {
        address indirizzoTrasformatore;
        string lottoMateriaPrima;
        uint256 quantitaMagazzino;
        bool contenuto;
    }

    //attributi magazzino del consumatore
    struct MagazzinoConsumatore {
        address indirizzoConsumatore;
        string lottoProdotto;
        uint256 quantitaMagazzino;
        bool contenuto;
    }

    //attributi prodotto finito
    struct ProdottoFinito {
        uint256 id;
        string lottoProdotto;
        string nomeProdotto;
        address indirizzoTrasformatore;
        string[] lottiMateriePrime; //codici identificatori delle materie prime utilizzate per la trasformazione
        uint256 quantitaProdotta;
        uint256 footprintTrasformazione; //footprint per kg del prodotto trasformato
        bool contenuto;
    }

    address Produttore; //colui che produce le materie prime
    address Trasformatore; //colui che trasforma le materie prime in prodotti finiti
    address Consumatore; //colui che acquisterà il prodotto finito

    mapping(string => MateriaPrima) elencoMateriePrime; //contiene le materie prime inserite dal produttore
    mapping(string => MagazzinoTrasformatore) magazzinoTrasformatore; //contiene le materie prime presenti nel magazzino del trasformatore
    mapping(string => ProdottoFinito) elencoProdotti; //contiene i prodotti che vengono inseriti dal trasformatore
    mapping(string => MagazzinoConsumatore) magazzinoConsumatore; //contiene i prodotti acquistati dal consumatore

    mapping(uint256 => MateriaPrima) nomiMateriePrime; //contiene le materie prime inserite dal produttore
    mapping(uint256 => ProdottoFinito) nomiProdottiFiniti; //contiene i prodotti finiti inseriti dal trasformatore

    constructor(address _produttore, address _trasformatore, address _consumatore) {
        Produttore = _produttore;
        Trasformatore = _trasformatore;
        Consumatore = _consumatore;
        numMateriePrime = 0;
        numProdotti = 0;
    }
    
    event StampaMateriaPrima(string lottoMateriaPrima, string nomeMateriaPrima, address indirizzoProduttore, uint256 quantitaMagazzino, uint256 footprintMateriaPrima);
    event AcquistaMateriaPrima(string lottoMateriaPrima, string nomeMateriaPrima, address indirizzoTrasformatore, uint256 quantitaMagazzino, uint256 footprintMateriaPrima);
    event StampaProdotto(string lottoProdotto, string nomeProdotto, address indirizzoTrasformatore, string[] lottiMateriePrime, uint256 quantitaProdotta, uint256 footprintTrasformazione);
    event AcquistaProdotto(string lottoProdotto, string nomeProdotto, address indirizzoConsumatore, uint256 quantitaMagazzino, uint256 footprintProdotto);

    //funzione che consente l'inserimento di materie prime da parte del produttore
    function aggiungiMateriaPrima(string memory _nomeMateriaPrima, uint256 _quantitaMagazzino, uint256 _footprintMateriaPrima) public {
        require(msg.sender == Produttore,"solo il produttore puo' produrre la materia prima.");
        require(_quantitaMagazzino > 0,"la quantita' deve essere maggiore di 0.");
        require(_footprintMateriaPrima > 0, "il footprint deve essere maggiore di 0.");

        
        elencoMateriePrime[string(abi.encodePacked(_nomeMateriaPrima, toString(numMateriePrime)))]=MateriaPrima({
            id: numMateriePrime,
            lottoMateriaPrima: string(abi.encodePacked(_nomeMateriaPrima,toString(numMateriePrime))),
            nomeMateriaPrima: _nomeMateriaPrima,
            indirizzoProduttore: Produttore,
            quantitaMagazzino: _quantitaMagazzino,
            footprintMateriaPrima: _footprintMateriaPrima,
            contenuto: true
        });

        
        nomiMateriePrime[numMateriePrime]=MateriaPrima({
            id: numMateriePrime,
            lottoMateriaPrima: string(abi.encodePacked(_nomeMateriaPrima, toString(numMateriePrime))),
            nomeMateriaPrima: _nomeMateriaPrima,
            indirizzoProduttore: Produttore,
            quantitaMagazzino: _quantitaMagazzino,
            footprintMateriaPrima: _footprintMateriaPrima,
            contenuto: true
        });

        numMateriePrime = numMateriePrime + 1;
        emit StampaMateriaPrima(string(abi.encodePacked(_nomeMateriaPrima, toString(numMateriePrime))), _nomeMateriaPrima, msg.sender, _quantitaMagazzino, _footprintMateriaPrima);
    }

    //funzione che permette al trasformatore di acquistare materia prima
    function acquistaMateriaPrima(string memory _lottoMateriaPrima, uint256 _quantitaMagazzino) public payable {
        require(msg.sender == Trasformatore,"solo il trasformatore puo' aquistare la materia prima.");
        require(_quantitaMagazzino > 0,"la quantita' deve essere maggiore di 0.");
        require(elencoMateriePrime[_lottoMateriaPrima].contenuto,"la materia prima e' inesistente");
        require(elencoMateriePrime[_lottoMateriaPrima].quantitaMagazzino >= _quantitaMagazzino,"scorta non sufficente.");

        if(magazzinoTrasformatore[_lottoMateriaPrima].contenuto){
            magazzinoTrasformatore[_lottoMateriaPrima].quantitaMagazzino += _quantitaMagazzino;
        }
        else{
            magazzinoTrasformatore[_lottoMateriaPrima] = MagazzinoTrasformatore({
                lottoMateriaPrima: _lottoMateriaPrima,
                quantitaMagazzino: _quantitaMagazzino,
                indirizzoTrasformatore: Trasformatore,
                contenuto: true
            });
        }


        elencoMateriePrime[_lottoMateriaPrima].quantitaMagazzino -= _quantitaMagazzino;

        emit AcquistaMateriaPrima(_lottoMateriaPrima, elencoMateriePrime[_lottoMateriaPrima].nomeMateriaPrima, msg.sender, _quantitaMagazzino, elencoMateriePrime[_lottoMateriaPrima].footprintMateriaPrima);
    }

    //funzione che permette l'inserimento di prodotti finiti da parte del trasformatore
    function aggiungiProdotto(string memory _nomeProdotto, string[] memory _lottiMateriePrime, uint256[] memory _quantMatPrUtil, uint256 _quantitaMagazzino, uint256 _footprintProdottoFinito) public payable {
        require(msg.sender == Trasformatore, "solo il trasformatore puo' aggiungere un prodotto.");
        require(_quantitaMagazzino > 0, "la quantita' prodotta deve essere un valore positivo e diverso da zero.");
        require(_footprintProdottoFinito > 0, "il footprint del prodotto deve essere un valore positivo e diverso da zero.");
        uint arrayLength = _lottiMateriePrime.length;

        for (uint i=0; i<arrayLength;i++){
            require(magazzinoTrasformatore[_lottiMateriePrime[i]].contenuto, string(abi.encodePacked(string(abi.encodePacked("il lotto", _lottiMateriePrime[i])), " e' inesistente")));
            require(_quantMatPrUtil[i] <= magazzinoTrasformatore[_lottiMateriePrime[i]].quantitaMagazzino, string(abi.encodePacked(string(abi.encodePacked("la quantita' nel magazzino per il lotto ", magazzinoTrasformatore[_lottiMateriePrime[i]].lottoMateriaPrima)), " non e' sufficiente")));
            require(magazzinoTrasformatore[_lottiMateriePrime[i]].quantitaMagazzino > 0, string(abi.encodePacked(string(abi.encodePacked("le scorte per il lotto ", magazzinoTrasformatore[_lottiMateriePrime[i]].lottoMateriaPrima)), " sono finite")));
        }

        uint oldfootprint = 0;
        for(uint i=0; i<arrayLength; i++){
            oldfootprint += elencoMateriePrime[_lottiMateriePrime[i]].footprintMateriaPrima;
        }

        for(uint i=0; i<arrayLength; i++) {
            magazzinoTrasformatore[_lottiMateriePrime[i]].quantitaMagazzino -= _quantMatPrUtil[i];
        }

        uint256 footprintTot = _footprintProdottoFinito + oldfootprint;

        
        elencoProdotti[string(abi.encodePacked(_nomeProdotto,toString(numProdotti)))]=ProdottoFinito({
            id: numProdotti,
            lottoProdotto: string(abi.encodePacked(_nomeProdotto,toString(numProdotti))),
            nomeProdotto: _nomeProdotto,
            indirizzoTrasformatore: Trasformatore,
            lottiMateriePrime: _lottiMateriePrime,
            quantitaProdotta: _quantitaMagazzino,
            footprintTrasformazione: footprintTot,
            contenuto: true
        });

        
        nomiProdottiFiniti[numProdotti]=ProdottoFinito({
            id: numProdotti,
            lottoProdotto: string(abi.encodePacked(_nomeProdotto,toString(numProdotti))),
            nomeProdotto: _nomeProdotto,
            indirizzoTrasformatore: Trasformatore,
            lottiMateriePrime: _lottiMateriePrime,
            quantitaProdotta: _quantitaMagazzino,
            footprintTrasformazione: footprintTot,
            contenuto: true
        });

        numProdotti = numProdotti + 1;
        emit StampaProdotto(string(abi.encodePacked(_nomeProdotto,toString(numProdotti))), _nomeProdotto, msg.sender, _lottiMateriePrime, _quantitaMagazzino, footprintTot);
    }

    //funzione che permette al consumatore di acquistare un prodotto finito
    function acquistaProdotto(string memory _lottoProdotto, uint256 _quantitaMagazzino) public payable {
        require(msg.sender == Consumatore, "solo il consumatore puo' acquistare un prodotto.");
        require(_quantitaMagazzino > 0, "la qauntita' acquistata deve essere un valore positivo diverso da zero.");
        require(elencoProdotti[_lottoProdotto].contenuto, "il lotto inserito e' insesistente.");
        require(elencoProdotti[_lottoProdotto].quantitaProdotta >= _quantitaMagazzino, "la quantita' inserita e' piu' grande della quantita' disponibile.");

        if(magazzinoConsumatore[_lottoProdotto].contenuto) {
            magazzinoConsumatore[_lottoProdotto].quantitaMagazzino += _quantitaMagazzino;
        }
        else {
            magazzinoConsumatore[_lottoProdotto] = MagazzinoConsumatore({
                lottoProdotto: _lottoProdotto,
                quantitaMagazzino: _quantitaMagazzino,
                indirizzoConsumatore: Consumatore,
                contenuto: true
            });
        }

        elencoProdotti[_lottoProdotto].quantitaProdotta -= _quantitaMagazzino;

        emit AcquistaProdotto(_lottoProdotto, elencoProdotti[_lottoProdotto].nomeProdotto, msg.sender, _quantitaMagazzino, elencoProdotti[_lottoProdotto].footprintTrasformazione);
    }

    //funzione che ci consente di vedere il footprint di un dato prodotto finito
    function vediFootprintProdottoFinito(string memory _lottoProdotto) public view returns (string memory) {
        require(msg.sender == Consumatore, "solo il consumatore puo' vedere il footprint del prodotto finito.");
        if(elencoProdotti[_lottoProdotto].contenuto){
            uint256 fp = elencoProdotti[_lottoProdotto].footprintTrasformazione;
            return string(abi.encodePacked(string(abi.encodePacked(string(abi.encodePacked("Il footprint di: ", _lottoProdotto)), " e' pari a: ")),toString(fp)));
        }
        else return "tale prodotto non e' presente in magazzino.";
    }

    //funzione che ci consente di vedere i lotti del prodotto
    function vediLottiProdotto(string memory _nomeProdotto) public view returns (string[] memory){
        require(msg.sender == Consumatore, "solo il consumatore puo' vedere tutti i lotti associati ad un prodotto.");
        string[] memory result=new string[](numProdotti);
        uint j = 0;

        for(uint i=0; i<numProdotti; i++){
            if(keccak256(abi.encodePacked(nomiProdottiFiniti[i].nomeProdotto)) == keccak256(abi.encodePacked(_nomeProdotto))){
                result[j] = nomiProdottiFiniti[i].lottoProdotto;
                j++;
            }
        }
        return result;
    }

    //funzione che mi consente di vedere tutti i lotti dei prodotti
    function vediTuttiLottiProdotti() public view returns (string[] memory) {
        require(msg.sender == Consumatore, "solo il consumatore puo' vedere tutti i lotti dei prodotti inseriti dal trasformatore.");
        require(numProdotti>0,"Non sono presenti prodotti");
        string[] memory result=new string[](numProdotti);
        uint j = 0;

        for(uint i=0; i<numProdotti; i++){
        result[j]=nomiProdottiFiniti[i].lottoProdotto;
        j++;
        }
        return result;
    }

    //funzione che mi consente di vedere i lotti di un determinato materia prima
    function vediLottiMateriaPrima(string memory _nomeMateriaPrima)  public view returns (string[] memory){
        require(msg.sender == Trasformatore, "solo il trasformatore puo' vedere tutti i lotti associati ad una materia prima");
        string[] memory result = new string[](numMateriePrime);      
        uint j = 0;

        for(uint i=0; i<=numMateriePrime; i++){
            if(keccak256(abi.encodePacked(nomiMateriePrime[i].nomeMateriaPrima)) == keccak256(abi.encodePacked(_nomeMateriaPrima))){
                result[j] = nomiMateriePrime[i].lottoMateriaPrima;
                j++;
            }
        }
        return result;
    }

    //funzione che mi consente di vedere tutti i lotti delle materie prime
    function vediTuttiLottiMateriePrime() public view returns (string[] memory){
        
        require(msg.sender == Trasformatore, "solo il Trasformatore puo' vedere tutti i lotti delle materie prime inserite dal produttore.");
        require(numMateriePrime>0,"Non sono presenti materie prime");
        string[] memory result= new string[](numMateriePrime);
        uint j = 0;

        for(uint i=0; i< numMateriePrime; i++){
            result[j] = nomiMateriePrime[i].lottoMateriaPrima;
            j++;
        }
        return result;
    }


    function numeroMateriePrime() view public returns (uint256){
        return numMateriePrime;
    }

    function numeroProdotti() view public returns (uint256){
        return numProdotti;
    }

    /**
     * @dev Converts a `uint256` to its ASCII `string` decimal representation.
     */
    function toString(uint256 value) internal pure returns (string memory) {
        
        if(value == 0) {
            return "0";
        }

        uint256 temp = value;
        uint256 digits;
        while(temp !=0) {
            digits++;
            temp /= 10;
        }
        bytes memory buffer = new bytes(digits);
        while(value != 0) {
            digits -= 1;
            buffer[digits] = bytes1(uint8(48 + uint256(value % 10)));
            value /= 10;
        }
        return string(buffer);
    }

    // Funzione utilizzata per stampare le informazioni di un prodotto inserito dal trasformatore
    function StampaInforProdTrasf(string memory _lottoProdotto) public view returns(ProdottoFinito memory){
        require(msg.sender == Consumatore, "solo il consumatore puo' vedere le informazioni relative ad un lotto di un prodotto inserito dal trasformatore.");
        require(elencoProdotti[_lottoProdotto].contenuto, "il lotto inserito e' inesistente.");
        return elencoProdotti[_lottoProdotto];
    }

    // Funzione utilizzata per stampare le informazioni di una materia prima inserita da un produttore
    function StampaInforMatPrProd(string memory _lottoMateriaPrima) public view returns(MateriaPrima memory){
        require(msg.sender == Trasformatore, "solo il trasformatore puo' vedere le informazioni relative ad un lotto di una materia prima inserito dal produttore.");
        require(elencoMateriePrime[_lottoMateriaPrima].contenuto, "il lotto inserito e' inesistente.");
        return elencoMateriePrime[_lottoMateriaPrima];
    }

    // Funzione utilizzata per stampare le informazioni di una materia prima acquistata dal trasformatore
    function StampaMatPrAcq(string memory _lottoMateriaPrima) public view returns(MagazzinoTrasformatore memory){
        require(msg.sender == Trasformatore, "solo il trasformatore puo' vedere le informazioni relative ad un lotto di una materia prima acquistato dal trasformatore.");
        require(magazzinoTrasformatore[_lottoMateriaPrima].contenuto, "il lotto inserito e' inesistente.");
        return magazzinoTrasformatore[_lottoMateriaPrima];
    }

    // Funzione utilizzata per stampare le informazioni di un prodotto acquistato dal consumatore
    function StampaInforProdCons(string memory _lottoProdotto) public view returns(MagazzinoConsumatore memory){
        require(msg.sender == Consumatore, "solo il consumatore puo' vedere le informazioni relative ad un lotto di un prodotto acquistato dal consumatore.");
        require(magazzinoConsumatore[_lottoProdotto].contenuto, "il lotto inserito e' inesistente.");
        return magazzinoConsumatore[_lottoProdotto];
    }
 }