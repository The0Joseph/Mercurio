$(document).ready(function(){

    $('#data').DataTable({
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
            {"data": "name"},
            {"data": "figura"},
            // {"data": "pvp"},
            {"data": "name"},
        ],
        columnDefs: [
            
            {
                // responsivePriority: 1,
                targets: [0],
                // class: 'text-center',
                orderable: false,
                render: function(data, type, row){
                    return `<div class="p-2">
                                <img src="${row.figura}" alt="" width="70" class="img-fluid rounded shadow-sm" />
                                <div class="ml-3 d-inline-block align-middle">
                                    <h5 class="mb-0"><p href="#" class="text-dark d-inline-block">${data}</p></h5><span class="text-muted font-weight-normal font-italic d-block">${ row.status }</span>
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
                                    <a href="edit/${row.id}" class="btn btn-warning"><i class="fa-solid fa-pen-to-square"></i></a>
                                </div>
                                <div class="m-2">
                                    <a href="delete/${row.id}" class="btn btn-danger"><i class="fa-solid fa-trash"></i></a>
                                </div>
                            </div>`;
                }
            },
        ],
        initComplete: function(setting, json){
            // alert('Tablacargada')
        }
    })

})