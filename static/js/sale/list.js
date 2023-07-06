$(document).ready(function(){

    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        paging: true,
    });

    $('.select2').select2({
        theme:'bootstrap4',
        language: 'es'
    })
    // $('#id_date_joined').tempusDominus();

    // const picker = new tempusDominus
    // .TempusDominus(document.getElementById('id_date_joined'));

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
        min: 0,
        max: 100,
        step: 0.1,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '%'
    });

})