$(function () {
    $('#datepicker').datepicker({
        inline: true,
        showOtherMonths: true,
        dayNamesMin: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],

        // Event that is triggered when user selects a specific date
        onSelect: function (dateText, inst) {
            let data = {
                isMonthly: false,
                day: inst.selectedDay,
                month: inst.selectedMonth + 1,
                year: inst.selectedYear,
            };
            let search_string = getQueryParams('search');
            if (search_string !== false) {
                data['search'] = search_string;
            }

            redirectUrl(data);
        },

        // Event that is triggered when the user switches to the next/prev month
        onChangeMonthYear: function (year, month, inst) {
            let data = {
                isMonthly: true,
                month: inst.selectedMonth + 1,
                year: inst.selectedYear,
            };
            let search_string = getQueryParams('search');
            if (search_string !== false) {
                data['search'] = search_string;
                console.log(data['search']);
            }
            redirectUrl(data);
        },
        defaultDate: getSelectedDate(),
    });
});
