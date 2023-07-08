let tablaProductos;
let verts = {
    items : {
        cli: '',
        date_joined : '',
        subtotal : 0.00,
        iva : 0.00,
        total : 0.00,
        productos: []
    },
    calculate_invoice:function() {
        let subtotal = 0.00;
        let iva = $('input[name="iva"]').val();
        $.each(this.items.productos, function(pos, dic){
            // console.log(pos)
            // console.log(dic)
            dic.subtotal = dic.cant * parseFloat(dic.pvp);
            subtotal += dic.subtotal;
        })
        
        this.items.subtotal = subtotal  // Guardando la suma del subtotal en this.items.subtotal

        this.items.iva = this.items.subtotal * iva // Multiplicando el subtotal almacena por el iva

        this.items.total = this.items.subtotal + this.items.iva //Sumando el Subtotal + iva almacenados para sacar el total

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2))
        $('input[name="iva_calculado"]').val(this.items.iva.toFixed(2))
        $('input[name="total"]').val(this.items.total.toFixed(2))
    },
    list: function(){
        this.calculate_invoice();
        tablaProductos = $('#data').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            paging: true,
            data: verts.items.productos,
            columns: [
                {'data': 'name'},
                {'data': 'name'},
                {'data': 'cat.name'},
                {'data': 'pvp'},
                {'data': 'cant', width: "130px"},
                {'data': 'subtotal'},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function(data, type, row){
                        return `<a href="#" rel="remove" class="btn btn-danger"><i class="fa-solid fa-trash"></i></a>`;
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function(data, type, row){
                        return 'S/' + parseFloat(data).toFixed(2)
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function(data, type, row){
                        return '<input type="text" name="cant" class="form-control input-sm text-center" autocomplete="off" value="'+data+'">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function(data, type, row){
                        return 'S/' + parseFloat(data).toFixed(2)
                    }
                },
            ],
            rowCallback: function( row, data ) {
                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 1000000,
                    step: 1,
                })
            }
        });
    },
    add: function(item){
        this.items.productos.push(item);
        this.list();
    }
}

$(document).ready(function(){

    $('.select2').select2({
        theme:'bootstrap4',
        language: 'es'
    })

    new tempusDominus.TempusDominus(document.getElementById('id_date_joined'),{
        localization: {
            locale: 'es',
            format: 'yyyy-MM-dd', //dd/MM/yyyy antes
        },
        display: {
            components: {
                clock: false,
            },
            theme: 'auto'
        }
    });

    $("#id_iva").TouchSpin({
        min: 0.0,
        max: 100,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    }).on('change',function () {
        verts.calculate_invoice()
    })
    .val(0.18);

    $("select[name='searchProductos']").select2({
        theme: 'bootstrap4',
        language: 'es',
        selectOnClose: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            delay: 250,
            data: function(params){
                // console.log(params)
                let queryParameters ={
                    term: params.term,
                    action: 'searchProductos'
                }
                return queryParameters
            },
            processResults: function (data) {
                // console.log(data)
                return {
                    results: data
                };
            
            },
          },
          placeholder: 'Buscar alguna categoria',
          minimumInputLength: 1,
    }).on('select2:select', function(e){
        // console.log(e.params)
        let data  = e.params.data;
        data.cant = 1; 
        data.subtotal = 0.00; 
        // verts.items.productos.push(data)
        // console.log('verts.items.productos');
        // console.log(verts.items);
        verts.add(data)
        // verts.list();

        $(this).val('').trigger('change.select2');

        setTimeout(
            ()=>{
                    $(this).select2("open")
                }, 500)
    })

    $('.btndeleteall').on('click',function () {
        if(verts.items.productos.length === 0) return false;
        alerta_Eliminar('a todos los productos', function () {
            verts.items.productos = [];
            verts.list()
        });
    })

    $('#data tbody')
    .on('click', 'a[rel="remove"]', function () {
        let tr = tablaProductos.cell($(this).closest('td','li')).index();
        verts.items.productos.splice(tr.row, 1);
        verts.list();
    })
    .on('change keyup', 'input[name="cant"]', function(){
      let cant = parseInt($(this).val())  
      let tr = tablaProductos.cell($(this).closest('td','li')).index(); // obtengo el numero de la fila donde se esta haciendo un change(dando click en el botón de añadir un producto mas o restarlo)
      console.log(tr)
      verts.items.productos[tr.row].cant = cant
      verts.calculate_invoice();
      // selecciona la sexta celda (td:eq(5)) en la fila correspondiente a "tr.row" en la tabla "tablaProductos".
      $('td:eq(5)', tablaProductos.row(tr.row).node()).html('S/ ' + verts.items.productos[tr.row].subtotal.toFixed(2));
    })



    $('form').on('submit', function (e) {
        e.preventDefault();


        // /Verificando si productos está vacio
        if(verts.items.productos.length === 0){
            message_error('Se nesecita tener productos')
            return false
        }

        // Asignando datos
        verts.items.date_joined = $('input[name="date_joined"]').val();
        verts.items.cli = $('select[name="cli"]').val();

        let parameters = new FormData()
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('verts', JSON.stringify(verts.items)); // verts.items nesecita ser tranformado a json para enviarlo al view


        submit_ajax(window.location.pathname, parameters, function () {
            location.href = '/tables/cliente/'; // Redireciona a la url almacenada en la variable list_url
        })

        // console.log(parameters)
    });

    verts.list()
})