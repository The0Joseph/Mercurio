function mensajeError(obj){
    let html = '';
    // Si el tipo de objecto es igual a un object
    if(typeof(obj) === 'object'){
        html = '<ul>';

        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>';
        });
    
        html += '</ul>';
    }
    else{
        html += '<p>'+obj+'</p>';
    }



    Swal.fire({
        icon: 'error',
        title: 'Error!',
        html: html,
      })
}

