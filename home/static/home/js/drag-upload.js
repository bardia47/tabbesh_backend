function dragUpload(inputName = "") {

    let dragUploadTemplate = `
    <div class="d-flex flex-column upload-drop-zone justify-content-center align-items-center p-2" id="dropZone">
        <img class="bounceIn" src="/static/home/images/icons/upload.svg" width="70" height="70">
        <input type="file" id="dropUploadFiles" name="${inputName}" hidden>
        <p class="text-black-50" id="dropZoneStatus">برای آپلود، فایل ها را اینجا بکشید.</p>
        <p class="text-black-50 mt-n2" id="dropZoneSize" style="display: none">
        <span id="fileSize"></span>
        مگابایت
        </p>
        <button id="uploadButton" type="button" class="btn btn-primary btn-sm">انتخاب فایل</button>
    </div>
    `;
    $(".drop-zone").append(dragUploadTemplate);

    let dropZone = $("#dropZone");

    dropZone.on("dragover", function (e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).addClass("drop");
    });

    dropZone.on("dragover", function (e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).addClass("drop");
    });

    dropZone.on("dragleave", function (e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).removeClass("drop");
    });

    $("#dropUploadFiles").on("change", function (e) {
        let file = e.target.files[0];
        dropZone.find("#dropZoneStatus").text(file.name);
        console.log($(this).find("#fileSize"))
        dropZone.find("#fileSize").text(Math.round(file.size / (1024 * 1024) * 100) / 100)
        dropZone.find("#dropZoneSize").show();
    });

    dropZone.on("drop", function (e) {
        e.preventDefault();
        e.stopPropagation();
        document.getElementById("dropUploadFiles").files = e.originalEvent.dataTransfer.files;
        $("#dropUploadFiles").change();
    });

    dropZone.on("click", function (e) {
        document.getElementById('dropUploadFiles').click();
    });

}
