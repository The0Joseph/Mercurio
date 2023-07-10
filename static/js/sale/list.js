$(document).ready(function () {
    let tablaVentas = $('#data').DataTable({
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
                                    <a  class="btn btn-danger"><i class="fa-solid fa-trash"></i></a>
                                </div>
                                <div class="m-2">
                                    <a rel="details" class="btn btn-info"><i class="fa-solid fa-magnifying-glass"></i></a>
                                </div>
                                <div class="m-2">
                                    <a rel="edit" href="/tablas/venta/edit/${row.id}" class="btn btn-warning"><i class="fa-solid fa-pen"></i></a>
                                </div>
                            </div>`;
                }
            },
        ],
        initComplete: function(setting, json){
            // alert('Tablacargada')
        }
    })

    $('#data tbody')
    .on('click', 'a[rel="details"]', function () {
        let tr = tablaVentas.cell($(this).closest('td','li')).index();
        let data = tablaVentas.row(tr.row).data();
        // console.log(tr)
        // console.log(data)

        $('#tableDetalle').DataTable({
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
                    'action': 'search_detail_sale',
                    'id': data.id
                }, //Paramentros
                dataSrc: ""
            },
            columns: [
                {"data": "prod.name"},
                {"data": "prod.cat.name"},
                {"data": "price"},
                {"data": "cant"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                
                {
                    targets: [-1,-3],
                    class: 'text-center',
                    // orderable: false,
                    render: function(data, type, row){
                        return 'S/' + parseFloat(data).toFixed(2)
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    // orderable: false,
                    render: function(data, type, row){
                        return data;
                    }
                },
            ],
            initComplete: function(setting, json){
                // alert('Tablacargada')
            }
        })
        $('#modalDetalle').modal('show');
    })

});