
contract Magazzino {



    struct LottoMateria{
        string MateriaPrima; //id della materia prima
        uint256 footprintMateriaPrima; //foot print per kg di questo lotto
        uint quantitaLotto;
        bool contenuto;
    }

    struct MateriaPrima {
        string nomeMateriaPrima; //chiave della mappa
        address indirizzoProduttore;
        uint256 quantitaMagazzino; //quantita' totale di tutti i lotti
        bool contenuto;
        uint[] lottoMaterie; //id dei lotto materie
    }

    uint256 numMateriePrime;
    uint256 numProdotti;

    mapping(uint256 => MateriaPrima) nomiMateriePrime;  //Prodotto
    mapping(string => LottoMateria) elencoMateriePrime; //i Lotti di materie

    //la funzione che mi consente di vedere i lotti di un determinato materia prima
    function vediLottiMateriaPrima(uint256 _nomeMateriaPrima /*id della materia prima */)  public view returns (string[] memory){
        string[] memory result = new string[](numMateriePrime);      
        uint j = 0;
        MateriaPrima memory materia = nomiMateriePrime[_nomeMateriaPrima];
        for(uint i=0; i<=materia.lottoMaterie.length; i++){
            result[i] = string(abi.encodePacked(materia.nomeMateriaPrima,materia.lottoMaterie[i]));
        }
        return result;
    }

    //funzione che mi consente di vedere tutti i lotti delle materie prime
    function vediTuttiLottiMateriePrime() public view returns (string[] memory){
        string[] memory result= new string[](numMateriePrime);
        uint j = 0;

        for(uint i=0; i< numMateriePrime; i++){
            for(uint k=0;k<nomiMateriePrime[i].lottoMaterie.length;k++){
                result.push(string (abi.encodePacked(<nomiMateriePrime[i].nomeMateriaPrima,<nomiMateriePrime[i].lottoMaterie[k])));
            }
        }
        return result;
    }

    function VediMateriaPrimaDaUnLotto(string memory lottoMateria) public view {
        
    }
}