const get_dict_form = (form_name) => {
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