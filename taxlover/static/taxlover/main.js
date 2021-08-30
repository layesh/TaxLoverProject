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
        acceptedFiles: "application/pdf,image/jpeg,image/jpg,image/png",
        accept: function (file, done) {
            done();
        },
        init: function () {
            this.on("success", function (file, response) {
                if (response['has_total_annual_payment'] === true) {
                    window.location.href = '/salary-info'
                } else {
                    document.getElementById('error-text').innerHTML = "Sorry, we can't extract a single information from your document.";
                    document.getElementById('upload-error').style.display = "";
                    document.getElementById('upload-again-btn').style.display = "";
                    document.getElementById('upload-progress').style.display = "none";
                    document.getElementById('spinner').style.display = "none";
                    this.removeAllFiles();
                }
            });
            this.on("error", function (file, error) {
                document.getElementById('error-text').innerHTML = error;
                document.getElementById('upload-error').style.display = "";
                document.getElementById('upload-again-btn').style.display = "";
                document.getElementById('salary-statement-upload').style.display = "none";
                this.removeAllFiles();
            });
            this.on("processing", function (file) {
                document.getElementById('salary-statement-upload').style.display = "none";
                document.getElementById('upload-progress').style.display = "";
                document.getElementById('spinner').style.display = "";
            });
        }
    };
});

