$(function () {
    $(".tab-link").click(function () {
        $(".tab-content").hide();
        $($(this).data("content")).show()
        $(".tab-link").removeClass("active");
        $(this).addClass("active")
    });
    // $("#uploadModal").modal();
    $("#addFileButton").click(function () {
        $("#uploadModal").modal();
    });
    fileManagerRender();
    studentListRender();
});
