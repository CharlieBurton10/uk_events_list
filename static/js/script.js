/*
    jQuery for MaterializeCSS initialization
*/

$(document).ready(function () {
    $(".sidenav").sidenav({edge: "right"});
});





/*
    vanilla JavaScript for MaterializeCSS initialization
*/

// document.addEventListener('DOMContentLoaded', function () {
//     let sidenavs = document.querySelectorAll(".sidenav");
//     let sidenavsInstance = M.Sidenav.init(sidenavs, {edge: "right"});
// });

let likes = 0;
$(document).ready(function () {
  // ajax to get current likes
  // let likes from server are 10
  // assign the current likes to variable
  likes = 1;
  setLikes(likes);
});

$("body").on("click", ".likeBtn", function () {
  // ajax to post a current likes
  // in success add increment to likes
  likes++;
  setLikes(likes);
});

function setLikes(count) {
  $(".totalLikes").text(count);
}