$(document).ready(function(){

    let tableCliente;

    function get_data_dataTable(){
        tableCliente = $('#data').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            paging: true,
            lengthMenu: [5, 10, 15, 20],  // Opciones de número de registros por página
            pageLength: 5 , // Mostrar 5 registros por página de forma predeterminada
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'searchdata'
                }, //Paramentros
                dataSrc: ""
            },
            columns: [
                {"data": "names"},
                {"data": "dni"},
                {"data": "address"},
                {"data": "names"},
            ],
            columnDefs: [
                
                {
                    // responsivePriority: 1,
                    targets: [0],
                    // class: 'text-center',
                    orderable: false,
                    render: function(data, type, row){
                        // console.log(row.dni)
                        console.log(row.date_birthday)
                        return `<div class="p-2">
                                    <img src="" alt="" width="70" class="img-fluid rounded shadow-sm" />
                                    <div class="ml-3 d-inline-block align-middle">
                                        <h5 class="mb-0"><p href="#" class="text-dark d-inline-block">${row.names +' '+ row.surnames}</p></h5><span class="text-muted font-weight-normal font-italic d-block">${row.gender.name} ${row.date_birthday}</span>
                                    </div>
                                </div>`;
                    }
                },
    
                {
                    // responsivePriority: 2, 
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function(data, type, row){
                        return `<div class="d-flex">
                                    <div class="m-2">
                                        <a href="#" rel="edit" class="btn btn-warning"><i class="fa-solid fa-pen-to-square"></i></a>
                                    </div>
                                    <div class="m-2">
                                        <a href="#" rel="delete" class="btn btn-danger"><i class="fa-solid fa-trash"></i></a>
                                    </div>
                                </div>`;
                    }
                },
            ],
            initComplete: function(setting, json){
                // alert('Tablacargada')
            }
        });
    }


    get_data_dataTable();

    $('.btnAdd').on('click', function(){
        $('input[name="action"]').val('add');
        // resetar el formulario
        $('form')[0].reset(); 
        $('#modalView').modal('show');
    })

    // $('#modalView').on('shown.bs.modal', function () {
    //     $('form')[0].reset();
    // })

    // window.$('#modalView').modal('show');

    $('form').on('submit', function(e){
      e.preventDefault();
      
      let parameters = new FormData(this)
        //   console.log(parameters)
     $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: parameters,
        dataType: 'json',
        processData: false,
        contentType: false
      })
      .done(function(data){

        if (!data.hasOwnProperty('error')){
            $('#modalView').modal('hide');
            
            tableCliente.ajax.reload();
            // get_data_dataTable()
            // location.reload()
            return
        }
        mensajeError(data.error)

      })
      .fail(function(jqXHR, textStatus, errorThrown){
        alert(textStatus + ' '+ errorThrown)
      })
    })
    
    $('#data').on('click', 'a[rel="edit"]', function(){
        let tr = tableCliente.cell( $(this).closest('td, li') ).index();
        let data = tableCliente.row(tr.row).data();

        $('input[name="action"]').val('edit')
        $('input[name="id"]').val(data.id)
        $('input[name="names"]').val(data.names)
        $('input[name="surnames"]').val(data.surnames)
        $('input[name="dni"]').val(data.dni)
        $('input[name="date_birthday"]').val(data.date_birthday)
        $('input[name="address"]').val(data.address)
        $('select[name="gender"]').val(data.gender.id)
        $('#modalView').modal('show');
        
        console.log(data)
    }).on('click', 'a[rel="delete"]', function(){
        let tr = tableCliente.cell( $(this).closest('td, li') ).index();
        let data = tableCliente.row(tr.row).data();

        let parameters = new FormData()
        parameters.append('action', 'delete')
        parameters.append('id', data.id)
        // $('#modalDelete').modal('show');

        Swal.fire({
            title: '¿Estás seguro de eliminar este cliente?',
            text: "Se eliminará a este cliente "+ data.names + ' ' + data.surnames,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            cancelButtonText: 'No',
            confirmButtonText: 'Sí'
          }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: window.location.pathname,
                    type: 'POST',
                    data: parameters,
                    dataType: 'json',
                    processData: false,
                    contentType: false
                })
                .done(function(data){
        
                    if (!data.hasOwnProperty('error')){
                        $('#modalDelete').modal('hide');
                        
                        tableCliente.ajax.reload();
                        // get_data_dataTable()
                        // location.reload()
                        return
                    }
                    mensajeError(data.error)
        
                })
                .fail(function(jqXHR, textStatus, errorThrown){
                    alert(textStatus + ' '+ errorThrown)
                })
            }
          })
              // alert('x')
          })

          //   console.log(parameters)



    /* Para cuando le doy click a un td, este codigo agrega una clase; 
        en este caso le agrega al texto de color rojo del td
    $('#data tbody').on( 'click', 'td', function () {
        var rowIdx = tableCliente
            .cell( this )
            .index().row;
     
        tableCliente
            .rows( rowIdx )
            .nodes()
            .to$()
            .addClass( 'text-danger' );
    } ); 
    */
})