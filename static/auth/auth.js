const SIGN_IN_URL = "http://0.0.0.0:5002/v1/sign_in/";

function auth() {
    let username = document.getElementById("inputEmail").value.toLowerCase();
    let password = document.getElementById("inputPassword").value;

    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let json = JSON.parse(this.responseText);
            console.log(json);
            // redirect
            go_to_menu(json)
        }
    };

    xhr.open("POST", SIGN_IN_URL, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    let data = JSON.stringify({"login": username, "password": password});
    xhr.send(data);
}

const GET_MENU_URL = "http://0.0.0.0:5002/menu"

//?id=0&login=dromakin

function go_to_menu(json) {
    window.location.replace(GET_MENU_URL + "?id=" + json.id + "&" + "login=" + json.login);
}

const SIGN_UP_URL = "http://0.0.0.0:5002/register";

function go_to_register() {
    window.location.replace(SIGN_UP_URL);
}
