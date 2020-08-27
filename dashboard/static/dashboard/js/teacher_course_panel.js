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

});

