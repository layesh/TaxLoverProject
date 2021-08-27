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

let keyboardSelected = 0;
let uploadSelected = 0;
let keyboardSelectedOnBtnFocus = 0;
let uploadSelectedOnBtnFocus = 0;

$("#keyboard-card").focusin(function () {
    $("#keyboard-footer").css("background", "#EDF9F2");
    keyboardSelected = 1;
});
$("#keyboard-card").focusout(function () {
    $("#keyboard-footer").css("background", "white");
    keyboardSelected = 0;
})

$("#upload-card").focusin(function () {
    $("#upload-footer").css("background", "#AFE3C3");
    uploadSelected = 1;
});
$("#upload-card").focusout(function () {
    $("#upload-footer").css("background", "#f2fbfc");
    uploadSelected = 0;
});

$("#choose-salary-input-submit-btn").mouseover(function () {
    if (keyboardSelected) {
        keyboardSelectedOnBtnFocus = 1;
    }

    if (uploadSelected) {
        uploadSelectedOnBtnFocus = 1;
    }
});
$("#choose-salary-input-submit-btn").mouseleave(function () {
    keyboardSelectedOnBtnFocus = 0;
    uploadSelectedOnBtnFocus = 0;
});

$(function () {
    Dropzone.options.salaryStatementUpload = {
        paramName: "file",
        maxFilesize: 2, // MB
        maxFiles: 1,
        addRemoveLinks: true,
        accept: function (file, done) {
            done();
        }
    };
});

