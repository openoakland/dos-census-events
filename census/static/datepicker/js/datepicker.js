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

    $('form#search-form').submit(function () {
        $(':input', this).each(function () {
            this.disabled = !($(this).val());
        });
    });

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
            $('#form-day').val(inst.selectedDay);
            $('#form-month').val(inst.selectedMonth + 1);
            $('#form-year').val(inst.selectedYear);
            $("#form-isMonthly").val('false');
            $('form#search-form').submit();
        },

        // Event that is triggered when the user switches to the next/prev month
        onChangeMonthYear: function (year, month, inst) {
            $("#form-isMonthly").val('true');
            $('#form-month').val(inst.selectedMonth + 1);
            $('#form-year').val(inst.selectedYear);
            $('form#search-form').submit();

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

            $('#datepicker').find(`[data-month='` + (month - 1) + `']`)
                .find("a").filter(function () {
                    return eventDates.indexOf($(this).text()) > -1;
                }).addClass('ui-datepicker-active-events');
        }
    });
}
