var Employee = function () {
    var employee_table;

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

    var renderSwitches = function () {
        // Switchery
        var i = 0;
        if (Array.prototype.forEach) {
            var elems = Array.prototype.slice.call(document.querySelectorAll('.switchery'));

            elems.forEach(function (html) {
                var switchery = new Switchery(html);
            });
        } else {
            var elems1 = document.querySelectorAll('.switchery');

            for (i = 0; i < elems1.length; i++) {
                var switchery = new Switchery(elems1[i]);
            }
        }

        var elemSmall = document.querySelectorAll('.switchery-sm');
        for (i = 0; i < elemSmall.length; i++) {
            new Switchery(elemSmall[i], {className: "switchery switchery-small"});
        }
    };

    var disableUser = function () {
        $(document).on("change", ".switchery", function () {
            $.ajax({
                beforeSend: function (xhr, settings) {
                    var csrftoken = getCookie('csrftoken');
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                url: '/accounts/employees/update/',
                type: 'POST',
                data: {
                    'employee_id': $(this).attr("data-id")
                },
                dataType: 'text',
                success: function (data) {
                    employee_table.ajax.reload();
                },
                error: function (request, error) {
                    console.log(request)
                }
            });
        });
    };
    var table = function () {
        employee_table = $('#employee_table').DataTable({
            responsive: false,
            autoWidth: false,

            serverSide: true,
            searching: true,
            sAjaxDataProp: 'results',
            dataType: 'json',
            columns: [
                {"data": "first_name", className:"d-none d-sm-none d-md-none  d-lg-none d-xl-table-cell"},
                {"data": "last_name"},
                {"data": "email", className:"d-none d-sm-none d-md-table-cell"},
                {"data": "phone_number", className:"d-none d-sm-none d-md-table-cell"},
                {"data": "position", className:"d-none d-sm-none d-md-none d-lg-table-cell"},
                {"data": "is_active"}
            ],
            fnDrawCallback: function (data) {
                renderSwitches()
            },
            ajax: {
                url: '/accounts/api/employees/',
                headers: {
                    'CSRFToken': $("body").attr("data-role")
                },
                type: "GET"

            },
            "columnDefs": [
                {
                    "targets": 0,
                    "render": function (data, type, row) {
                        return "<a href='/accounts/employees/" + row.pk + "'>" + data + "</a>"
                    }
                },
                {
                    "targets": 1,
                    "render": function (data, type, row) {
                        return "<a href='/accounts/employees/" + row.pk + "'>" + data + "</a>"
                    }
                },
                {
                    "targets": -2,
                    "className": "text-center",
                    "render": function (data, type, row) {
                        return '<div class="badge badge-primary label-square">' + data + '</div>'
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


                        return "<a  class='btn  btn-sm btn-icon btn-info mr-1' href='/accounts/employees/" + row.pk + "'>" +
                            "<i class='ft-edit'></i></a>" +
                            '<input type="checkbox" data-id="' + row.pk + '" class="switchery" ' + checked + '/>'
                    }
                }]
        });
    };
    return {
        //main function to initiate template pages
        init: function () {
            disableUser();
            table();
        }
    };
}();