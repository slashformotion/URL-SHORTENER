$(document).ready(function () {

    // Check for click events on the navbar burger icon
    $(".navbar-burger").click(function () {

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");

    });

    
}); 
function copyToClipboard(element) {
    var $temp = $("<input>");
    $("body").append($temp);
    console.log(element);
    $temp.val(element);
    $temp.select();
    document.execCommand("copy");
    $temp.remove();
}