var modal;

$(document).ready(function () {
    // Get the modal
    modal = document.getElementById('myModal');

// Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
    modal.style.display = "block";

// When the user clicks on <span> (x), close the modal
    span.onclick = function () {
        modal.style.display = "none";
    }

// When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

});

function goToPlayStore() {
    modal.style.display = "none";
    window.open('https://play.google.com/store/apps/details?id=com.piresereliquias.poketctrl');

}

