$(function () {
    $('#datepicker').datepicker({
        inline: true,
        showOtherMonths: true,
        dayNamesMin: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],

        // Event that is triggered when user selects a specific date
        onSelect: function (dateText, inst) {
            data = {
                isMonthly: false,
                day: inst.selectedDay,
                month: inst.selectedMonth + 1,
                year: inst.selectedYear,
            };
            search_string = getQueryParams('search');
            if (search_string !== false) {
                data['search'] = search_string;
            }

            redirectUrl(data);
        },

        // Event that is triggered when the user switches to the next/prev month
        onChangeMonthYear: function (year, month, inst) {
            data = {
                isMonthly: true,
                month: inst.selectedMonth + 1,
                year: inst.selectedYear,
            };
            search_string = getQueryParams('search');
            if (search_string !== false) {
                data['search'] = search_string;
            }
            redirectUrl(data);
        },
        defaultDate: getSelectedDate(),
    });
});

function getQueryParams(name) {
    var results = new RegExp('[\?&]' + name + '=([^&#]*)')
        .exec(window.location.search);

    return (results !== null) ? results[1] || 0 : false;
}

function getSelectedDate() {
    if (!window.location.search) {
        return new Date();
    }
    var date = new Date();
    if (getQueryParams('year') !== false
        && getQueryParams('month') !== false) {
        if (getQueryParams('isMonthly') == 'true') {
            date = new Date(getQueryParams('year'),
                getQueryParams('month') - 1, 1);
        } else if (getQueryParams('day') !== false) {
            date = new Date(getQueryParams('year'),
                getQueryParams('month') - 1,
                getQueryParams('day'));
        }
    }
    return date;
}

function redirectUrl(query_params) {
    window.location = "/?" + $.param(query_params);
}
