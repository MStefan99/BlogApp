function post_favourites(link) {
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("post-save").innerHTML =
            this.responseText;
       }
    };
    xhttp.open("GET", link, true);
    xhttp.send();
}