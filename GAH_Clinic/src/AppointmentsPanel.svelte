<script>
  import Card from "./Card.svelte";

  let upcomingAppointments = [
    {
      date: "10/05/2024",
      time: "14:00",
      doctor: "Dr. Ana Silva",
    },
    {
      date: "12/05/2024",
      time: "09:00",
      doctor: "Dr. Carlos Pereira",
    },
  ];
</script>

<Card>
  <h2>Próximas Consultas</h2>
  <div class="appointments">
    {#each upcomingAppointments as appointment}
      <div class="appointment">
        {appointment.date} às {appointment.time} com {appointment.doctor}
      </div>
    {/each}
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
    box-sizing: border-box; /* Garante que o padding não afete o tamanho total */
  }
</style>
