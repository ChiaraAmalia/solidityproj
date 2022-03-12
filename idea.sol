//
contract Magazzino {

    address Produttore; //colui che produce le materie prime
    address Trasformatore; //colui che trasforma le materie prime in prodotti finiti
    address Consumatore; //colui che acquisterà il prodotto finito

    struct LottoMateria{
        string nomeId;// => id della mappa;
        uint256 materiaPrima; //id della materia prima che questo lotto appartiene
        uint256 footprintMateriaPrima; //foot print per kg di questo lotto
        uint quantitaLotto;
        bool contenuto;
    }

    struct MateriaPrima {
        //uint256 id //id della materia prima.
        string nomeMateriaPrima;
        address indirizzoProduttore;
        uint256 quantitaMagazzino; //quantita' totale di tutti i lotti
        uint[] lottoMaterie; //id dei lotto materie
        bool contenuto;
        
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

    event StampaMateriaPrima(string lottoMateriaPrima, string nomeMateriaPrima, address indirizzoProduttore, uint256 quantitaMagazzino, uint256 footprintMateriaPrima);
    //funzione che consente l'inserimento di materie prime da parte del produttore
    function aggiungiMateriaPrima(string memory _nomeMateriaPrima, uint256 _quantitaMagazzino, uint256 _footprintMateriaPrima, uint256 _tipoMateriaPrima) public {
        require(msg.sender == Produttore,"solo il produttore puo' produrre la materia prima.");
        require(_quantitaMagazzino > 0,"la quantita' deve essere maggiore di 0.");
        require(_footprintMateriaPrima > 0, "il footprint deve essere maggiore di 0.");

        uint id = 0;

        if(_tipoMateriaPrima ==0){//inserire lotto di una materia prima.
            
            numMateriePrime ++;
            id = numMateriePrime;
            nomiMateriePrime[id]=MateriaPrima({
                //MateriaPrima: string(abi.encodePacked(_nomeMateriaPrima, toString(numMateriePrime))),
                nomeMateriaPrima: _nomeMateriaPrima,
                indirizzoProduttore: Produttore,
                quantitaMagazzino: _quantitaMagazzino,
                contenuto: true,
                lottoMaterie: new uint[](0)
            });
        }
        else{
            id = _tipoMateriaPrima;
            nomiMateriePrime[id].quantitaMagazzino += _quantitaMagazzino;
        }
        
        numLotto++;
        elencoMateriePrime[string(abi.encodePacked(_nomeMateriaPrima, toString(numLotto)))] = LottoMateria({
            nomeId: string(abi.encodePacked(_nomeMateriaPrima, toString(numLotto))),
            materiaPrima: id,
            footprintMateriaPrima: _footprintMateriaPrima,
            quantitaLotto: _quantitaMagazzino,
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
                result[j] = (string (abi.encodePacked(nomiMateriePrime[i].nomeMateriaPrima,nomiMateriePrime[i].lottoMaterie[k])));
                j++;
            }
        }
        return result;
    }

    function VediMateriaPrimaDaUnLotto(string memory lottoMateria) public view returns(MateriaPrima memory materia) {
        require(elencoMateriePrime[lottoMateria].contenuto,"il lotto non esiste");
        require(nomiMateriePrime[elencoMateriePrime[lottoMateria].materiaPrima].contenuto,"la materia prima non esiste");
        return nomiMateriePrime[elencoMateriePrime[lottoMateria].materiaPrima];
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