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

//function alerta eliminar

function alerta_Eliminar(context, callback){
    Swal.fire({
        title: '¿Estás seguro de eliminar ' + context + '?',
        text: "Al aceptar esta acción se procede a eliminar " + context ,
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        cancelButtonText: 'No',
        confirmButtonText: 'Sí'
      }).then((result) => {
        if (result.isConfirmed) {
            callback();
        }

    })
}

function submit_ajax(url, parameters, callback){
    $.ajax({
        type: "POST",
        url: url,
        data: parameters,
        dataType: "json",
        processData: false,
        contentType: false
    })
    .done(function(data){

        if (!data.hasOwnProperty('error')){
            callback();
            return false
        }
        mensajeError(data.error)

    })
    .fail(function(jqXHR, textStatus, errorThrown){
        alert(textStatus + ' '+ errorThrown)
    })
}

function message_error(context){
    Swal.fire(
        'Error',
        context,
        'error'
      )
}

