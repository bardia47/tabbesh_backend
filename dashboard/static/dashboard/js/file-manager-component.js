let uploadModal = $("#uploadModal");
let uploadModalTitle = uploadModal.find("#title");
let uploadModalDescription = uploadModal.find("#description");
let uploadModalSenderId = uploadModal.find("#senderId");
let uploadModalDocumentId = uploadModal.find("#documentId");
let uploadModalAddOrEditStatus = uploadModal.find("#addOrEditStatus");
let uploadModalSubmit = uploadModal.find("#uploadSubmit");
let courseCode = "";

function renderDocuments(data) {
    let documentRowsTemplate = ``, documentRow = ``, fileManagerTemplate = ``;
    if (data.documents.length === 0) {
        documentRowsTemplate = `
        <tr>
            <td class="p-3 vazir-bold" style="font-size: 15px;" colspan="8" scope="row">
                <img class="mb-2" src="/static/home/images/icons/file-manager-empty.svg" width="35"
                     height="35">
                <br>
                متاسفانه جزوه ای یافت نشد !
            </td>
        </tr>
        `;
    } else {
        $.each(data.documents, function (index, document) {
            $("#courseId").val(document.course);
            let documentUploadDate = new persianDate(Date.parse(document.upload_date));
            documentRow = `
            <tr>
                <th style="font-family:'Vazir_Bold'" scope="row">${index + 1}</th>
                <td>${document.title}</td>
                <td>${document.sender_name}</td>
                <td>${documentUploadDate.format("LLLL")}</td>
                <td>${document.description}</td>
                <td data-toggle="tooltip" data-placement="top" title="تغییر جزوه">
                    <a class="edit-document" data-id="${document.id}" data-document-title="${document.title}" data-description="${document.description}"
                        style="cursor: pointer">
                        <i class="fas fa-edit text-info"></i>
                    </a>
                 </td>
                <td data-toggle="tooltip" data-placement="top" title="حذف جزوه">
                    <a class="delete-document" data-document-id="${document.id}"style="cursor: pointer">
                        <i class="fas fa-trash-alt text-danger"></i>
                    </a>
                </td>
                <td data-toggle="tooltip" data-placement="top" title="دانلود جزوه" style="text-align:center"><a href="${document.upload_document}" target="_blank">
                    <img src="/static/home/images/icons/download.svg" width="20" height="20"></a>
                </td>
            </tr>
            `;
            documentRowsTemplate += documentRow;
        });
    }

    fileManagerTemplate = `
    <div id="fileManagerContainer" class="container">
        <div id="fileManagerTitle"  class="row mb-2">
            <div class="d-flex col-md-5 file-manager-image">
                <img src="${data.course.image}" width="50" height="50">
                <div class="ml-2">
                    <p class="m-0"><strong>${data.course.title}</strong></p>
                    <h6 class="p-0"><small>${data.course.teacher}</small></h6>         
                </div>
            </div>
            <div  id="addFileButton" class="ml-auto" data-toggle="tooltip" data-placement="top" title="اضافه کردن جزوه">
                <img class="mt-3 mr-md-5" src="/static/home/images/icons/plus.svg" width="35" height="35">
            </div>
        </div>
        <div class="table-responsive-sm">
            <table class="table table-hover">
                <thead>
                <tr>
                    <th scope="col"><img src="/static/home/images/icons/folder.svg" width="25" height="25"></th>
                    <th scope="col">عنوان</th>
                    <th scope="col">فرستنده</th>
                    <th scope="col">تاریخ</th>
                    <th scope="col">توضیحات</th>
                    <th scope="col">ویرایش</th>
                    <th scope="col">حذف</th>
                    <th scope="col">دانلود</th>
                </tr>
                </thead>
                <tbody>
                    ${documentRowsTemplate}
                </tbody>
            </table>
        </div>
    </div>
`;
    $("#fileManager").append(fileManagerTemplate);
    $('[data-toggle="tooltip"]').tooltip()

    addDocumentConfigure();
    editDocumentsConfigure();
    deleteDocumentsConfigure();
}


function fileManagerRender(code) {
    courseCode = code;
    $.ajax({
        url: `/dashboard/lessons/files/${courseCode}/`,
        type: "GET",
        dataType: "json",
        success: function (data) {
            $("#fileManagerContainer").remove();
            renderDocuments(data);
        },
        error: function () {
            alert("خطا در بارگزاری جزوات ... صفحه را بازنشانی کنید!")
        },
    });
}


function addDocumentConfigure() {
    // fire modal with button
    $("#addFileButton").click(function () {
        // reset inputs data
        uploadModalAddOrEditStatus.val("add");
        uploadModalTitle.val("");
        uploadModalDescription.val("");

        // configure modal for edit document
        uploadModal.find(".modal-title").text("اضافه کردن جزوه ی جدید");
        uploadModal.find("#titleLabel").text("عنوان جزوه");
        uploadModal.find("#descriptionLabel").text("توضیحات جزوه");
        uploadModal.find("#fileLabel").text("فایل جدید جزوه را در این قسمت آپلود کنید.");
        uploadModal.find("#uploadSubmit").text("آپلود جزوه");
        uploadModal.modal();
    });
}


function editDocumentsConfigure() {
    $(".edit-document").click(function () {
        // fill inputs data
        uploadModalTitle.val($(this).data("document-title"));
        uploadModalDescription.val($(this).data("description"));
        uploadModalDocumentId.val($(this).data("id"));
        uploadModalAddOrEditStatus.val("edit");

        // configure modal for edit document
        uploadModal.find(".modal-title").text("تغییر جزوه ی آپلود شده");
        uploadModal.find("#titleLabel").text("عنوان جدید جزوه");
        uploadModal.find("#descriptionLabel").text("توضیحات جدید");
        uploadModal.find("#fileLabel").text("در صورت تغییر فایل جزوه می توانید از این قسمت استفاده کنید.");
        uploadModal.find("#uploadSubmit").text("ثبت تغییرات");
        uploadModal.modal();
    });
}

// delete documents
function deleteDocumentsConfigure() {
    $(".delete-document").click(function () {
        $("#deleteFileModal").modal();
        $("#deleteDocumentId").val($(this).data("document-id"))
    })
}

function addDocumentAjax() {
    let editFormData = new FormData($("#documentUploadForm")[0]);
    if ($("#dropUploadFiles")[0].files.length === 0) editFormData.delete("upload_document");
    $.ajax({
        url: `/dashboard/lessons/files/${courseCode}/`,
        type: "POST",
        data: editFormData,
        processData: false,
        contentType: false,
        dataType: "json",
        beforeSend: function (xhr, settings) {
            uploadModalSubmit.prop('disabled', true);
            $("#uploadModal").find("#uploadSubmit").text("در حال آپلود");
            $("#uploadLoading").show();
            $("#uploadFailedAlert").hide();
        },
        success: function (data, textStatus, xhr) {
            uploadModalSubmit.prop('disabled', false);
            $("#uploadLoading").hide();
            $("#uploadModal").modal("hide");
            // render file manager with new data
            fileManagerRender(courseCode);
            resetModal();
        },
        error: function (xhr, status, error) {
            uploadModalSubmit.prop('disabled', false);
            $("#uploadLoading").hide();
            $("#uploadFailedAlert").show();
        }
    });

}


function editDocumentAjax() {
    let editFormData = new FormData($("#documentUploadForm")[0]);
    if ($("#dropUploadFiles")[0].files.length === 0) editFormData.delete("upload_document");
    // read form data
    // for (let p of editFormData) console.log(p[0], p[1])
    $.ajax({
        url: `/dashboard/lessons/files/${courseCode}/${uploadModalDocumentId.val()}/`,
        type: "POST",
        data: editFormData,
        processData: false,
        contentType: false,
        dataType: "json",
        beforeSend: function (xhr, settings) {
            uploadModalSubmit.prop('disabled', true);
            $("#uploadSubmit").text("در حل ثبت تغییرات");
            $("#uploadLoading").show();
            $("#uploadFailedAlert").hide();
        },
        success: function (data, textStatus, xhr) {
            uploadModalSubmit.prop('disabled', false);
            $("#uploadLoading").hide();
            $("#uploadModal").modal("hide");
            // render file manager with new data
            fileManagerRender(courseCode);
            resetModal();
        },
        error: function (xhr, status, error) {
            uploadModalSubmit.prop('disabled', false);
            alert("خطا در تغییر جزوه ، دوباره امتحان کنید.")
            $("#uploadLoading").hide();
            $("#uploadFailedAlert").show();
        }
    });

}


function resetModal() {
    uploadModalTitle.val("");
    uploadModalDescription.val("");
    restDropZone();
    $("#uploadFailedAlert").hide();
    $("#validationForFile").hide();
}

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


$("#deleteFileAccept").click(function () {
    $.ajax({
        url: `/dashboard/lessons/files/${courseCode}/${$("#deleteDocumentId").val()}/`,
        type: "GET",
        dataType: "json",
        success: function () {
            $("#deleteFileModal").modal("hide");
            $("#deleteDocumentId").val("");
            // render file manager with new data
            fileManagerRender(courseCode);
        },
        error: function (xhr, status, error) {
            $("#deleteFileModal").modal("hide");
            $("#deleteDocumentId").val("");
            alert("خطا در حذف جزوه ، دوباره امتحان کنید.");
        }
    });
});


// set default tooltip to hover
$.fn.tooltip.Constructor.Default.trigger = 'hover';