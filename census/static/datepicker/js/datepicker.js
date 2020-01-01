(function ($) {
    /*
    jQuery's datepicker widget contains a property called 'beforeShow',
    useful for when we need to make any additional calls before the widget
    is loaded. However, there seems to be a bug due to which the property
    doesn't seem to register. I've included the code snippet below to add it
    to the widget, and we can possibly get rid of it in the future when
    the jQuery library is updated.
     */
    $.extend($.datepicker, {

        // Reference the orignal function so we can override it and call it later
        _inlineDatepicker2: $.datepicker._inlineDatepicker,

        // Override the _inlineDatepicker method
        _inlineDatepicker: function (target, inst) {

            // Call the original
            this._inlineDatepicker2(target, inst);

            let beforeShow = $.datepicker._get(inst, 'beforeShow');

            if (beforeShow) {
                beforeShow.apply(target, [target, inst]);
            }
        }
    });
}(jQuery));

$(function () {
    $('#datepicker').datepicker({
        inline: true,
        showOtherMonths: true,
        dayNamesMin: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
        beforeShow: function () {
            let date = getSelectedDate();
            highlightMonthEvents(date.getMonth() + 1, date.getFullYear());
        },

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
            }
            redirectUrl(data);
        },
        defaultDate: getSelectedDate(),
    });
});

function highlightMonthEvents(month, year) {
    /*
    Given a month and year, highlight days with events
    Note: Month provided in the argument is 1-indexed
    and not 0-indexed as is normally used in JavaScript.
     */
    $.ajax({
        url: '/',
        method: 'GET',
        data: {
            isMonthly: true,
            month: month,
            year: year,
        },
        headers: {
            credentials: 'include'
        },
        dataType: 'json',
        success: function (data) {
            let eventDates = data.dates;

            $('#datepicker').find(`[data-month='`+(month-1)+`']`)
                .find("a").filter(function () {
                return eventDates.indexOf($(this).text()) > -1;
            }).addClass('ui-datepicker-active-events');
        }
    });
}

