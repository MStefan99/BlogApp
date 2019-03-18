"use strict";

function add_to_favourites(post_id) {
  var xhttp = new XMLHttpRequest();
  var button = document.getElementById("post-save");

  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("post-save").innerHTML = "Remove  from favourites";
    }
  };

  xhttp.open("POST", "/add_post/", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("post=" + post_id);

  button.onclick = function () {
    remove_from_favourites(post_id);
  };
}

function remove_from_favourites(post_id) {
  var xhttp = new XMLHttpRequest();
  var button = document.getElementById("post-save");

  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("post-save").innerHTML = "Save to favourites";
    }
  };

  xhttp.open("POST", "/del_post/", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("post=" + post_id);

  button.onclick = function () {
    add_to_favourites(post_id);
  };
}
//# sourceMappingURL=favourites.js.map