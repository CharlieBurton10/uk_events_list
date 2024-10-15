/*jshint esversion: 11 */
$(document).ready(function () {
        let eventId;
    $(".sidenav").sidenav({edge: "right"});
    $('.collapsible').collapsible();
    $("select").formSelect();
    $('.modal').modal();
    $('.delete-btn').click(function(){
        eventId = $(this).data('event-id');
    });
    $('#confirm-delete').click(function(){
    $('#confirm-delete').attr("href", "/delete_event/" + eventId);});
    validateMaterializeSelect();
    function validateMaterializeSelect() {
        let classValid = { "border-bottom": "1px solid #4caf50", "box-shadow": "0 1px 0 0 #4caf50" };
        let classInvalid = { "border-bottom": "1px solid #f44336", "box-shadow": "0 1px 0 0 #f44336" };
        if ($("select.validate").prop("required")) {
            $("select.validate").css({ "display": "block", "height": "0", "padding": "0", "width": "0", "position": "absolute" });
        }
        $(".select-wrapper input.select-dropdown").on("focusin", function () {
            $(this).parent(".select-wrapper").on("change", function () {
                if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () { })) {
                    $(this).children("input").css(classValid);
                }
                });
        }).on("click", function () {
            if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
                $(this).parent(".select-wrapper").children("input").css(classValid);
            } else {
                $(".select-wrapper input.select-dropdown").on("focusout", function () {
                    if ($(this).parent(".select-wrapper").children("select").prop("required")) {
                        if ($(this).css("border-bottom") != "1px solid rgb(76, 175, 80)") {
                            $(this).parent(".select-wrapper").children("input").css(classInvalid);
                        }
                    }
                });
            }
        });
    }
});
document.querySelectorAll('button.like').forEach(bttn=>{
    bttn.addEventListener('click',function(e){
        this.nextElementSibling.textContent=Number( this.nextElementSibling.textContent ) + 1;
        bttn.disabled = true;
    });
  })

const getLike = document.querySelector('.like');
const getinterested = document.querySelector('.interested');

let like = 0;

increaseLike = () => {
like ++
getinterested.innerHTML = `${like}`
}
    
likeClick = () => {
increaseLike()
}