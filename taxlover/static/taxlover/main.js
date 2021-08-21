$(function () {
    $("#datepicker").datepicker({
        changeMonth: true,
        changeYear: true,
        yearRange: '1950:2030',
        dateFormat: 'dd/mm/yy'
    });
});

$(document).ready(function(){
    $(".dropdown").hover(function(){
        var dropdownMenu = $(this).children(".dropdown-menu");
        if(dropdownMenu.is(":visible")){
            dropdownMenu.parent().toggleClass("open");
        }
    });
});

// Current it doesn't work. Need find a way of working.
// Feature: Expanding a accordion item in the left column will collapse open item in the right side.
// Only one open item can be present in a page at any given time.
$('#accordionExample').on('show.bs.collapse', function () {
    $('#accordionExample1 .in').collapse('hide');
});


