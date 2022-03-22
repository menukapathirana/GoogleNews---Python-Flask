$(document).ready(function () {
    $(".slide-toggle").click(function () {
        $(".boxfeedback").animate({
            width: "toggle"
        });
    });



    $('#btnyes').bind('click', function () {
        $.getJSON('/background_feedbackYes', {
            feedbackYes: 'Yes',
        }, function (data) {
            $("#result").text(data.result);
            return false;
        });
        $(".slide-toggle").hide()
        $(".boxfeedback").hide()

    });

        $('#btnno').bind('click', function () {
        $.getJSON('/background_feedbackNo', {
            feedbackNo: 'No',
        }, function (data) {
            $("#result").text(data.result);
            return false;
        });
        $(".slide-toggle").hide()
        $(".boxfeedback").hide()

    });


});


// window.onload
window.onload = function () {
    $(".boxfeedback").hide()
};



