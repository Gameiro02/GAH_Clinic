<script>
  import Card from "./Card.svelte";

  let pastAppointments = [
    {
      date: "01/04/2024",
      time: "10:00",
      doctor: "Dr. Sofia Martins",
    },
    {
      date: "15/03/2024",
      time: "16:00",
      doctor: "Dr. Luís Costa",
    },
  ];
</script>

<Card>
  <h2>Histórico de Consultas</h2>
  <div class="appointments">
    {#each pastAppointments as appointment}
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
