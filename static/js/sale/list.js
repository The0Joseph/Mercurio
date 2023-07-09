$(document).ready(function () {
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
                'action': 'salesData'
            }, //Paramentros
            dataSrc: ""
        },
        columns: [
            {"data": "cli.names"},
            {"data": "date_joined"},
            {"data": "subtotal"},
            {"data": "iva"},
            {"data": "total"},
            {"data": "total"},
        ],
        columnDefs: [
            
            {
                targets: [0],
                // class: 'text-center',
                orderable: false,
                render: function(data, type, row){
                    return `<div class="p-2">
                                <div class="ml-3 d-inline-block align-middle">
                                    <h5 class="mb-0"><p href="#" class="text-dark d-inline-block">${row.cli.names} ${row.cli.surnames}</p></h5>
                                </div>
                            </div>`;
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function(data, type, row){
                    return `<div class="d-flex">
                                <div class="m-2">
                                    <a href="" class="btn btn-info"><i class="fa-solid fa-magnifying-glass"></i></a>
                                </div>
                                <div class="m-2">
                                    <a href="" class="btn btn-danger"><i class="fa-solid fa-trash"></i></a>
                                </div>
                            </div>`;
                }
            },
        ],
        initComplete: function(setting, json){
            // alert('Tablacargada')
        }
    })

});