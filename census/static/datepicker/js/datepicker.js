$(document).ready(function () {
    // This request is made to populate the initial set of events
    // when the page loads
    $.ajax({
        url: '/events/',
        method: 'GET',
        dataType: 'json',
        headers: {
            credentials: 'include'
        },
        success: function (data) {
            render_event_template(data.events);
        }
    });
});

$(function () {
    $('#datepicker').datepicker({
        inline: true,
        showOtherMonths: true,
        dayNamesMin: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],

        // Event that fires on selecting a specific date
        onSelect: function (dateText, inst) {
            $.ajax({
                url: '/events/',
                method: 'GET',
                data: {
                    isMonthly: false,
                    day: inst.selectedDay,
                    month: inst.selectedMonth + 1,
                    year: inst.selectedYear,
                },
                dataType: 'json',
                success: function (data) {
                    render_event_template(data.events);
                }
            });
        },

        // Event that fires when the user switches to the next/prev month
        onChangeMonthYear: function (year, month, inst) {
            $.ajax({
                url: '/events/',
                method: 'GET',
                data: {
                    isMonthly: true,
                    month: inst.selectedMonth + 1,
                    year: inst.selectedYear,
                },
                dataType: 'json',
                success: function (data) {
                    render_event_template(data.events);
                }
            });
        }
    });
});

function render_event_template(events) {
    if (!$.isEmptyObject(events)) {
        render_events(events);
    } else {
        render_no_events();
    }
}

function render_no_events() {
    /*
    Render a dialog box to display a message if no events are found
     */

    $('#event-list').empty();
    $('#no-events-alert').show();
}

function render_events(events) {
    /*
    Iterate through a list of events and generate HTML to create collapsible
    event boxes (e.g. https://designsystem.digital.gov/components/accordion/)
     */
    $('#event-list').empty();
    $('#no-events-alert').hide();
    for (var month in events) {
        if (events.hasOwnProperty(month)) {
            for (var j = 0; j < events[month].length; j++) {
                var priv = events[month][j].is_private_event ? "(PRIVATE)" : ""
                var label = "<label class='usa-label' for='title'>" + events[month][j].start_date + " " + events[month][j].start_time + "</label>";
                var h2 = "<h2 class='usa-accordion__heading'>" +
                    "<button class='usa-accordion__button' aria-expanded='true' aria-controls='a" + events[month][j].id +
                    "'>" + events[month][j].title + priv + "</button>" + "</h2>"
                var div = "<div id='a" + events[month][j].id + "' class='usa-accordion__content usa-prose'>" +
                    "<p>" + events[month][j].description + "</p>" + "</div>";
                $('#event-list').append(label);
                $('#event-list').append(h2);
                $('#event-list').append(div);
            }
        }
    }
}
