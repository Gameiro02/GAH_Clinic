<script>
    let selectedSpecialty = '';
    let selectedDoctor = '';
    let selectedDate = '';
    let selectedTime = '';

    async function scheduleAppointment() {
        try {
            const tokenString = localStorage.getItem("jwt");
            if (tokenString) {
                const token = JSON.parse(tokenString);

                // Get date and time from the form
                const specialty = selectedSpecialty;
                const doctor = selectedDoctor;
                const date = new Date(selectedDate).toISOString().slice(0, 10);  // Gets 'YYYY-MM-DD'
                const timeParts = selectedTime.split(':');
                const time = timeParts.length === 2 ? `${selectedTime}:00` : selectedTime;  // Ensures 'HH:mm:ss'
                
                const requestData = JSON.stringify({
                    specialty,
                    doctor,
                    date,
                    time
                });

                console.log("Request data:", requestData)

                const response = await fetch("http://localhost:8000/book-appointment/", {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: requestData
                });

                if (!response.ok) {
                    throw new Error('Failed to schedule appointment');
                }

                console.log("Appointment scheduled successfully");
            }
            
        } catch (error) {
            console.error("Error scheduling appointment:", error.message);
        }
    }

</script>

<div>
    <h1>Schedule an Appointment</h1>
</div>

<form on:submit|preventDefault={scheduleAppointment}>
    <label for="specialty">Specialty:</label>
    <input id="specialty" type="text" bind:value={selectedSpecialty} required>

    <label for="doctor">Doctor:</label>
    <input id="doctor" type="text" bind:value={selectedDoctor} required>

    <label for="date">Date:</label>
    <input id="date" type="date" bind:value={selectedDate} required>

    <label for="time">Time:</label>
    <input id="time" type="time" bind:value={selectedTime} required>

    <button type="submit">Set Appointment</button>
</form>

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