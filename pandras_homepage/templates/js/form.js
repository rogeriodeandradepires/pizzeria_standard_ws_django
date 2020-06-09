const firebaseConfig = {
    apiKey: "AIzaSyB-wRbzMD6zI8gXGR_M_bc_GoKvzr2m1LM",
    authDomain: "brpandras.firebaseapp.com",
    databaseURL: "https://brpandras.firebaseio.com",
    projectId: "brpandras",
    storageBucket: "brpandras.appspot.com",
    messagingSenderId: "225510747607",
    appId: "1:225510747607:web:8f7f1a7548bbc57f"
};

firebase.initializeApp(firebaseConfig);

$( document ).ready(function() {
    $(":button").bind('keyup mouseup', function () {
        this.blur();
    });
});

function sendMessage() {

    var isEmpty = false;

    // swal({
    //     title: "Sucesso",
    //     text: "Recebemos sua Mensagem e entraremos em contato assim que possível. Obrigado pelo contato.",
    //     icon: "success",
    // }).then((value) => {
    //
    // });

    var firebaseRef = firebase.database().ref('mensagem');
    var campos = [];
    campos.push(document.getElementById('inputName').value);
    campos.push(document.getElementById('inputEmail').value);
    campos.push(document.getElementById('inputPhone').value);
    campos.push(document.getElementById('inputCity').value);
    campos.push(document.getElementById('inputState').value);
    campos.push(document.getElementById('inputDescription').value);
    campos.push(document.getElementById('inputMonths').value);

    campos.forEach(function (valor) {
        // alert("valor="+valor);
        if (checkEmptyness(valor)) {
            isEmpty = true;
            // alert("vazio="+valor);
        }
    });

    var d = new Date();

    if (!isEmpty) {
        if (validateEmail(campos[1])) {
            firebaseRef.push().set({
                "nome": campos[0],
                "email": campos[1],
                "telefone": campos[2],
                "cidade": campos[3],
                "estado": campos[4],
                "descricao": campos[5],
                "prazo": campos[6],
                "dataEnvio":d.toDateString()
            }).then(function () {

                document.getElementById('inputName').value = "";
                document.getElementById('inputEmail').value = "";
                document.getElementById('inputPhone').value = "";
                document.getElementById('inputCity').value = "";
                document.getElementById('inputState').value = "";
                document.getElementById('inputDescription').value = "";
                document.getElementById('inputMonths').value = "";

                swal({
                    title: "Sucesso",
                    text: "Recebemos sua Mensagem e entraremos em contato assim que possível. Obrigado pelo contato.",
                    icon: "success",
                }).then((value) => {
                    window.close();
                });
            }, function (error) {

                document.getElementById('inputName').value = "";
                document.getElementById('inputEmail').value = "";
                document.getElementById('inputPhone').value = "";
                document.getElementById('inputCity').value = "";
                document.getElementById('inputState').value = "";
                document.getElementById('inputDescription').value = "";
                document.getElementById('inputMonths').value = "";

                swal({
                    title: "Erro",
                    text: "Não foi possível salvar sua Mensagem. Por favor, envie um email para contato@pandras.com.br informando este erro: " + error.message,
                    icon: "error",
                }).then((value) => {
                });
            });
        } else {
            swal({
                title: "Erro",
                text: "E-mail inválido! Por favor confira seu endereço de E-mail.",
                icon: "error",
            }).then((value) => {
            });
        }

    } else {
        emptyFieldMessage();
    }

}

function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

function changeStatus() {
    document.getElementById('btn_send').bind('keyup mouseup', function () {
        // alert("changed");
    });
    // document.getElementById('btn_send').hideFocus(true); //.setAttribute("aria-pressed",false);
}

function checkEmptyness(value) {
    if (value == "") {
        return true;
    } else {
        return false;
    }
}

function emptyFieldMessage() {
    swal({
        icon: 'error',
        title: 'Atenção!',
        text: 'Preencha todos os campos!',
        dangerMode: true,
        onOpen: () => {
            // swal.showLoading()
            // timerInterval = setInterval(() => {
            //     // swal.getContent().querySelector('strong')
            //     //     .textContent = userClass//swal.getTimerLeft()
            // }, 100)
        },
        onClose: () => {
            // clearInterval(timerInterval)
        }
    }).then((result) => {
        if (
            result.dismiss === swal.DismissReason.timer
        ) {
            console.log('I was closed by the timer')
        }
    })
}
