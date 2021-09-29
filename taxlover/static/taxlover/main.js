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

// $(function () {
//     Dropzone.options.salaryStatementUpload = {
//         paramName: "file",
//         maxFilesize: 2, // MB
//         maxFiles: 1,
//         acceptedFiles: "application/pdf,image/jpeg,image/jpg,image/png",
//         accept: function (file, done) {
//             done();
//         },
//         init: function () {
//             this.on("success", function (file, response) {
//                 if (response['has_total_annual_payment'] === true) {
//                     window.location.href = '/salary-info?info=True'
//                 } else {
//                     document.getElementById('error-text').innerHTML = "Sorry, we can't extract a single information from your document.";
//                     document.getElementById('upload-error').style.display = "";
//                     document.getElementById('upload-again-btn').style.display = "";
//                     document.getElementById('upload-progress').style.display = "none";
//                     document.getElementById('spinner').style.display = "none";
//                     this.removeAllFiles();
//                 }
//             });
//             this.on("error", function (file, error) {
//                 document.getElementById('error-text').innerHTML = error;
//                 document.getElementById('upload-error').style.display = "";
//                 document.getElementById('upload-again-btn').style.display = "";
//                 document.getElementById('salary-statement-upload').style.display = "none";
//                 this.removeAllFiles();
//             });
//             this.on("processing", function (file) {
//                 document.getElementById('salary-statement-upload').style.display = "none";
//                 document.getElementById('upload-progress').style.display = "";
//                 document.getElementById('spinner').style.display = "";
//             });
//         }
//     };
// });

function addCommas(nStr) {
    nStr += '';
    x = nStr.split('.');
    x1 = x[0];
    x2 = x.length > 1 ? '.' + x[1] : '';
    var rgx = /(\d+)(\d{3})/;
    while (rgx.test(x1)) {
        x1 = x1.replace(rgx, '$1' + ',' + '$2');
    }
    return x1 + x2;
}

function formatToTwoDecimalPlaces(nStr) {
    if (isNaN(nStr)) {
        return nStr;
    }

    nStr += '';
    let x = nStr.split('.');
    let x1 = x[0];
    let x2 = x.length > 1 ? '.' + x[1] : '';

    if (x1 !== '') {
        return parseFloat(nStr).toFixed(2);
    } else {
        return nStr;
    }
}

function removeCommas(nStr) {
    if (typeof nStr === 'undefined') {
        return '';
    }
    return nStr.replace(/\,/g, '');
}

function hasInputValue(id) {
    let input = $("#" + id);

    if(input.val().length > 0) {
        return true;
    } else {
        return false;
    }
}

function parseDecimalInputValue(id) {
    let value = parseFloat(removeCommas(document.getElementById(id).value));

    if (isNaN(value)) {
        return 0;
    } else {
        return value;
    }
}

function setTextBoxValue(id, value) {
    document.getElementById(id).value = value;
}

function setLabelValue(id, value) {
    document.getElementById(id).innerHTML = value;
}

function getTextBoxValue(id) {
    return removeCommas(document.getElementById(id).value);
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})

