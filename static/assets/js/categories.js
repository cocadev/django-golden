var Categories = function () {


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

    var trackNameDescription = function () {
        var name_prev = $("#category-name-prev");
        var desc_prev = $("#category-desc-prev");
        $("#category_name").on("change keydown paste input", function () {
            if ($(this).val().length > 0) {
                name_prev.html($(this).val())
            } else {
                name_prev.html("Product Name");
            }
        });
        $("#category-desc").on("change keydown paste input", function () {
            if ($(this).val().length > 0) {
                var text = $(this).val();
                if ($(this).val().length > 80) {
                    text = jQuery.trim(text).substring(0, 80)
                            .split(" ").slice(0, -1).join(" ") + "...";
                }

                desc_prev.html(text)

            } else {
                desc_prev.html("Here you can add some description of your category.");
            }
        });
    };

    var handleImage = function () {
        var category_img = $("#category_img");
        var category_img_input = $(".category_img_input");
        category_img.on("click", function (e) {
            e.preventDefault();
            category_img_input.click()
        })
        category_img_input.on('change', function () {
            readImage(this)
        });

        function readImage(input) {
            var ValidImageTypes = ["image/gif", "image/jpeg", "image/png"];

            if (input.files && input.files[0]) {
                if ($.inArray(input.files[0]["type"], ValidImageTypes) < 0) {
                    return;
                }
                var reader = new FileReader();
                reader.onload = function (e) {
                    category_img.children("img").attr('src', e.target.result);
                };
                reader.readAsDataURL(input.files[0]);
            }
        }
    };
    return {
        //main function to initiate template pages
        init: function () {
            trackNameDescription();
            handleImage();
        },
        draw: function () {
        }

    };
}();