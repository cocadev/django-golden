var Orders = function () {
    var orders_table = $('#orders_table');
    var reloader = $("#re-loader");

    function getRandomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
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

    var handleDateRage = function () {
        // Basic Date Range Picker
        $('.daterange').daterangepicker(
            {
                singleDatePicker: true,
                autoUpdateInput: true,
                timePicker: true,
                timePickerIncrement: 5,
                timePicker24Hour: true,
                use24hours: true,
                locale: {
                    format: 'DD/MM/YYYY HH:mm'
                }
            }
        )

    };

    var deleteOrder = function () {
        var removeBtn = $(".remove-order");
        var clickedBtn;
        var modalBox = $("#remove-confirm-modal")
        removeBtn.on("click", function (e) {
            clickedBtn = $(this);
            modalBox.modal("show");
            e.preventDefault();

            $("#remove-confirm-action").on("click", function () {

                modalBox.modal("hide");
                $.ajax({
                    beforeSend: function (xhr, settings) {
                        var csrftoken = getCookie('csrftoken');
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    },
                    url: '/accounts/orders/update/',
                    type: 'DELETE',
                    data: {
                        'order_id': removeBtn.attr("data-id")
                    },
                    dataType: 'text',
                    success: function (data) {
                        reloader.click();
                        clickedBtn.parent().parent().hide()
                    },
                    error: function (request, error) {
                        console.log(request)
                    }
                });
            });
        })
    };

    var createInvoice = function () {
        var seen = false;
        $('#create-invoice').on("click", function () {
            if (!seen) {
                $.ajax({
                    beforeSend: function (xhr, settings) {
                        var csrftoken = getCookie('csrftoken');
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    },
                    url: '/accounts/api/clients/',
                    type: 'GET',
                    data: {},
                    dataType: 'json',
                    success: function (data) {
                        $.map(data.results, function (result, i) {
                            var title = result.client.company_name + " - " + result.client.first_name + " " + result.client.last_name;
                            $("#clients").append(new Option(title, result.client.pk, false, false)).trigger('change');
                        });
                        seen = true
                    }
                    ,
                    error: function (request, error) {
                        console.log(request)
                    }
                });
            }
        })
    };
    var addOrder = function () {
        var product_select = $('#products');
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
                data: {
                    'length': 1000
                },
                dataType: 'json',
                success: function (data) {
                    var sl = new Option("", "", false, false);
                    sl.selected = true;
                    sl.disabled = true;
                    product_select.empty();
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

                    product_select.append(sl).trigger('change');
                }
                ,
                error: function (request, error) {
                    console.log(request)
                }
            });
        });
        $("#submitOrder").on("click", function (e) {
            e.preventDefault()
            if ((product_select.val() > 0) && ($("#amount").val() > 0)) {
                $("#orderForm").submit();
            } else {
                $("#orders-alert").slideToggle()
            }
        });
    };
    var table = function () {
        var colors = {};
        $('#orders_table').DataTable({
            responsive: false,
            autoWidth: false,
            serverSide: true,
            pageLength: 25,
            searching: true,
            sAjaxDataProp: 'results',
            order: [[5, "desc"]],
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
                {"data": "pk", "orderable": false},
                {"data": "uuid"},
                {"data": "client"},
                {"data": "orders", "orderable": false},
                {"data": "state"},
                {"data": "issue_date"},
                {"data": "pk", "orderable": false},
            ],
            ajax: {
                url: '/accounts/api/invoices/',
                headers: {
                    'CSRFToken': getCookie('csrftoken')
                },
                type: "GET",
                data: {
                    "cid": "1"
                }
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

                api.column(-2, {page: 'current'}).data().each(function (group, i) {
                    if (last !== group) {
                        $(rows).eq(i).before(
                            '<tr class="group"><td colspan="8"><span class="badge badge-success text-bold-800" style="background-color: #2d303b">' + group + '</span></td></tr>'
                        );

                        last = group;
                    }
                });
            },
            "columnDefs": [
                {
                    "targets": 0,
                    "className": "text-center",
                    "render": function (data, type, row) {
                        return '<input data-id="' + row.pk + '" type="checkbox" class="input-chk">'
                    }
                },
                {
                    "targets": 1,
                    "className": "text-center",
                    "render": function (data, type, row) {
                        return '<a href="' + row.pk + '">' + data + '</a>'
                    }
                },
                {
                    "targets": 2,
                    "className": "text-center",
                    "render": function (data, type, row) {
                        if (data.company_name)
                            return '<a href="' + row.pk + '">' + data.company_name + '</a>'
                        return '<a href="' + row.pk + '">' + data.first_name + ' ' + data.last_name + '</a>'
                    }
                },
                {
                    "targets": 4,
                    "className": "text-center",
                    "render": function (data, type, row) {
                        return "<span class='badge badge-m badge-warning state-" + data + "'><a  class='text-bold-600' href='#' >" + data + "</a></span>"
                    }
                },
                {
                    "targets": 3,
                    "className": "text-center",
                    "render": function (data, type, row) {
                        return data.length
                    }
                },
                {
                    "targets": 5,
                    "className": "text-center",
                    "render": function (data, type, row) {
                        return data
                    }
                },
                {
                    "targets": 6,
                    "className": "text-center orders-options",
                    "render": function (data, type, row) {
                        return "<a class='btn btn-icon btn-pure secondary' style='color: #5c6382' href='" + row.pk + "' data-id='" + data + "'><i class='la la-list'></i></a>" +
                            "<a class='btn btn-icon btn-pure secondary delete-invoice' data-id='" + data + "'><i class='la la-remove'></i></a>"
                    }
                }
            ]
        });
        $('.buttons-copy, .buttons-csv, .buttons-print, .buttons-pdf, .buttons-excel').addClass('btn btn-sm btn-info mr-1 d-none');
    };
    var tableOptions = function () {
        var confirmModal = $("#merge-confirm-modal");
        var html = "<div class='table-options col-sd-12'><a id='merge-invoices' href='#' data-toggle='modal'" +
            " data-target='merge-confirm-modal'><i class=''></i>Merge Invoice</a><a  href='#' data-toggle='dropdown'" +
            " aria-haspopup='true' aria-expanded='false' id='change-state' class='change-state'>Change state</a></div>";
        $("#orders_table_filter").prepend(html);

        $("#merge-invoices").on("click", function (e) {
            e.preventDefault();
            confirmModal.modal("show");

            $("#merge-confirm-action").on("click", function () {
                confirmModal.modal("hide");
                ids = [];

                orders_table.find('input[type="checkbox"]:checked').each(function () {
                    ids.push($(this).attr("data-id"))
                });
                reloader.click();
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
                reloader.click();
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
    var statesHandler = function () {
        var stateBtn = $(".state-btn");
        var stateModal = $("#state-confirm-modal");

        $("#change-state").on("click", function () {
            stateModal.modal("show");
        });

        stateBtn.click(function () {
            stateBtn.removeClass("active");
            $(this).addClass("active");
        });
        $("#state-confirm-action").on("click", function () {
            ids = [];
            stateModal.modal("hide");
            reloader.click();


            orders_table.find('input[type="checkbox"]:checked').each(function () {
                ids.push($(this).attr("data-id"))
            });

            if (ids.length > 0) {
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
                        ids: ids,
                        state: $(".state-btn.active").attr("data-role")
                    },
                    dataType: 'json',
                    success: function (data) {
                        orders_table.DataTable().ajax.reload();
                    }
                    ,
                    error: function (request, error) {
                        orders_table.DataTable().ajax.reload();
                    }
                });
            }
        })


    };

    var changeUnit = function () {
        var units = $("#unit");
        $("#products").on("select2:select", function (e) {
            var data = e.params.data;
            units.empty();
            $.ajax({
                beforeSend: function (xhr, settings) {
                    var csrftoken = getCookie('csrftoken');
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                url: '/accounts/products/create/pricing/',
                type: 'GET',
                data: {
                    'id': data.id
                },
                dataType: 'json',
                success: function (data) {
                    $.map(data.result, function (name, unit) {
                        units.append(new Option(name, unit, false, false)).trigger('change');
                    });
                }
                ,
                error: function (request, error) {
                    console.log(request)
                }
            });
        })
    };
    return {
        //main function to initiate
        init: function () {
            deleteOrder();
            addOrder();
            changeUnit();

        },
        run: function () {
            table();
            tableOptions();
            statesHandler();
            createInvoice();
            handleDateRage()
        }
    };
}();