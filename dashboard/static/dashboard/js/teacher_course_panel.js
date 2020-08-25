$(function () {
    $(".tab-link").click(function () {
        $(".tab-content").hide();
        $($(this).data("content")).show()
        $(".tab-link").removeClass("active");
        $(this).addClass("active")
    });
    fileManagerRender();
    $("#fileManager").show();
    studentListRender();
    dragUpload("upload_document");

    // new document upload ajax
    $("#documentUploadForm").submit(function (e) {
        addDocument();
    });

});


function addDocument() {
    let formData = new FormData(document.getElementById("documentUploadForm"));
    $.ajax({
        url: "http://127.0.0.1:8000/dashboard/lessons/files/020009/",
        type: "POST",
        data: new FormData($("#documentUploadForm")[0]),
        processData: false,
        contentType: false,
        dataType: "json",
        beforeSend: function (xhr, settings) {
            $("#uploadSubmit").text("در حال آپلود");
            $("#uploadLoading").show();
            $("#uploadFailedAlert").hide();
        },
        success: function (data, textStatus, xhr) {
            $("#uploadSubmit").text("ارسال جزوه");
            $("#uploadLoading").hide();
            $("#uploadModal").modal("hide");
            // render file manager with new data
            $("#fileManager").empty();
            fileManagerRender();
        },
        error: function (xhr, status, error) {
            $("#uploadSubmit").text("ارسال جزوه");
            $("#uploadLoading").hide();
            $("#uploadFailedAlert").show();
        }
    });
    e.preventDefault();

}