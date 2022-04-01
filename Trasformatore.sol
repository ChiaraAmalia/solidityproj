// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;
pragma abicoder v2;
import "./Consumatore.sol";

/**
 * @title Magazzino delle materie prime
 * @dev Gestione del magazzino delle materie prime
 */

 contract Trasformatore {

     address Trasformatore; //colui che trasforma le materie prime in prodotti finiti
     uint256 numProdotti;
     Consumatore ConsContract;

     constructor(address _trasformatore,address _ConsContract) {
        Trasformatore = _trasformatore;
        numProdotti = 0;
        ConsContract = Consumatore(_ConsContract);
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

        //attributi magazzino del trasformatore
    struct MagazzinoTrasformatore {
        address indirizzoTrasformatore;
        string lottoMateriaPrima;
        uint256 quantitaMagazzino;
        bool contenuto;
    }

    mapping(string => MagazzinoTrasformatore) magazzinoTrasformatore; //contiene le materie prime presenti nel magazzino del trasformatore
    mapping(string => ProdottoFinito) elencoProdotti; //contiene i prodotti che vengono inseriti dal trasformatore
    mapping(uint256 => ProdottoFinito) nomiProdottiFiniti; //contiene i prodotti finiti inseriti dal trasformatore

    event AcquistaMateriaPrima(string lottoMateriaPrima, string nomeMateriaPrima, address indirizzoTrasformatore, uint256 quantitaMagazzino, uint256 footprintMateriaPrima);
    event StampaProdotto(string lottoProdotto, string nomeProdotto, address indirizzoTrasformatore, string[] lottiMateriePrime, uint256 quantitaProdotta, uint256 footprintTrasformazione);
    event AcquistaProdotto(string lottoProdotto, string nomeProdotto, address indirizzoConsumatore, uint256 quantitaMagazzino, uint256 footprintProdotto);

    function TacquistaMateriaPrima(string memory _lottoMateriaPrima, uint256 _quantitaMagazzino) public payable {
        require(msg.sender == Trasformatore,"solo il trasformatore puo' aquistare la materia prima.");
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


        
    }

    //funzione che permette l'inserimento di prodotti finiti da parte del trasformatore
    function TaggiungiProdotto(string memory _nomeProdotto, string[] memory _lottiMateriePrime, uint256[] memory _quantMatPrUtil, uint256 _quantitaMagazzino, uint256 _footprintProdottoFinito,uint oldfootprint) public payable {

        uint arrayLength = _lottiMateriePrime.length;

        for (uint i=0; i<arrayLength;i++){
            require(magazzinoTrasformatore[_lottiMateriePrime[i]].contenuto, string(abi.encodePacked(string(abi.encodePacked("il lotto ", _lottiMateriePrime[i])), " e' inesistente")));
            require(_quantMatPrUtil[i] <= magazzinoTrasformatore[_lottiMateriePrime[i]].quantitaMagazzino, string(abi.encodePacked(string(abi.encodePacked("la quantita' nel magazzino per il lotto ", magazzinoTrasformatore[_lottiMateriePrime[i]].lottoMateriaPrima)), " non e' sufficiente")));
            require(magazzinoTrasformatore[_lottiMateriePrime[i]].quantitaMagazzino > 0, string(abi.encodePacked(string(abi.encodePacked("le scorte per il lotto ", magazzinoTrasformatore[_lottiMateriePrime[i]].lottoMateriaPrima)), " sono finite")));
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

    //funzione che ci consente di vedere i lotti del prodotto
    function vediLottiProdotto(string memory _nomeProdotto) public view returns (string[] memory){
        require(msg.sender == ConsContract.Copy(), "solo il consumatore puo' vedere tutti i lotti associati ad un prodotto.");
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
        require(msg.sender == ConsContract.Copy(), "solo il consumatore puo' vedere tutti i lotti dei prodotti inseriti dal trasformatore.");
        require(numProdotti>0,"Non sono presenti prodotti");
        string[] memory result=new string[](numProdotti);
        uint j = 0;

        for(uint i=0; i<numProdotti; i++){
        result[j]=nomiProdottiFiniti[i].lottoProdotto;
        j++;
        }
        return result;
    }

    function numeroProdotti() view public returns (uint256){
        return numProdotti;
    }

    // Funzione utilizzata per stampare le informazioni di un prodotto inserito dal trasformatore
    function StampaInforProdTrasf(string memory _lottoProdotto) public view returns(ProdottoFinito memory){
        require(msg.sender == ConsContract.Copy(), "solo il consumatore puo' vedere le informazioni relative ad un lotto di un prodotto inserito dal trasformatore.");
        require(elencoProdotti[_lottoProdotto].contenuto, "il lotto inserito e' inesistente.");
        return elencoProdotti[_lottoProdotto];
    }

    

    // Funzione utilizzata per stampare le informazioni di una materia prima acquistata dal trasformatore
    function StampaMatPrAcq(string memory _lottoMateriaPrima) public view returns(MagazzinoTrasformatore memory){
        require(msg.sender == Trasformatore, "solo il trasformatore puo' vedere le informazioni relative ad un lotto di una materia prima acquistato dal trasformatore.");
        require(magazzinoTrasformatore[_lottoMateriaPrima].contenuto, "il lotto inserito e' inesistente.");
        return magazzinoTrasformatore[_lottoMateriaPrima];
    }

    //funzione che permette al consumatore di acquistare un prodotto finito
    function acquistaProdotto(string memory _lottoProdotto, uint256 _quantitaMagazzino) public payable {
        require(_quantitaMagazzino > 0, "la quantita' acquistata deve essere un valore positivo diverso da zero.");
        require(elencoProdotti[_lottoProdotto].contenuto, "il lotto inserito e' insesistente.");
        require(elencoProdotti[_lottoProdotto].quantitaProdotta >= _quantitaMagazzino, "la quantita' inserita e' piu' grande della quantita' disponibile.");
        ConsContract.CacquistaProdotto(_lottoProdotto,_quantitaMagazzino);
        elencoProdotti[_lottoProdotto].quantitaProdotta -= _quantitaMagazzino;
        emit AcquistaProdotto(_lottoProdotto, elencoProdotti[_lottoProdotto].nomeProdotto, msg.sender, _quantitaMagazzino, elencoProdotti[_lottoProdotto].footprintTrasformazione);
 }

 //funzione che ci consente di vedere il footprint di un dato prodotto finito
    function vediFootprintProdottoFinito(string memory _lottoProdotto) public view returns (string memory) {
        require(msg.sender == ConsContract.Copy(), "solo il consumatore puo' vedere il footprint del prodotto finito.");
        if(elencoProdotti[_lottoProdotto].contenuto){
            uint256 fp = elencoProdotti[_lottoProdotto].footprintTrasformazione;
            return string(abi.encodePacked(string(abi.encodePacked(string(abi.encodePacked("Il footprint di: ", _lottoProdotto)), " e' pari a: ")),toString(fp)));
        }
        else return "Tale lotto non e' presente in magazzino";
    }

    function CheckAddress(address indirizzo)public payable returns(bool){
        if(indirizzo == Trasformatore) return true;
        else return false;
    }

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

 }