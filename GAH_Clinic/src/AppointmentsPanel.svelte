<script>
  import { onMount } from "svelte";
  import Card from "./Card.svelte";

  let upcomingAppointments = [];
  let errorMessage = '';
  let isLoading = true;

  onMount(async () => {
    const tokenString = localStorage.getItem("jwt");
    if (tokenString) {
      const token = JSON.parse(tokenString);
      try {
        const response = await fetch("http://localhost:8000/user/appointments/", {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        if (!response.ok) {
          if (response.status === 401) {
            throw new Error('Authorization failed. Please login again');
          } else if (response.status === 500) {
            throw new Error('Server error. Please try again later');
          }
        throw new Error('Failed to fetch appointments');
        }

        const result = await response.json();
        if (result.status !== "success" || !Array.isArray(result.appointments)) {
          console.log("Error or unexpected format in response:", result);
          throw new Error('Data format error: Expected an array of appointments.');
        }
        upcomingAppointments = result.appointments;
      } catch (err) {
        console.error(err.message);
        upcomingAppointments = [];
      } finally {
        isLoading = false;
      }
  } else {
    errorMessage = 'No authentication token found. Please login';
  }
});
</script>

<Card>
  <h2>Próximas Consultas</h2>
  <div class="appointments">
    {#if isLoading}
      <div class="spinner"></div>
    {:else if errorMessage}
      <p class="error">{errorMessage}</p>
    {:else if upcomingAppointments.length === 0}
      <p class="info">Não tens nenhuma consulta agendada.</p>
    {:else}
      {#each upcomingAppointments as appointment}
        <div class="appointment">
          {appointment.date} às {appointment.time} com {appointment.doctorName}
        </div>
      {/each}
    {/if}
  </div>
</Card>

<style>
  .appointments {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: flex-start;
  }
  .appointment {
    background: #f0f0f0;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 10px;
    width: 500px;
    text-align: left;
    box-sizing: border-box;
  }
  .spinner {
    border: 4px solid rgba(0,0,0,0.1);
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border-left-color: #09f;
    animation: spin 1s ease infinite;
  }
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  .error, .info {
    text-align: center;
    padding: 20px;
    width: 100%;
  }
</style>
