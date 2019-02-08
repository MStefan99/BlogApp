function add_to_favourites(post_id) {
    let xhttp = new XMLHttpRequest();
    let button = document.getElementById("post-save");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("post-save").innerHTML =
            "Remove  from favourites";
       }
    };
    xhttp.open("GET", "/add_post/?post=" + post_id, true);
    xhttp.send();
    button.onclick = function() { remove_from_favourites(post_id) };
}

function remove_from_favourites(post_id) {
    let xhttp = new XMLHttpRequest();
    let button = document.getElementById("post-save");
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("post-save").innerHTML =
            "Save to favourites";
       }
    };
    xhttp.open("GET", "/del_post/?post=" + post_id, true);
    xhttp.send();
    button.onclick = function() { add_to_favourites(post_id) };
}