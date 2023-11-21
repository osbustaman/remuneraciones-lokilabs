const get_dict_form = (form_name) => {
    /**
     * 
     * :form_name: id del formulario
     * 
     * 
     * :return
     *      diccionario con los inputs del formulario
     * 
    */
    const formulario = document.getElementById(form_name);
    const elementos = formulario.elements;
    const diccionario = {};
    for (let i = 0; i < elementos.length; i++) {
        const elemento = elementos[i];
        let key = elemento.id;

        const classes = elemento.className.split(' ');
        const hasRequiredClass = classes.includes('not-required');

        if (!hasRequiredClass) {
            diccionario[key] = elemento.value;
        }
    }
    return diccionario;
}


const save_data = (form_name) => {
    const dict_form = get_dict_form(form_name);
    const _validate_inputs = validate_inputs(form_name);

    console.log(`${_validate_inputs}`);

    if(!_validate_inputs){
        console.log(`no se envian datos`);


    }else{
        console.log(`se envia datos`);
    }
}