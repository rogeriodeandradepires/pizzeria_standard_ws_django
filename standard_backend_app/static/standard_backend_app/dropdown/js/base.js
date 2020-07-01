(function ($) {
    alert('antes');
    alert('antes 2');
    // var selectField = $('#delivery');
    var selectField = document.getElementById('id_delivery');
    // console.log($('#delivery').attr('id'));
    alert(document.getElementById('id_delivery').val);
    alert('antes 3');
    // var verified = $('.abcdefg');
    var verified = document.getElementsByClassName('abcdefg');

    alert('antes 4');

    function toggleVerified(value) {
        alert('mudou tipo de retirada')
        if (value === 'Entrega') {
            verified.show();
        } else {
            verified.hide();
        }
    }

    // show/hide on load based on pervious value of selectField
    toggleVerified(selectField.val());

    // show/hide on change
    selectField.change(function () {
        toggleVerified($(this).val());
    });
    alert('depois');
})(django.jQuery);

// (function ($) {
//     alert('antes');
//     $(function () {
//         alert('antes 2');
//         var selectField = $('#id_delivery'),
//             verified = $('.abcdefg');
//
//         alert('antes 3');
//
//         function toggleVerified(value) {
//             alert('mudou tipo de retirada')
//             if (value === 'Entrega') {
//                 verified.show();
//             } else {
//                 verified.hide();
//             }
//         }
//
//         // show/hide on load based on pervious value of selectField
//         toggleVerified(selectField.val());
//
//         // show/hide on change
//         selectField.change(function () {
//             toggleVerified($(this).val());
//         });
//     });
//     alert('depois');
// })(django.jQuery);

// (function($) { // < start of closure
//     // within this block, $ = django.jQuery
//     $(document).ready(function() {
//         alert();
//     });
// })(django.jQuery);
