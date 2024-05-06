function getCalendarDaysWith35Spaces(monthNumber, year) {

    let month = getMonthNumber(monthNumber);

    // 1. Create a new Date object for the first day 
    const date = new Date(year, month - 1, 1);

    // 2. Get the day of the week (0 for Sunday, 6 for Saturday)
    const firstDay = date.getDay();
    console.log('firstDay:', firstDay);

    // 3. Get the total number of days in the month
    const daysInMonth = new Date(year, month, 0).getDate();

    // 4. Calculate the total number of empty days needed at the start
    const emptyDays = firstDay % 7;
    console.log('emptyDays:', emptyDays);

    // 5. Clear the array with 35 empty spaces
    let calendarDays = Array(35).fill(null);

    // 6. Fill in the days of the month
    for (let i = 0; i < emptyDays; i++) {
        // if the day is empty, fill it with the previous month's last days
        calendarDays[i] = daysInMonth - emptyDays + i + 1;
    }

    for (let i = 0; i < daysInMonth; i++) {
        // fill the days of the month
        calendarDays[emptyDays + i] = i + 1;
    }

    // Fill in the remaining days with the next month's first days
    for (let i = 0; i < calendarDays.length - daysInMonth - emptyDays; i++) {
        calendarDays[emptyDays + daysInMonth + i] = '';
    }

    return calendarDays;

}

function getMonthNumber(monthOrNumber) {
    // Check if the input is a numeric month (0-11)
    if (typeof monthOrNumber === 'number' && monthOrNumber >= 0 && monthOrNumber <= 11) {
        return monthOrNumber;
    }

    // Check if the input is a month name in English
    const monthNames = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];
    const monthIndex = monthNames.indexOf(monthOrNumber);
    if (monthIndex !== -1) {
        return monthIndex + 1;
    }

    // Invalid input
    throw new Error('Invalid month input: ' + monthOrNumber);
}

function getMonthName(monthNumber) {

    if (typeof monthNumber !== 'number' || monthNumber < 1 || monthNumber > 12) {
        throw new Error('Invalid month number: ' + monthNumber);
    }

    const monthNames = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];
    return monthNames[monthNumber - 1];
}


export { getCalendarDaysWith35Spaces, getMonthNumber, getMonthName };