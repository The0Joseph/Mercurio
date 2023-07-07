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
            console.log(pos)
            console.log(dic)
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
        $('#data').DataTable({
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
                {'data': 'cant'},
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
                        return '<input type="text" name="cant" class="form-control" autocomplete="off" value="'+data+'">';
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
            ]
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

        $(this).val('').trigger('change.select2')
    })
})