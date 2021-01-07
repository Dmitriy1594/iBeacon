const SIGN_UP_URL = "http://0.0.0.0:5002/v1/sign_on/";

function create_account() {
    let username = document.getElementById("exampleEmail").value;
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
                // console.log(json);
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

const GET_AUTH_URL = "http://0.0.0.0:5002/auth";


function go_to_login_page() {
    window.location.replace(GET_AUTH_URL);
}

const TURN_ON_PI = "http://0.0.0.0:5002/v1/turn_on/";

function turn_on(name, alert_ = true) {
    // update data before start
    deploy_data_to_pi(name);

    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let json = JSON.parse(this.responseText);
            // console.log(json);
            if (alert_ === true) {
                alert(json.info_output);
            }
            // reload
            location.reload();
        }
    };

    xhr.open("POST", TURN_ON_PI, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    let data = JSON.stringify(
        {
            "name": name
        }
    );
    xhr.send(data);
}

const TURN_OFF_PI = "http://0.0.0.0:5002/v1/turn_off/";

function turn_off(name, alert_= true, reload= true) {
    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let json = JSON.parse(this.responseText);
            // console.log(json);
            if (alert_ === true) {
                alert(json.info_output);
            }
            // update data
            // deploy_data_to_pi(name);
            // reload
            if (reload === true) {
                location.reload();
            }
        }
    };

    xhr.open("POST", TURN_OFF_PI, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    let data = JSON.stringify(
        {
            "name": name
        }
    );
    xhr.send(data);
}


const NULL_CV = "http://0.0.0.0:5002/v1/set_null_count_visitors/";

function set_null_count_visitors(name,) {
    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let json = JSON.parse(this.responseText);
            // console.log(json);
            // location.reload();
            document.getElementById(id).innerHTML = "Count Visitors: 0";
        }
    };

    xhr.open("POST", NULL_CV, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    let data = JSON.stringify(
        {
            "name": name
        }
    );
    xhr.send(data);
}


const UPDATE_NP_BY_ID = "http://0.0.0.0:5002/v1/update_by_id/";

function save_changes(id, name, price, reload= true) {
    let new_name = document.getElementById(name).value;
    // parseFloat("554,20".replace(",", "."))
    let new_price = parseFloat(document.getElementById(price).value);

    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let json = JSON.parse(this.responseText);
            // console.log(json);
            // update data on PI.
            // reload
            if (reload === true) {
                location.reload();
            }

            set_null_count_visitors(json.name);
            // location.reload();
        }
    };

    xhr.open("POST", UPDATE_NP_BY_ID, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    let data = JSON.stringify(
        {
            "id": id,
            "name": new_name,
            "price": new_price
        }
    );
    xhr.send(data);
}


const DEPLOY_DATA_TO_PI = "http://0.0.0.0:5002/v1/deploy_data_json/";


function deploy_data_to_pi(name, reload= true) {
    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let json = JSON.parse(this.responseText);
            // console.log(json);
            // reload
            // location.reload();
            if (reload === true) {
                location.reload();
            }
        }
    };

    xhr.open("POST", DEPLOY_DATA_TO_PI, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    let data = JSON.stringify(
        {
            "name": name
        }
    );
    xhr.send(data);
}


// function save_changes_active(id, name, price) {
//     save_changes(id, name, price, false);
//     deploy_data_to_pi(document.getElementById(name).value);
//     turn_off(document.getElementById(name).value, false, false)
//     turn_on(name, false)
// }

const SETTINGS_DEPLOY_URL = "http://0.0.0.0:5002/v1/deploy_settings_json/"


function update_settings(name, alert_) {
    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let json = JSON.parse(this.responseText);
            // console.log(json);
            if (alert_ === true) {
                alert("New settings deployed!");
            }
            // update data
            // deploy_data_to_pi(name);
            // reload
        }
    };

    xhr.open("POST", SETTINGS_DEPLOY_URL, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    let data = JSON.stringify(
        {
            "name": name
        }
    );
    xhr.send(data);
}

// Update count_visitors
const CV_URL = "http://0.0.0.0:5002/v1/get_pi_by_name/"

function get_count_visitors_by_name(product_name) {
    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let json = JSON.parse(this.responseText);
            let id = "count_visitors_" + json.uuid;
            // console.log(json);
            // if (alert_ === true) {
            //     alert("New settings deployed!");
            // }
            // update data
            // deploy_data_to_pi(name);
            // reload
            // plot(json)
            document.getElementById(id).innerHTML = "Count Visitors: " + json.count_visitors;
        }
    };

    xhr.open("POST", CV_URL, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    let data = JSON.stringify(
        {
            "name": product_name
        }
    );
    xhr.send(data);
}

// PLOTS

const PLOTS_URL = "http://0.0.0.0:5002/v1/get_locate_data_by_name/"

function get_locate_data_by_name(product_name) {
    get_count_visitors_by_name(product_name);

    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let json = JSON.parse(this.responseText);
            // console.log(json);
            // if (alert_ === true) {
            //     alert("New settings deployed!");
            // }
            // update data
            // deploy_data_to_pi(name);
            // reload
            plot(json);
        }
    };

    xhr.open("POST", PLOTS_URL, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    let data = JSON.stringify(
        {
            "name": product_name
        }
    );
    xhr.send(data);
}

// https://codepen.io/Dmitriy1594/pen/gOwKpxe
// Polar chart
function plot(locate_data) {
    let ld = locate_data;

    // var ts = new Date(ld["date"] * 1000);

    var data = {
        datasets: [{
            data: [
                ld.meters,
            ],
            backgroundColor: [
                "RGBA(40,167,69,0.5)",
            ],
            label: 'Beacon' // for legend
        }],
        labels: [
            ld["device_name"]
        ]
    };
    var ctx = $("#chart-area");
    new Chart(ctx, {
        data: data,
        type: 'polarArea'
    });
}



const PLOT_URL = "http://0.0.0.0:5002/v1/get_data_plot_by_product/"

function get_data_plot_by_product(product_name) {
    get_count_visitors_by_name(product_name);

    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let json = JSON.parse(this.responseText);
            // console.log(json);
            // if (alert_ === true) {
            //     alert("New settings deployed!");
            // }
            // update data
            // deploy_data_to_pi(name);
            // reload
            plots(json);
        }
    };

    xhr.open("POST", PLOT_URL, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    let data = JSON.stringify(
        {
            "product_name": product_name
        }
    );
    xhr.send(data);
}

function plots(data) {
    //    get data
    var ctx = $("#chart-area-all");
    new Chart(ctx, {
        data: data,
        type: 'polarArea'
    });
}

