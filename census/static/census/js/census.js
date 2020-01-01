function getQueryParams(name) {
    /*
    Given a query parameter name, this method will parse the current URL
    an extract the value for the param if found else return false
     */
    let results = new RegExp('[\?&]' + name + '=([^&#]*)')
        .exec(window.location.search);

    return (results !== null) ?
        decodeURIComponent(results[1]
                            .replace(/[+]/g,' ')
                            .trim())
        || 0 : false;
}

function getSelectedDate() {
    /*
    Parse date query parameters of current URL and return a date object.
     */
    if (!window.location.search) {
        return new Date();
    }
    let date = new Date();
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
    /*
    Redirect browser to URL with given query params
     */
    window.location = "/?" + $.param(query_params);
}
