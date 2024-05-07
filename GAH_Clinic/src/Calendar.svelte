<script>
  import { appointmentsData } from './store.js'; 
  import Card from "./Card.svelte";
  import {
    getCalendarDaysWith35Spaces,
    getMonthNumber,
    getMonthName,
  } from "./functions_calendar.js";

  let currentDate = new Date();
  let month = getMonthName(currentDate.getMonth() + 1);
  let year = currentDate.getFullYear();
  let days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

  // Reactive subscription to appointments data
  $: data = {
    ...$appointmentsData,
    appointments: $appointmentsData.upcomingAppointments.concat($appointmentsData.pastAppointments)
  };

  // Function to populate calendar days
  function populateCalendarDays(month, year) {
    let rawDays = getCalendarDaysWith35Spaces(month, year);
    return rawDays.map(day => {
      let fullDate = `${year}-${('0' + (getMonthNumber(month))).slice(-2)}-${('0' + day).slice(-2)}`;
      let appointmentForDay = data.appointments.find(app => app.date === fullDate);
      return {
        day,
        appointment: appointmentForDay ? {...appointmentForDay} : null
      };
    });
  };

  // Reactive declaration to update calendar days
  $: calendarDays = populateCalendarDays(month, year);

  // Navigation functions
  const handlePrevious = () => {
    let monthNumber = getMonthNumber(month);
    if (monthNumber === 1) {
      month = "December";
      year--;
    } else {
      month = getMonthName(monthNumber - 1);
    }
    // No need to set calendarDays here since it's reactively set by the $: calendarDays declaration
  };

  const handleNext = () => {
    let monthNumber = getMonthNumber(month);
    if (monthNumber === 12) {
      month = "January";
      year++;
    } else {
      month = getMonthName(monthNumber + 1);
    }
    // No need to set calendarDays here since it's reactively set by the $: calendarDays declaration
  };
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
      {#each calendarDays as {day, appointment}}
        <span class={appointment ? 'appointment' : ''} title={appointment ? `${appointment.time} with ${appointment.doctorName}` : ''}>
          {day}
        </span>
      {/each}
    </div>
  </Card>
</div>

<style>
  button {
    background: none;
    border: none;
    height: 30px;
    width: 30px;
    cursor: pointer;
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

  .appointment {
    color: #007BFF; /* Blue color for days with appointments */
    cursor: pointer;
    font-weight: bold;
  }
</style>
