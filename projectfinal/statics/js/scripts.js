$(document).ready(function () {
    $(".danger").on("click", function (e) {
        e.preventDefault();
        console.log('Shallow!')
    });
});


swal({
    title: "¿Estás seguro de borrar?",
    text: "Una vez borrado el registro ya no podrás recuperarlo",
    icon: "Ojito!",
    buttons: true,
    dangerMode: true,
})
    .then((willDelete) => {
        if (willDelete) {
            swal("De acuerdo, el registro ha sido eliminado", {
                icon: "success",
            });
        } else {
            swal("El registro sigue en la BBDD");
        }
    });