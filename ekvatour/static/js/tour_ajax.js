$(document).ready(function () {
    console.log("ready")
    let _cities = []
    let _options = []


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

    function load_start_info() {

        $.each($('#id_cities label'), function (index, value) {
            c = {
                name: $(value).text().split('\n')[0],
                id: $(value).children().attr("value")
            }
            _cities.push(c)
        });

        $.each($('#id_options label'), function (index, value) {
            o = {
                name: $(value).text().split('\n')[0],
                id: $(value).children().attr("value")
            }
            _options.push(c)
        });


    }

    load_start_info();


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


                data_list = JSON.parse(data_list);
                _cities = data_list
                $("#id_cities label").remove();
                data_list.forEach(city => {
                    $("#id_cities").append(`
                        <label class="check-div">` + city.name +
                        `<input type="checkbox" value="` + city.id + `">
                            <span class="checkmark"></span>
                        </label>`)
                });
            },
            error: function (d) {
                console.log(d);
            }
        });
    });
    var a;

    $('.search-button').on('click', function (e) {
        e.preventDefault();
        var city_list = [];
        var options_list = [];
        var nutrition_list = [];
        var categories_list = [];

        $("#id_cities input:checked").each(function () {
            city_list.push($(this).val());
        })
        $("#id_options input:checked").each(function () {
            options_list.push($(this).val());
        })
        $("#id_eats input:checked").each(function () {
            nutrition_list.push($(this).val());
        })
        $("#id_categories input:checked").each(function () {
            categories_list.push($(this).val());
        })
        data = {
            country: $("#id_country option:selected").val(),
            tour_type: $("#id_tour").val(),
            city_list: city_list,
            options_list: options_list,
            nutrition_list: nutrition_list,
            categories_list: categories_list,
            departure_date_start: $("#id_departure_date_start").val(),
            departure_date_end: $("#id_departure_date_end").val(),
            days_min: $("#id_days_min").val(),
            days_max: $("#id_days_max").val(),
            number_of_adults: $("#id_number_of_adults").val(),
            number_of_child: $("#id_number_of_child").val(),
        }
        console.log(data)
        $.ajax({
            url: 'filtertours/',
            method: 'POST',
            data: data,
            success: function (response) {
                response = JSON.parse(response);

                if (response.length > 0) {
                    $(".serach_results tbody").children().remove()
                    response.forEach(tour => {
                        console.log(tour)
                        var fields = tour.fields;
                        var city_name = _cities.find(x => x.id == fields.city).name;
                        var options_name_list = [];
                        var departure_date = new Date(fields.departure_date);
                        var arrival_date = new Date(fields.arrival_date);
                        var Difference_In_Days = (arrival_date - departure_date) / (1000 * 3600 * 24);
                        for (var o in fields.tour_options) {
                            options_name_list.push(_options.find(x => x.id == o))
                        }
                        var markup = `
                        <tr onclick="open_modal_to_buy('${city_name}(Krasnoyarsk)','${fields.cost}',${tour.pk})">
                        <td><p>${fields.departure_date}</p>
                            <p><i class="fas fa-clock"></i> ${fields.departure_time}</p></td>
                        <td>${city_name} (Krasnoyarsk)</td>
                        <td>${Difference_In_Days} <span class="people-span">+1</span></td>
                        <td>${fields.hotel_name} ${fields.tour_category} </td>
                        <td>${fields.accommodation_number}</td>
                        <td>${fields.tour_nutrition}</td>
                        <td><i class="fas fa-users"></i> <i class="fas fa-child"></i>
        
                        </td>
                        <td>${fields.arrival_date}</td>
                        <td><span class="cost-span">${Intl.NumberFormat('ru-RU').format(fields.cost)} ₽</span></td>
                    </tr>`
                        console.log(markup)
                        $(".serach_results tbody").append(markup);
                    });

                    $(".serach_results").show();
                    $("#no_tours").hide();
                } else {
                    $(".serach_results").hide();
                    $("#no_tours").show();
                }

            },
            error: function (d) {
                console.log(d);
                $("#no_tours").show();
            }
        });
    });

    $('.search-button').click();


    /* 1. Visualizing things on Hover - See next part for action on click */
    $('#stars_review li').on('mouseover', function () {
        var onStar = parseInt($(this).data('value'), 10); // The star currently mouse on

        // Now highlight all the stars that's not after the current hovered star
        $(this).parent().children('li.star').each(function (e) {
            if (e < onStar) {
                $(this).addClass('hover');
            } else {
                $(this).removeClass('hover');
            }
        });

    }).on('mouseout', function () {
        $(this).parent().children('li.star').each(function (e) {
            $(this).removeClass('hover');
        });
    });


    /* 2. Action to perform on click */
    $('#stars_review li').on('click', function () {
        var onStar = parseInt($(this).data('value'), 10); // The star currently selected
        var stars = $(this).parent().children('li.star');

        for (i = 0; i < stars.length; i++) {
            $(stars[i]).removeClass('selected');
        }

        for (i = 0; i < onStar; i++) {
            $(stars[i]).addClass('selected');
        }
        $("#start_rating").attr("value", onStar)

    });


});


function responseMessage(msg) {
    $('.success-box').fadeIn(200);
    $('.success-box div.text-message').html("<span>" + msg + "</span>");
}

function open_modal_to_buy(tour_name, tour_cost, id) {
    $("#bronirovano").hide();
    $("#modal_tour_name").text(tour_name);
    $("#modal_tour_cost").text(Intl.NumberFormat('ru-RU').format(tour_cost));
    $("#tour_id").attr("value", id)
    $('#TourGetModal').modal('toggle');
}

function open_review(id) {
    $("#start_rating").attr("value", 1)
    $("#reserved_id").attr("value", id)
    $("#review_text").val("")
    $('#reviewModal').modal('toggle');

    var stars = $('#stars_review').children('li.star');

    for (i = 0; i < stars.length; i++) {
        $(stars[i]).removeClass('selected');
        $(stars[i]).removeClass('hover');
    }

}
