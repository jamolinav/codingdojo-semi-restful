//import { data } from "jquery"
//const { data } = require("jquery")


$(document).ready(function() {
    
    $("#email").focusout(checkEmail);

    $('#dtBasicExample').DataTable({
        "pagingType": "simple_numbers", // "simple" option for 'Previous' and 'Next' buttons only
        "language": {
            "url": "//cdn.datatables.net/plug-ins/9dcbecd42ad/i18n/Spanish.json"
            }
      });
    $('.dataTables_length').addClass('bs-select');

})

function checkEmail(){
    console.log('lost focus email')
    if ($('#email').val() == "") {
        return
    }

    var data = $("#formRegister").serialize()
    $.ajax({
        method : "POST",
        url : "checkEmail/",
        data : data,
        dateaType : "JSON"
    })
    .done (function(response){
        var size = Object.keys(response["errors"]).length
        if ( size > 0 ) {
            console.log(response["errors"])
            $('#messages').html(JSON.stringify(response["errors"]));
        } else {
            console.log("Correo valido")
        }

    })
}