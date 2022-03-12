//
contract Magazzino {



    struct LottoMateria{
        //id lotto => id della mappa;
        uint256 MateriaPrima; //id della materia prima che questo lotto appartiene
        uint256 footprintMateriaPrima; //foot print per kg di questo lotto
        uint quantitaLotto;
        bool contenuto;
    }

    struct MateriaPrima {
        //uint256 id //id della materia prima.
        string nomeMateriaPrima;
        address indirizzoProduttore;
        uint256 quantitaMagazzino; //quantita' totale di tutti i lotti
        bool contenuto;
        uint[] lottoMaterie; //id dei lotto materie
    }

    uint256 numMateriePrime;
    uint256 numProdotti;
    uint256 numLotto; //numero lotto

    constructor(address _produttore, address _trasformatore, address _consumatore) {
        Produttore = _produttore;
        Trasformatore = _trasformatore;
        Consumatore = _consumatore;
        numMateriePrime = 0;
        numProdotti = 0;
    }

    mapping(uint256 => MateriaPrima) nomiMateriePrime;  //Prodotto
    mapping(string => LottoMateria) elencoMateriePrime; //i Lotti di materie

    //funzione che consente l'inserimento di materie prime da parte del produttore
    function aggiungiMateriaPrima(string memory _nomeMateriaPrima, uint256 _quantitaMagazzino, uint256 _footprintMateriaPrima, uint256 _tipoMateriaPrima) public {
        require(msg.sender == Produttore,"solo il produttore puo' produrre la materia prima.");
        require(_quantitaMagazzino > 0,"la quantita' deve essere maggiore di 0.");
        require(_footprintMateriaPrima > 0, "il footprint deve essere maggiore di 0.");

        uint id = 0;

        if(_tipoMateriaPrima ==0){//inserire lotto di una materia prima.
            
            numMateriePrime ++;
            id = numeroMateriePrime;
            nomiMateriePrime[id]=MateriaPrima({
                id: id,
                MateriaPrima: string(abi.encodePacked(_nomeMateriaPrima, toString(numMateriePrime))),
                nomeMateriaPrima: _nomeMateriaPrima,
                indirizzoProduttore: Produttore,
                quantitaMagazzino: _quantitaMagazzino,
                footprintMateriaPrima: _footprintMateriaPrima,
                contenuto: true
            });
        }
        else{
            id = _tipoMateriaPrima;
            nomiMateriePrime[id].quantitaMagazzino += _quantitaMagazzino;
            nomiMateriePrime[id]._footprintMateriaPrima += _footprintMateriaPrima;
        }
        
        numLotto++;
        elencoMateriePrime[string(abi.encodePacked(_nomeMateriaPrima, toString(numLotto)))]=MateriaPrima({
            id: numLotto,
            MateriaPrima: id,
            indirizzoProduttore: Produttore,
            quantitaLotto: _quantitaMagazzino,
            footprintMateriaPrima: _footprintMateriaPrima,
            contenuto: true
        });
        nomiMateriePrime[id].lottoMaterie.push(numLotto);

        

        
        emit StampaMateriaPrima(string(abi.encodePacked(_nomeMateriaPrima, toString(numMateriePrime))), _nomeMateriaPrima, msg.sender, _quantitaMagazzino, _footprintMateriaPrima);
    }

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
                result.push(string (abi.encodePacked(nomiMateriePrime[i].nomeMateriaPrima,nomiMateriePrime[i].lottoMaterie[k])));
            }
        }
        return result;
    }

    function VediMateriaPrimaDaUnLotto(string memory lottoMateria) public view returns(MateriaPrima memory materia) {
        require(elencoMateriePrime[lottoMateria].contenuto,"il lotto non esiste");
        require(nomiMateriePrime[elencoMateriePrime[lottoMateria].MateriaPrima],"la materia prima non esiste");
        returns nomiMateriePrime[elencoMateriePrime[lottoMateria].MateriaPrima];
    }

}