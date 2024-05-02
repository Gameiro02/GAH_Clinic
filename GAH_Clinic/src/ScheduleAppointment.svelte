<script>
    let selectedDate = '';
    let selectedTime = '';

    function scheduleAppointment() {
        // Add logic to schedule an appointment
        console.log("Appointment set for", selectedDate, "at", selectedTime);
    }
</script>

<style>
    form {
        display: flex;
        flex-direction: column;
        max-width: 300px;
        margin: auto;
    }
    input, button {
        margin: 0.5em 0;
        padding: 0.5em;
    }
</style>

<form on:submit|preventDefault={scheduleAppointment}>
    <label for="date">Date:</label>
    <input id="date" type="date" bind:value={selectedDate} required>

    <label for="time">Time:</label>
    <input id="time" type="time" bind:value={selectedTime} required>

    <button type="submit">Set Appointment</button>
</form>