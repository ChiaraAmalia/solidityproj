// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;
pragma abicoder v2;

/**
 * @title Magazzino delle materie prime
 * @dev Gestione del magazzino delle materie prime
 */

 contract Consumatore {

     address Consumatore; //colui che acquisterà il prodotto finito
     address public Copy;

     constructor(address _consumatore) {
        Consumatore = _consumatore;
        Copy = _consumatore;
    }

    //attributi magazzino del consumatore
    struct MagazzinoConsumatore {
        address indirizzoConsumatore;
        string lottoProdotto;
        uint256 quantitaMagazzino;
        bool contenuto;
    }

    mapping(string => MagazzinoConsumatore) magazzinoConsumatore; //contiene i prodotti acquistati dal consumatore

    //questa funzione viene richiamata all'interno del contratto del trasformatore per effettuare l'acquisto del prodotto
    //da parte del consumatore. Il prodotto acquistato con relativa quantità viene quindi registrato nel magazzino del consumatore.
    //Se esistente, ne viene semplicemente incrementata la quantità disponibile
    function CacquistaProdotto(string memory _lottoProdotto, uint256 _quantitaMagazzino)public payable{
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

    }


// Funzione utilizzata per stampare le informazioni di un prodotto acquistato dal consumatore
    function StampaInforProdCons(string memory _lottoProdotto) public view returns(MagazzinoConsumatore memory){
        require(msg.sender == Consumatore, "solo il consumatore puo' vedere le informazioni relative ad un lotto di un prodotto acquistato dal consumatore.");
        require(magazzinoConsumatore[_lottoProdotto].contenuto, "il lotto inserito e' inesistente.");
        return magazzinoConsumatore[_lottoProdotto];
    }
 }