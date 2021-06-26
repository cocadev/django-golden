var Products = function () {
    var product_table = $('#product_table');
    var img_box = $("#product_img, #product-upload-btn");
    var img_input = $("#product_img_input");
    var statistic_tab = $("#statisticTab");

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

    var handleLogo = function () {
        img_box.on("click", function (e) {
            e.preventDefault();
            img_input.click();
        });
        img_input.on('change', function () {
            readImage(this)
        });
        $("#clear-product-input").click(function (e) {
            e.preventDefault();
            img_input.val("");
            img_box.attr("src", "/static/app-assets/images/photo_default.png")
        });
        function readImage(input) {
            var ValidImageTypes = ["image/gif", "image/jpeg", "image/png"];

            if (input.files && input.files[0]) {
                if ($.inArray(input.files[0]["type"], ValidImageTypes) < 0) {
                    return;
                }
                var reader = new FileReader();
                reader.onload = function (e) {
                    img_box.attr('src', e.target.result);
                };
                reader.readAsDataURL(input.files[0]);
            }
        }
    };

    var handleDateRage = function () {
        // Basic Date Range Picker
        $('.daterange').daterangepicker(
            {
                autoUpdateInput: false,
                timePicker: true,
                timePickerIncrement: 30,
                locale: {
                    format: 'DD/MM/YYYY'
                }
            }
        ).on('apply.daterangepicker', function (ev, picker) {
            $(this).val(picker.startDate.format('DD/MM/YYYY') + ' - ' + picker.endDate.format('DD/MM/YYYY'));
        }).on('cancel.daterangepicker', function (ev, picker) {
            $(this).val('');
        });

    };

    var table = function () {
        var colors = {};
        product_table.DataTable({
            responsive: false,
            autoWidth: false,
            serverSide: true,
            searching: true,
            sAjaxDataProp: 'results',
            order: [[3, "asc"]],
            dataType: 'json',
            dom: 'Blfrtip',
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
                {
                    "data": "image",
                    "orderable": false,
                    className: "d-none d-sm-none d-md-none d-lg-none d-xl-table-cell"
                },
                {"data": "name"},
                {"data": "short_description", "visible": false},
                {"data": "category", className: "d-none d-sm-none d-md-none  d-lg-none d-xl-table-cell"},
                {"data": "article_number", "className": "text-center d-none d-sm-none  d-md-table-cell"},
                {"data": "period", className: "d-none d-sm-none d-md-none d-lg-table-cell"},
                {"data": "is_active"}
            ],
            ajax: {
                url: '/accounts/api/products/',
                headers: {
                    'CSRFToken': getCookie('csrftoken')
                },
                type: "GET",
                data: {
                    "cid": product_table.attr("data-filter")
                }
            },
            "drawCallback": function (settings) {
                $(".switchBootstrap").bootstrapSwitch();

                var api = this.api();
                var rows = api.rows({page: 'current'}).nodes();
                var last = null;

                api.column(3, {page: 'current'}).data().each(function (group, i) {
                    if (last !== group) {
                        $(rows).eq(i).before(
                            '<tr class="group"><td colspan="8"><span class="text-bold-800">' + group + '</span></td></tr>'
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
                        if (data)
                            return '<img src="' + data + '" alt="' + row.name + '" class="media-object table-thumbnail">'
                        return ""
                    }
                },

                {
                    "targets": 1,
                    "render": function (data, type, row) {
                        var description = "";
                        if (row.short_description)
                            description = jQuery.trim(row.short_description).substring(0, 50)
                                    .split(" ").slice(0, -1).join(" ") + "...";
                        return "<a href='/accounts/products/" + row.pk + "/' class='text-bold-600'>" + data + "</a>" +
                            '<p class="text-muted d-none d-sm-none d-md-none d-lg-none d-xl-table-cell">' + description + '</p>';
                    }
                },
                {
                    "targets": 2,
                    "className": "text-center",
                    "render": function (data, type, row) {
                        return "<a href='/accounts/products/" + row.pk + "/'>" + data + "</a>"
                    }
                },
                {
                    "targets": 3,
                    "className": "text-center",
                    "render": function (data, type, row) {
                        if (!colors[data]) {
                            colors[data] = getRandomColor()
                        }
                        return "<span class='badge badge-m badge-warning' style='background-color: " + colors[data] + "'><a  class='text-bold-600' href='/accounts/categories/' >" + data + "</a></span>"
                    }
                },
                {
                    "targets": -2,
                    "className": "text-center",
                    "render": function (data, type, row) {
                        if (data)
                            return "<div class='badge badge-danger badge-square'><i class='la la-calendar font-medium-2'></i><span>" + data + "</span></div>";
                        return ""
                    }
                },
                {
                    "targets": -1,
                    "orderable": false,
                    "className": "text-center",
                    "render": function (data, type, row) {
                        checked = "";
                        if (row.is_active) {
                            checked = "checked"
                        }


                        return "<a  class='btn  btn-sm btn-icon btn-info mr-1' href='/accounts/products/" + row.pk + "'>" +
                            "<i class='ft-edit'></i></a>" +
                            '<input type="checkbox" data-id="' + row.pk + '" class="switchBootstrap product_state" ' +
                            'data-on-text="<i class=\'la la-truck\'></i>" ' +
                            'data-off-text="<i class=\'la la-lock\'></i>" data-on-color="success" ' +
                            'data-off-color="danger"' + checked + '/>'


                    }
                }]
        });
        $('.buttons-copy, .buttons-csv, .buttons-print, .buttons-pdf, .buttons-excel').addClass('btn btn-sm btn-info mr-1 d-none');
    };

    var deleteProductImage = function () {
        $(document).on("click", "#delete-product-image", function (e) {
            e.preventDefault();
            var id = $(this).attr("data-id");
            $.ajax({
                beforeSend: function (xhr, settings) {
                    var csrftoken = getCookie('csrftoken');
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                url: '/accounts/product/update/',
                type: 'DELETE',
                data: {
                    'product_id': id
                },
                dataType: 'text',
                success: function (data) {
                    img_box.attr("src", "/static/app-assets/images/photo_default.png")
                },
                error: function (request, error) {
                    console.log(request)
                }
            });

        });
    };

    var disableProduct = function () {
        $(document).on("switchChange.bootstrapSwitch", ".switchBootstrap", function () {
            $.ajax({
                beforeSend: function (xhr, settings) {
                    var csrftoken = getCookie('csrftoken');
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                url: '/accounts/product/update/',
                type: 'POST',
                data: {
                    'product_id': $(this).attr("data-id")
                },
                dataType: 'text',
                success: function (data) {
                },
                error: function (request, error) {
                    console.log(request)
                }
            });
        });
    };

    var history_table = function () {
        var colors = {};
        var historyTble = $('#orders_table');
        historyTble.DataTable({
            responsive: false,
            autoWidth: false,
            serverSide: true,
            searching: true,
            sAjaxDataProp: 'results',
            order: [[5, "desc"]],
            dataType: 'json',
            dom: 'frtlp',
            columns: [

                {"data": "uuid"},
                {"data": "client"},
                {"data": "orders", "orderable": false},
                {"data": "uuid"},
                {"data": "state"},
                {"data": "created_date"},


            ],
            ajax: {
                url: '/accounts/api/invoices/product/',
                headers: {
                    'CSRFToken': getCookie('csrftoken')
                },
                type: "GET",
                data: {
                    "product-id": historyTble.attr("data-id")
                }
            },
            "drawCallback": function (settings) {
                var api = this.api();
                var rows = api.rows({page: 'current'}).nodes();
                var last = null;

                api.column(-1, {page: 'current'}).data().each(function (group, i) {
                    if (last !== group) {
                        $(rows).eq(i).before(
                            '<tr class="group"><td colspan="8"><span class="badge badge-success text-bold-800" style="background-color: ' + colors[group] + '">' + group + '</span></td></tr>'
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
                        return '<a href="/accounts/orders/' + row.pk + '">' + data + '</a>'
                    }
                },
                {
                    "targets": 1,
                    "className": "text-center",
                    "render": function (data, type, row) {
                        if (data.company_name)
                            return '<a href="/accounts/orders/' + row.pk + '">' + data.company_name + '</a>'
                        return '<a href="/accounts/orders/' + row.pk + '">' + data.first_name + ' ' + data.last_name + '</a>'
                    }
                },
                {
                    "targets": 2,
                    "className": "text-center",
                    "render": function (data, type, row) {
                        return data.length
                    }
                },
                {
                    "targets": 3,
                    "className": "text-center",
                    "render": function (data, type, row) {
                        var amount = 0;
                        for (var i = 0; i < row.orders.length; i++) {
                            if (row.orders[i].pk = historyTble.attr("data-id"))
                                amount = row.orders[i].amount
                        }

                        if (!(amount % 1 != 0))
                            return parseInt(amount)
                        return amount
                    }
                },
                {
                    "targets": 4,
                    "className": "text-center",
                    "render": function (data, type, row) {
                        if (!colors[data]) {
                            colors[data] = getRandomColor()
                        }
                        return "<span class='badge badge-m badge-warning' style='background-color: " + colors[data] + "'><a  class='text-bold-600' href='/accounts/categories/' >" + data + "</a></span>"
                    }
                }
            ]
        });
        $('.buttons-copy, .buttons-csv, .buttons-print, .buttons-pdf, .buttons-excel').addClass('btn btn-sm btn-info mr-1 d-none');
    };

    var productBarChart = function () {
        var lineChart;
        var periodRange = $('#statistic-period');
        var interval = $('#statistic-interval');

        function drawChart(periodStart, periodEnd, interval) {
            //Get the context of the Chart canvas element we want to select
            var ctx = $("#column-chart");

            if (typeof lineChart != "undefined") {
                lineChart.destroy()
            }

            // Chart Options
            var chartOptions = {
                // Elements options apply to all of the options unless overridden in a dataset
                // In this case, we are setting the border of each bar to be 2px wide and green
                elements: {
                    rectangle: {
                        borderWidth: 2,
                        borderColor: 'rgb(0, 255, 0)',
                        borderSkipped: 'bottom'
                    }
                },
                responsive: true,
                maintainAspectRatio: false,
                responsiveAnimationDuration: 100,
                legend: {
                    position: 'top',
                },
                scales: {
                    xAxes: [{
                        display: true,
                        barPercentage: 0.6,
                        gridLines: {
                            color: "#f3f3f3",
                            drawTicks: false
                        },
                        scaleLabel: {
                            display: true
                        }
                    }],
                    yAxes: [{
                        display: true,
                        stepSize: 1,
                        ticks: {
                            stepSize: 1,
                            suggestedMin: 0
                        },
                        gridLines: {
                            color: "#f3f3f3",
                            drawTicks: false
                        },
                        scaleLabel: {
                            display: true
                        }
                    }]
                },
                title: {
                    display: true,
                    text: 'Product charts'
                }
            };

            var labels = [];
            var st_data = [];

            $.ajax({
                beforeSend: function (xhr, settings) {
                    var csrftoken = getCookie('csrftoken');
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                url: '/accounts/api/products/statistics/',
                type: 'GET',
                data: {
                    'product': $("#statistic-product").val(),
                    'from': periodStart,
                    'till': periodEnd,
                    'interval': interval
                },
                dataType: 'json',
                success: function (data) {
                    if (data.result) {
                        data.result.map(function (key, value) {
                            var date = key[Object.keys(key)[0]];
                            var count = key["count"];
                            labels.push(moment(date).format('DD-MM-YYYY'));
                            st_data.push(parseInt(count))
                        });
                        // Chart Data
                        var chartData = {
                            labels: labels,
                            datasets: [{
                                label: "Number of orders [" + interval + "]",
                                data: st_data,
                                backgroundColor: "#26C6DA",
                                hoverBackgroundColor: "#0097A7",
                                borderColor: "transparent"
                            }]
                        };
                        console.log(chartData);
                        var config = {
                            type: 'bar',
                            // Chart Options
                            options: chartOptions,

                            data: chartData
                        };
                        lineChart = new Chart(ctx, config);

                        ctx.css("height", "400px");
                    }
                },
                error: function (request, error) {
                    console.log(request)
                }
            });
        }

        periodRange.daterangepicker({
            showDropdowns: true,
            startDate: moment().add(-30, 'days'),
            endDate: moment(),
            locale: {
                format: 'DD-MM-YYYY'
            }
        }).on('apply.daterangepicker', function (ev, picker) {
            drawChart(picker.startDate.format("DD-MM-YYYY"), picker.endDate.format("DD-MM-YYYY"), interval.val());
        });

        interval.on('select2:select', function (e) {
            var date = periodRange.val().split(" - ");
            drawChart(date[0], date[1], interval.val());

        });

        statistic_tab.on("click", function () {

            drawChart(moment().add(-14, 'days').format("DD-MM-YYYY"), moment().format("DD-MM-YYYY"), interval.val());
        })
    };

    var totalOrders = function () {
        statistic_tab.on("click", function () {
            $.ajax({
                beforeSend: function (xhr, settings) {
                    var csrftoken = getCookie('csrftoken');
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                url: '/accounts/api/products/statistics/',
                type: 'GET',
                data: {
                    'product': $("#statistic-product").val(),
                    'type': "TotalOrders"
                },
                dataType: 'json',
                success: function (data) {
                    $("#total-orders").html(data.result);
                },
                error: function (request, error) {
                    console.log(request)
                }
            });
        });
    };
    var sumOrders = function () {
        statistic_tab.on("click", function () {
            $.ajax({
                beforeSend: function (xhr, settings) {
                    var csrftoken = getCookie('csrftoken');
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                url: '/accounts/api/products/statistics/',
                type: 'GET',
                data: {
                    'product': $("#statistic-product").val(),
                    'type': "SumOrders"
                },
                dataType: 'json',
                success: function (data) {
                    $("#sum-orders").html(data.result);
                },
                error: function (request, error) {
                    console.log(request)
                }
            });
        });
    };

    var pricesUnites = function () {
        var removedElement;
        var toRemove;
        var confirmModal = $("#remove-confirm-modal");
        // Default
        $('.repeater-default').repeater();

        // Custom Show / Hide Configurations
        $('.file-repeater, .contact-repeater').repeater({
            show: function () {
                $(this).slideDown();
                $(this).find("select option").attr("disabled", false);
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
    };

    return {
        //main function to initiate template pages
        init: function () {
            handleLogo();
            handleDateRage();
            deleteProductImage();
        },
        draw: function () {
            table();
            disableProduct();
        },
        history: function () {
            history_table();
        },
        statistic: function () {
            productBarChart();
            totalOrders();
            sumOrders();
        },
        prices: function () {
            pricesUnites();
        }
    };
}();