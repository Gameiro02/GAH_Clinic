<script>
  import Card from "./Card.svelte";
  import { appointmentsData } from "./store.js";

  $: data = $appointmentsData;
</script>

<Card>
  <h2>Próximas Consultas</h2>
  <div class="appointments">
    {#if data.isLoading}
      <div class="spinner-container">
        <div class="spinner"></div>
      </div>
    {:else if data.errorMessage}
      <p class="error">{data.errorMessage}</p>
    {:else if data.upcomingAppointments.length === 0}
      <p class="info">Não tens nenhuma consulta agendada.</p>
    {:else}
      {#each data.upcomingAppointments as appointment}
        <div class="appointment">
          {appointment.date} às {appointment.time} com {appointment.doctorName}
        </div>
      {/each}
    {/if}
  </div>
</Card>

<Card>
  <h2>Histórico de Consultas</h2>
  <div class="appointments">
    {#if data.isLoading}
      <div class="spinner-container">
        <div class="spinner"></div>
      </div>
    {:else if data.errorMessage}
      <p class="error">{data.errorMessage}</p>
    {:else if data.pastAppointments.length === 0}
      <p class="info">Não tens nenhuma consulta histórica.</p>
    {:else}
      {#each data.pastAppointments as appointment}
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
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
    min-height: 200px;
    width: 100%;
    margin: 20px auto;
    padding: 0 10px;
    box-sizing: border-box;
  }

  .appointment {
    background: #f0f0f0;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 10px;
    width: calc(100% - 20px);
    text-align: left;
    box-sizing: border-box;
  }

  .spinner-container {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    flex-grow: 1;
  }

  .spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border-left-color: #09f;
    animation: spin 1s ease infinite;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  .error,
  .info {
    text-align: center;
    padding: 20px;
    width: 100%; /* Assegura que texto de erro e informação preenchem a largura */
    color: red; /* Cor para mensagens de erro */
  }

  .info {
    color: #666; /* Cor menos proeminente para mensagens informativas */
  }
</style>
