// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;
pragma abicoder v2;
import "./Trasformatore.sol";

/**
 * @title Magazzino delle materie prime
 * @dev Gestione del magazzino delle materie prime
 */

 contract Magazzino {

    uint256 numMateriePrime;
    Trasformatore ContractT;

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



    address Produttore; //colui che produce le materie prime

    mapping(string => MateriaPrima) elencoMateriePrime; //contiene le materie prime inserite dal produttore
    mapping(uint256 => MateriaPrima) nomiMateriePrime; //contiene le materie prime inserite dal produttore

    constructor(address _produttore, address _consumatore,address _addressTrasformatore) {
        Produttore = _produttore;
        numMateriePrime = 0;
        ContractT = Trasformatore(_addressTrasformatore);
    }
    
    event StampaMateriaPrima(string lottoMateriaPrima, string nomeMateriaPrima, address indirizzoProduttore, uint256 quantitaMagazzino, uint256 footprintMateriaPrima);

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
        require(_quantitaMagazzino > 0,"la quantita' deve essere maggiore di 0.");
        require(elencoMateriePrime[_lottoMateriaPrima].contenuto,"la materia prima e' inesistente");
        require(elencoMateriePrime[_lottoMateriaPrima].quantitaMagazzino >= _quantitaMagazzino,"scorta non sufficente.");
        ContractT.TacquistaMateriaPrima(_lottoMateriaPrima, _quantitaMagazzino);
        elencoMateriePrime[_lottoMateriaPrima].quantitaMagazzino -= _quantitaMagazzino;
        elencoMateriePrime[_lottoMateriaPrima].quantitaMagazzino -= _quantitaMagazzino;
        emit AcquistaMateriaPrima(_lottoMateriaPrima, elencoMateriePrime[_lottoMateriaPrima].nomeMateriaPrima, msg.sender, _quantitaMagazzino, elencoMateriePrime[_lottoMateriaPrima].footprintMateriaPrima);
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
        
        require(ContractT.CheckAddress(msg.sender), "solo il Trasformatore puo' vedere tutti i lotti delle materie prime inserite dal produttore.");
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


    /**
     * @dev Converts a `uint256` to its ASCII `string` decimal representation.
     */

    // Funzione utilizzata per stampare le informazioni di una materia prima inserita da un produttore
    function StampaInforMatPrProd(string memory _lottoMateriaPrima) public view returns(MateriaPrima memory){
        require(ContractT.CheckAddress(msg.sender), "solo il trasformatore puo' vedere le informazioni relative ad un lotto di una materia prima inserito dal produttore.");
        require(elencoMateriePrime[_lottoMateriaPrima].contenuto, "il lotto inserito e' inesistente.");
        return elencoMateriePrime[_lottoMateriaPrima];
    }

    function aggiungiProdotto(string memory _nomeProdotto, string[] memory _lottiMateriePrime, uint256[] memory _quantMatPrUtil, uint256 _quantitaMagazzino, uint256 _footprintProdottoFinito) public payable {
        require(ContractT.CheckAddress(msg.sender), "solo il trasformatore puo' aggiungere un prodotto.");
        require(_quantitaMagazzino > 0, "la quantita' prodotta deve essere un valore positivo e diverso da zero.");
        require(_footprintProdottoFinito > 0, "il footprint del prodotto deve essere un valore positivo e diverso da zero.");
        uint arrayLength = _lottiMateriePrime.length;
        uint oldfootprint = 0;
        for(uint i=0; i<arrayLength; i++){
            oldfootprint += elencoMateriePrime[_lottiMateriePrime[i]].footprintMateriaPrima;
        }

        for(uint i=0; i<arrayLength; i++) {
            magazzinoTrasformatore[_lottiMateriePrime[i]].quantitaMagazzino -= _quantMatPrUtil[i];
        }
        ContractT(_nomeProdotto, _lottiMateriePrime,_quantMatPrUtil,_quantitaMagazzino,_footprintProdottoFinito,oldfootprint); 
    }

 }