function modalRender(modalId, headerTemplate, bodyTemplate, footerTemplate) {
    let modalTemplate = `
    <div class="modal fade" id="${modalId}" tabindex="-1" role="dialog" aria-labelledby="${modalId}" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
            <div class="modal-header">
            ${headerTemplate}
            </div>
            <div class="modal-body">
            ${bodyTemplate}
            </div>
            <div class="modal-footer">
            ${footerTemplate}
            </div>
        </div>
        </div>
    </div>
    `;

    return modalTemplate;
}