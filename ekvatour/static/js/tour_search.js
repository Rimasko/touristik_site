$(document).ready(function () {
    console.log("ready")

    // CSRF code
    function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
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

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $("#id_country").on("change", function () {
        console.log("clicked")
        var value = $("#id_country option:selected").val()
        console.log(value)

        data = {
            "country": value
        }
        $.ajax({
            url: 'city_by_country/',
            method: 'GET',
            data: data,
            success: function (data_list) {

                console.log(data_list);
                data_list = JSON.parse(data_list)
                $("#id_cities label").remove()
                data_list.forEach(city => {
                    $("#id_cities").append(`
                        <label class="check-div">` + city.name +
                            `<input type="checkbox">
                            <span class="checkmark"></span>
                        </label>`)
                });
            },
            error: function (d) {
                console.log(d);
            }
        });
    });

    $('.search-button').on('click', function (e) {
        console.log("clicked")
        // e.preventDefault();
        var $this = $(this),
            data = $this.data();


        $this.hide();
        $.ajax({
            url: 'testajax/',
            method: 'POST',
            data: data,
            success: function (d) {
                console.log(d);
            },
            error: function (d) {
                console.log(d);
            }
        });
    });
});