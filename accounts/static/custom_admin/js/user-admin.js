$(document).ready(function () {
    $("#sendPass").click(function () {
        $.ajax({
            type: "POST",
            url: "/signin/forget-password/",
            dataType: "json",

            data: {
                phone_number: $(this).attr("value"),
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
            },
            beforeSend: function (xhr, settings) {
                $("#sendPass").prop("disabled", true);
            },
            success: function (data) {
                alert(data.success);
            },
            error: function ($xhr) {
                var data = $xhr.responseJSON;
                alert(data.error);
            },
        });
    });
});