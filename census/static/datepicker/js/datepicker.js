$(function () {
    $('#datepicker').datepicker({
        inline: true,
        //nextText: '&rarr;',
        //prevText: '&larr;',
        showOtherMonths: true,
        //dateFormat: 'dd MM yy',
        dayNamesMin: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
        //showOn: "button",
        // buttonImage: "img/calendar-blue.png",
        // buttonImageOnly: true,
        onSelect: function (dateText, inst) {
            $.ajax({
                url: '/events/',
                method: 'GET',
                data: {
                    isMonthly: false,
                    day: inst.selectedDay,
                    month: inst.selectedMonth,
                    year: inst.selectedYear,
                },
                dataType: 'json',
                success: function (data) {
                    var events = data.request.events;
                    render_events(events);


                }
            });
        },
        onChangeMonthYear: function (year, month, inst) {
            $.ajax({
                url: '/events/',
                method: 'GET',
                data: {isMonthly: true, month: inst.selectedMonth, year: inst.selectedYear},
                dataType: 'json',
                success: function (data) {
                    var events = data.request.events;
                    render_events(events);
                }
            });
        }
    });
});

function render_events(events) {
    $('#event-list').empty();
    for (var i = 0; i < events.length; i++) {
        var label = "<label class='usa-label' for='title'>" + events[i].start_time + "</label>"
        var h2 = "<h2 class='usa-accordion__heading'>" +
            "<button class='usa-accordion__button' aria-expanded='true' aria-controls='a" + events[i].id +
            "'>" + events[i].title + "</button>" + "</h2>"
        var div = "<div id='a" + events[i].id + "' class='usa-accordion__content usa-prose'>" +
            "<p>" + events[i].description + "</p>" + "</div>"
        $('#event-list').append(label);
        $('#event-list').append(h2);
        $('#event-list').append(div);
    }
}
