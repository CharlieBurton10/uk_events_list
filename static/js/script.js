/*jshint esversion: 11 */
$(document).ready(function () {
    $(".sidenav").sidenav({edge: "right"});
    $("select").formSelect();
});

document.querySelectorAll('button.like').forEach(bttn=>{
    bttn.addEventListener('click',function(e){
      this.nextElementSibling.textContent=Number( this.nextElementSibling.textContent ) + 1;
    });
  })

const getLike = document.querySelector('.like');
const getLikeNum = document.querySelector('.likeNum');

let like = 0;

increaseLike = () => {
like ++
getLikeNum.innerHTML = `${like}`
}
    
likeClick = () => {
increaseLike()
}
  