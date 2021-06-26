(function (window, document, $) {
    'use strict';
    var $html = $('html');
    var $body = $('body');
    var $cart = $('#cart');
    var $cart_btn = $(".add_to_basket");
    var $cart_content = $("#cart-content");
    //$cart_content.modal({observeChanges: true});


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

    $(".price-unit").on("click", function () {
        if ($(this).is(':checked')) {
            $(".add_to_basket.basket-" + $(this).attr("data-id")).removeAttr("disabled").addClass("selected-basket");
            $cart_btn.attr("data-unit", $(this).val())
        }
    });
    $cart_btn.on("click", function () {
        if (!$(this).attr("disabled")) {
            $cart.modal("show");
            $.ajax({
                beforeSend: function (xhr, settings) {
                    var csrftoken = getCookie('csrftoken');
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                url: '/cart',
                type: 'POST',
                data: {
                    'product': $(this).attr("data-id"),
                    'name': $(this).attr("data-name"),
                    'image': $(this).attr("data-image"),
                    'unit': $(this).attr("data-unit"),
                    'price': $(this).attr("data-price"),
                    'quantity': 1
                },
                dataType: 'json',
                success: function (result) {
                    console.log(result)
                },
                error: function (request, error) {
                    console.log(request)
                }
            });
        }
    });

    $cart.on('shown.bs.modal', function () {
        $.ajax({
            beforeSend: function (xhr, settings) {
                var csrftoken = getCookie('csrftoken');
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            url: '/cart',
            type: 'GET',
            data: {},
            dataType: 'json',
            success: function (response) {
                var html = "";
                var i = 1;
                jQuery.map(response.result, function (data, index) {
                    i = i + 1;
                    html = html + '<div class="row product-card"> \
                                <div class="col-md-2 col-xs-3">  \
                                    <figure class="thumb_menu_list"><img  \
                                            src="/media/' + data.image + '" \
                                            alt="thumb"></figure> \
                                </div> \
                                <div class="col-md-10 col-xs-9"> \
                                    <ul class="product-row product-row-cart"> \
                                        <li><h5>' + data.name + '</h5></li> \
                                        <li> \
                                            <div class="row cart-element"> \
                                                <div class="col-md-9 col-xs-9 cart-amount-box"> \
                                                    <div class="input-group amount-input"> \
                                                    <span class="input-group-addon cart-minus" data-id="' + index + '"><i \
                                                            class="icon_minus_alt"></i></span> \
                                                        <input type="text" class="form-control prk-quantity prk-' + index + '" value="' + data.quantity + '"> \
                                                        <span class="input-group-addon cart-plus" data-id="' + index + '"><i \
                                                                class="icon_plus_alt"></i></span> \
                                                    </div> \
                                                </div> \
                                                <div class="col-md-3 col-xs-3 cart-trash-box"> \
                                                    <a href="#" class="btn btn-danger cart-2" data-toggle="dropdown" \
                                                       aria-expanded="true"><i \
                                                            class="icon_trash"></i></a> \
                                                </div> \
                                            </div> \
                                        </li> \
                                    </ul> \
                                </div> \
                            </div>'
                });
                $cart_content.html(html);
                if (i > 4) {
                    i = 4
                }
                $cart.css("margin-top", (i * -40));
                $(".product-card:odd").addClass("card-even")
            },
            error: function (request, error) {
                console.log(request)
            }
        });
    });

    $body.on("click", ".cart-plus", function () {
        var input = $(".prk-" + $(this).attr("data-id"));
        input.val(parseInt(input.val()) + 1);
        input.change()

    });

    $body.on("click", ".cart-minus", function () {
        var input = $(".prk-" + $(this).attr("data-id"));
        if (parseInt(input.val())  > 1){
             input.val(parseInt(input.val()) - 1)
        }
        input.change()
    });

     $body.on("change paste", ".prk-quantity", function () {
        console.log($(this).val())
    });

    $(".close-cat").on("click", function () {
        $cart.modal("hide");
    });
})(window, document, jQuery);