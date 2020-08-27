$(function () {
    $(".tab-link").click(function () {
        $(".tab-content").hide();
        $($(this).data("content")).show()
        $(".tab-link").removeClass("active");
        $(this).addClass("active")
    });
    fileManagerRender($("#courseCode").val());
    $("#fileManager").show();
    studentListRender($("#courseCode").val());

    // add upload zone to modal with name = "upload_document"
    dragUpload("upload_document");


    // configure modal for edit & delete
    $("#documentUploadForm").submit(function (e) {
        e.preventDefault();
        if (uploadModalAddOrEditStatus.val() === "add") {
            if ($("#dropUploadFiles")[0].files.length === 0) $("#validationForFile").show();
            else {
                addDocumentAjax();
                $("#validationForFile").hide()
            }
        } else {
            editDocumentAjax();
        }
    });
});

