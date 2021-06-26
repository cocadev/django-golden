var Clients = function () {
    function getRandomColor() {
        var letters = '0123456789ABCDEF';
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

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
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }


    var deleteOrder = function () {
        var removeBtn = $(".remove-order");
        removeBtn.on("click", function () {
            var tmp = $(this);
            $.ajax({
                beforeSend: function (xhr, settings) {
                    var csrftoken = getCookie('csrftoken');
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                url: '/accounts/orders/update/',
                type: 'POST',
                data: {
                    'order_id': $(this).attr("data-id")
                },
                dataType: 'text',
                success: function (data) {
                    $("#re-loader").click();
                    tmp.parent().parent().hide();
                },
                error: function (request, error) {
                    console.log(request)
                }
            });

        })
    };
    var addOrder = function () {
        var product_select = $('#products')
        product_select.empty().select2({
            maximumSelectionSize: 1
        });

        $('#add-order').on("click", function () {
            $.ajax({
                beforeSend: function (xhr, settings) {
                    var csrftoken = getCookie('csrftoken');
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                url: '/accounts/api/products/',
                type: 'GET',
                data: {},
                dataType: 'json',
                success: function (data) {

                    $.map(data.results, function (product, i) {
                        if (!product.is_active) {
                            return;
                        }
                        if (product_select.find("option[value=" + product.pk + "]").length) {
                            product_select.val(product.pk).trigger("change");
                        } else {
                            product_select.append(new Option(product.name, product.pk, false, false)).trigger('change');
                        }
                    });
                }
                ,
                error: function (request, error) {
                    console.log(request)
                }
            });
        })
    };

    var table = function () {
        var colors = {};
        $('#orders_table').DataTable({
            responsive: false,
            autoWidth: false,
            serverSide: true,
            searching: true,
            sAjaxDataProp: 'results',
            order: [[1, "desc"]],
            dataType: 'json',
            dom: 'Bfrtlp',
            buttons: [
                {
                    extend: 'print',
                    exportOptions: {
                        columns: [1, 2, 3, 4, 5]
                    }
                }, {
                    extend: 'excelHtml5',
                    exportOptions: {
                        columns: [1, 2, 3, 4, 5]
                    }
                }, {
                    extend: 'pdfHtml5',
                    exportOptions: {
                        columns: [1, 2, 3, 4, 5]
                    }
                }
            ],
            columns: [
                {"data": "client", "orderable": false},
                {"data": "client"},
                {"data": "client", "orderable": false},
                {"data": "client", "orderable": false},
                {"data": "client", "orderable": false},
                {"data": "client", "orderable": false}
            ],
            ajax: {
                url: '/accounts/api/clients/',
                headers: {
                    'CSRFToken': getCookie('csrftoken')
                },
                type: "GET"

            },
            "drawCallback": function (settings) {
                // Checkbox & Radio 1
                $('.icheck input').iCheck({
                    checkboxClass: 'icheckbox_square-blue',
                    radioClass: 'iradio_square-blue',
                });

                var api = this.api();
                var rows = api.rows({page: 'current'}).nodes();
                var last = null;

                api.column(2, {page: 'current'}).data().each(function (group, i) {
                    if (last !== group.company_name) {

                        $(rows).eq(i).before(
                            '<tr class="group"><td colspan="8"><span class="badge badge-success text-bold-800" style="background: #2d303b">' + group.company_name + '</span></td></tr>'
                        );

                        last = group.company_name;
                    }
                });
            },
            "columnDefs": [
                {
                    "targets": 0,
                    "className": "text-center",
                    "render": function (data, type, row) {
                        return '<a href="' + data.pk + '">' + data.first_name + ' ' + data.last_name + '</a>'
                    }
                },
                {
                    "targets": 1,
                    "className": "text-center",
                    "render": function (data, type, row) {
                        if (data.company_name)
                            return '<a href="' + data.pk + '">' + data.company_name + '</a>'
                        return '<a href="' + data.pk + '">' + data.first_name + ' ' + data.last_name + '</a>'
                    }
                },
                {
                    "targets": 2,
                    "className": "text-center",
                    "render": function (data, type, row) {

                        return "<a href='tel:" + data.phone_number + "'>" + data.phone_number + "</a>"
                    }
                },
                {
                    "targets": 3,
                    "className": "text-center",
                    "render": function (data, type, row) {
                        return "<a href='mailto:" + data.email + "'>" + data.email + "</a>"
                    }
                },
                {
                    "targets": 4,
                    "className": "text-center",
                    "render": function (data, type, row) {
                        if (data.business_address_street)
                            return data.business_address_street + ' ' + data.business_address_house_number + ', <br />' +
                                data.business_address_zipecode + ' ' + data.get_business_address_city_display + ' ' + data.get_business_address_country_display

                        return ""
                    }
                },
                {
                    "targets": 5,
                    "className": "text-center orders-options",
                    "render": function (data, type, row) {
                        return "<a class='btn btn-icon btn-pure secondary' style='color: #5c6382' href='" + row.pk + "' data-id='" + data + "'><i class='la la-list'></i></a>"
                    }
                }
            ]
        });
        $('.buttons-copy, .buttons-csv, .buttons-print, .buttons-pdf, .buttons-excel').addClass('btn btn-sm btn-info mr-1 d-none');
    };
    var tableOptions = function () {
        var confirmModal = $("#merge-confirm-modal")


        $("#merge-invoices").on("click", function () {

            confirmModal.modal("show");

            $("#merge-confirm-action").on("click", function () {
                confirmModal.modal("hide");
                ids = [];

                $('#orders_table').find('input[type="checkbox"]:checked').each(function () {
                    ids.push($(this).attr("data-id"))
                });
                $("#re-loader").click();
                if (ids.length > 0) {
                    $.ajax({
                        beforeSend: function (xhr, settings) {
                            var csrftoken = getCookie('csrftoken');
                            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                            }
                        },
                        url: '/accounts/orders/',
                        type: 'POST',
                        data: {
                            ids: ids
                        },
                        dataType: 'json',
                        success: function (data) {
                            $('#orders_table').DataTable().ajax.reload();
                        }
                        ,
                        error: function (request, error) {
                            $('#orders_table').DataTable().ajax.reload();
                            console.log(error)
                        }
                    });
                }
            })


        });

        $(document).on("click", ".delete-invoice", function (e) {
            var invoice = $(this);
            e.preventDefault();
            confirmModal.modal("show");
            $("#merge-confirm-action").on("click", function () {
                confirmModal.modal("hide");
                $("#re-loader").click();
                if (invoice.attr("data-id") > 0) {
                    $.ajax({
                        beforeSend: function (xhr, settings) {
                            var csrftoken = getCookie('csrftoken');
                            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                            }
                        },
                        url: '/accounts/orders/',
                        type: 'DELETE',
                        data: {
                            invoice: invoice.attr("data-id")
                        },
                        dataType: 'json',
                        success: function (data) {
                            $('#orders_table').DataTable().ajax.reload();
                        }
                        ,
                        error: function (request, error) {
                            $('#orders_table').DataTable().ajax.reload();
                        }
                    });
                }
            })
        });
    };


    return {
        //main function to initiate template pages
        init: function () {
            deleteOrder();
            addOrder();

        },
        run: function () {
            table();
            tableOptions();
        }
    };
}();