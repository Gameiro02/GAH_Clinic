<script>
  import {
    getCalendarDaysWith35Spaces,
    getMonthNumber,
    getMonthName,
  } from "./functions_calendar.js";
  import Card from "./Card.svelte";

  let currentDate = new Date();

  let month = getMonthName(currentDate.getMonth() + 1);
  let year = currentDate.getFullYear();
  let days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  let calendarDays = Array(35).fill(null);

  const handlePrevious = () => {
    console.log("Going to the previous month (<)");

    // get the month number
    let monthNumber = getMonthNumber(month);

    // if the month is January, then go to December of the previous year
    if (monthNumber === 1) {
      month = "December";
      year--;
    } else {
      month = getMonthName(monthNumber - 1);
    }

    calendarDays = getCalendarDaysWith35Spaces(month, year);
  };

  const handleNext = () => {
    console.log("Going to the next month (>)");

    // get the month number
    let monthNumber = getMonthNumber(month);

    // if the month is December, then go to January of the next year
    if (monthNumber === 12) {
      month = "January";
      year++;
    } else {
      month = getMonthName(monthNumber + 1);
      console.log(month);
    }

    calendarDays = getCalendarDaysWith35Spaces(month, year);
  };

  calendarDays = getCalendarDaysWith35Spaces(month, year);
</script>

<div class="calendar">
  <Card>
    <div class="calendar-header">
      <h2>{month} {year}</h2>
      <div>
        <button on:click={handlePrevious}>&lt;</button>
        <button on:click={handleNext}>&gt;</button>
      </div>
    </div>

    <div class="weekdays">
      {#each days as day}
        <span style="font-weight: bold">{day}</span>
      {/each}
    </div>

    <div class="days">
      {#each calendarDays as day, i}
        {#if day >= 24 && i <= 6}
          <span style="color: lightgray">{day}</span>
        {:else}
          <span>{day}</span>
        {/if}
      {/each}
    </div>
  </Card>
</div>

<style>
  button {
    background: none;
    border: none;
    height: 30px;
    width: 25px;
    cursor: pointer;
    width: 30px;
    border-radius: 50%;
    font-size: 25px;
  }

  h2 {
    display: inline;
  }

  .calendar-header {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
    justify-content: space-between;
  }

  .weekdays,
  .days {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    font-size: 11px;
    align-items: center;
    justify-items: center;
  }

  .weekdays {
    margin-bottom: 10px;
  }

  .days {
    grid-auto-rows: minmax(30px, auto);
  }
</style>
