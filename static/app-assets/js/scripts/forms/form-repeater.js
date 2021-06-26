/*=========================================================================================
 File Name: form-repeater.js
 Description: Repeat forms or form fields
 ----------------------------------------------------------------------------------------
 Item Name: Modern Admin - Clean Bootstrap 4 Dashboard HTML Template
 Version: 1.0
 Author: PIXINVENT
 Author URL: http://www.themeforest.net/user/pixinvent
 ==========================================================================================*/

(function (window, document, $) {
    'use strict';

    var removedElement;
    var toRemove;
    var confirmModal = $("#remove-confirm-modal");
    // Default
    $('.repeater-default').repeater();

    // Custom Show / Hide Configurations
    $('.file-repeater, .contact-repeater').repeater({
        show: function () {
            $(this).slideDown();
            $(this).find("select").attr("disabled", false);
            $('.select2-container').remove();
            $('.select2').select2({});
        },
        hide: function (remove) {
            removedElement = $(this);
            toRemove = remove;
            confirmModal.modal("show")
        }
    });

    $("#remove-confirm-action").on("click", function () {
        confirmModal.modal("hide");
         $.ajax({
                beforeSend: function (xhr, settings) {
                    var csrftoken = getCookie('csrftoken');
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                url: '/accounts/products/create/pricing/',
                type: 'DELETE',
                data: {
                    'id': removedElement.find("button").attr("data-id")
                },
                dataType: 'text',
                success: function (data) {
                     removedElement.slideUp(toRemove);
                },
                error: function (request, error) {
                    console.log(request)
                }
            });
    });
})(window, document, jQuery);