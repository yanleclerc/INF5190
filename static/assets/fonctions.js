function validerMatricule(){
    let matriculeRegEx = new RegExp('[a-zA-Z]{3}-[0-9]{2}');
    let matriculeId = document.getElementById("matricule_id").value;


    if ( !matriculeRegEx.test(matriculeId) ){
        document.getElementById("invalid_matricule").innerHTML
            = "Le matricule ne respecte pas le format suivant: XXX-99";
        return false;
    }
    return true;
}

function validerHeures(){
    let codeProjet = document.getElementById("code_de_projet").value;
    let duree = document.getElementById("duree").value;

    if (codeProjet){


        return false;
    }
    if (duree){


        return false;
    }
    return true
}
