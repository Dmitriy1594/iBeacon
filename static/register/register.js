const SIGN_UP_URL = "http://0.0.0.0:5002/v1/sign_on/";

function create_account() {
    let username = document.getElementById("exampleEmail").value.toLowerCase();
    let password1 = document.getElementById("examplePassword").value;
    let password2 = document.getElementById("examplePasswordRep").value;

    if (password1 !== password2) {
        console.log("passwords are not the same!")
        alert("passwords are not the same!")
    } else {
        let xhr = new XMLHttpRequest();

        xhr.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                let json = JSON.parse(this.responseText);
                console.log(json);
                // redirect
                go_to_login_page(json)
            }
        };

        xhr.open("POST", SIGN_UP_URL, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        let data = JSON.stringify({"login": username, "password": password1});
        xhr.send(data);
    }
}

const GET_AUTH_URL = "http://0.0.0.0:5002/auth"

function go_to_login_page() {
    window.location.replace(GET_AUTH_URL);
}

const GET_PASSWORD = "http://0.0.0.0:5002/v1/get_example_password"


function get_example_password() {
    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let json = JSON.parse(this.responseText);
            // console.log(json);
            // if (alert_ === true) {
            //     alert("New settings deployed!");
            // }
            // plot(json)
            // alert("Example password:\n" + json.example_password);
            document.getElementById("example_password").innerHTML = "Example password: " + json.example_password;
        }
    };

    xhr.open("GET", GET_PASSWORD, true);
    // xhr.setRequestHeader("Content-Type", "application/json");
    // let data = JSON.stringify(
    //     {
    //         "name": product_name
    //     }
    // );
    xhr.send();
}
