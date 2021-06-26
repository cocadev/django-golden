var Settings = function () {

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function getRandomColor() {
        var letters = '0123456789ABCDEF';
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    var handleLang = function () {
        $(".language-select option").each(function () {
            // Add $(this).val() to your list
            $(this).attr("data-icon", "i flag-icon flag-icon-" + $(this).val());
            $(".select2").trigger('change.select2')
        });
    };
    var handleImage = function () {
        var category_img = $("#company_img, #category-upload-btn");
        var category_img_input = $("#company_img_input");
        category_img.on("click", function (e) {
            e.preventDefault();
            category_img_input.click()
        })
        category_img_input.on('change', function () {
            readImage(this)
        });

        $("#clear-img-input").click(function (e) {
            e.preventDefault();
            category_img_input.val("");
            category_img.attr("src", "/static/app-assets/images/photo_default.png")
        });

        function readImage(input) {
            var ValidImageTypes = ["image/gif", "image/jpeg", "image/png"];

            if (input.files && input.files[0]) {
                if ($.inArray(input.files[0]["type"], ValidImageTypes) < 0) {
                    return;
                }
                var reader = new FileReader();
                reader.onload = function (e) {
                    console.log("tets")
                    category_img.attr('src', e.target.result);
                };
                reader.readAsDataURL(input.files[0]);
            }
        }
    };
    return {
        //main function to initiate template pages
        init: function () {
            handleLang();
            handleImage();
        },
        draw: function () {
        }

    };
}();