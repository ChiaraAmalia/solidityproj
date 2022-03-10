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
    }

    //attributi magazzino del consumatore
    struct MagazzinoConsumatore {
        address indirizzoConsumatore;
        string lottoProdotto;
        uint256 quantitaMagazzino;
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

    mapping(string => MateriaPrima) elencoMateriePrime; //contiene le materie prime
    mapping(string => MagazzinoTrasformatore) magazzinoTrasformatore; //contiene le materie prime presenti nel magazzino del trasformatore
    mapping(string => ProdottoFinito) elencoProdotti; //contiene i prodotti che vengono inseriti dal trasformatore
    mapping(string => MagazzinoConsumatore) magazzinoConsumatore; //contiene i prodotti acquistati dal consumatore

    mapping(uint256 => MateriaPrima) nomiMateriePrime;  //tipologia di materia prima
    mapping(uint256 => ProdottoFinito) nomiProdottiFiniti;

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
        require(elencoMateriePrime[_lottoMateriaPrima].quantitaMagazzino >= _quantitaMagazzino,"la scorta non sufficente.");

        magazzinoTrasformatore[_lottoMateriaPrima] = MagazzinoTrasformatore({
            lottoMateriaPrima: _lottoMateriaPrima,
            quantitaMagazzino: _quantitaMagazzino,
            indirizzoTrasformatore: Trasformatore
        });

        elencoMateriePrime[_lottoMateriaPrima].quantitaMagazzino -= _quantitaMagazzino;

        emit AcquistaMateriaPrima(_lottoMateriaPrima, elencoMateriePrime[_lottoMateriaPrima].nomeMateriaPrima, msg.sender, _quantitaMagazzino, elencoMateriePrime[_lottoMateriaPrima].footprintMateriaPrima);
    }

    //funzione che permette l'inserimento di prodotti finiti da parte del trasformatore
    function aggiungiProdotto(string memory _nomeProdotto, string[] memory _lottiMateriePrime, uint256[] memory _quantMatPrUtil, uint256 _quantitaMagazzino, uint256 _footprintProdottoFinito) public payable {
        require(msg.sender == Trasformatore);
        require(_quantitaMagazzino > 0);
        require(_footprintProdottoFinito > 0);
        uint arrayLength = _lottiMateriePrime.length;

        for (uint i=0; i<arrayLength;i++){
            require(_quantMatPrUtil[i] <= magazzinoTrasformatore[_lottiMateriePrime[i]].quantitaMagazzino);
            require(magazzinoTrasformatore[_lottiMateriePrime[i]].quantitaMagazzino > 0);
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
        require(msg.sender == Consumatore);
        require(_quantitaMagazzino > 0);
        require(elencoProdotti[_lottoProdotto].contenuto);
        require(elencoProdotti[_lottoProdotto].quantitaProdotta >= _quantitaMagazzino);

        magazzinoConsumatore[_lottoProdotto] = MagazzinoConsumatore({
            lottoProdotto: _lottoProdotto,
            quantitaMagazzino: _quantitaMagazzino,
            indirizzoConsumatore: Consumatore
        });

        elencoProdotti[_lottoProdotto].quantitaProdotta -= _quantitaMagazzino;

        emit AcquistaProdotto(_lottoProdotto, elencoProdotti[_lottoProdotto].nomeProdotto, msg.sender, _quantitaMagazzino, elencoProdotti[_lottoProdotto].footprintTrasformazione);
    }

    //funzione che ci consente di vedere il footprint di un dato prodotto finito
    function vediFootprintProdottoFinito(string memory _lottoProdotto) public view returns (string memory) {
        if(elencoProdotti[_lottoProdotto].contenuto){
            uint256 fp = elencoProdotti[_lottoProdotto].footprintTrasformazione;
            return string(abi.encodePacked(string(abi.encodePacked(string(abi.encodePacked("Il footprint di: ", _lottoProdotto)), "e' pari a: ")),toString(fp)));
        }
        else return "tale prodotto non e' presente in magazzino";
    }

    //funzione che ci consente di vedere i lotti del prodotto
    function vediLottiProdotto(string memory _nomeProdotto) public view returns (string[] memory){
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

    // Funzione utilizzata per stampare un prodotto acquistato
    function StampaProdotti(string memory _LottoProdotto) public view returns(MagazzinoConsumatore memory){
        require(msg.sender == Consumatore);
        require(elencoProdotti[_LottoProdotto].contenuto);
        return magazzinoConsumatore[_LottoProdotto];
    }
 }