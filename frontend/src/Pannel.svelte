<script>
  import Card from "./Card.svelte";
  import { appointmentsData } from "./store.js";
  import { cardio } from 'ldrs'
  import Button from "./Button.svelte";

  cardio.register();

  $: data = $appointmentsData;
</script>

<div class="card w-96 bg-base-100 shadow-xl">
  <div class="card-body items-center text-center">
    <h2 class="card-title text-base-content text-4xl">Empty</h2>
  </div>
</div>

<div class="card w-96 bg-base-100 shadow-xl">
  <div class="card-body items-center text-center p-5">
    <h2 class="card-title text-base-content text-4xl">Próximas Consultas</h2>
    <div class="appointments">
      {#if data.isLoading}
        <div class="spinner-container">
          <l-cardio
            size="150"
            stroke="10"
            speed="0.7"
            color="oklch(var(--bc))"
          ></l-cardio>
        </div>
      {:else if data.errorMessage}
        <p class="error">{data.errorMessage}</p>
      {:else if data.upcomingAppointments.length === 0}
        <p class="info">Não tens nenhuma consulta agendada.</p>
      {:else}
        <div class="overflow-x-auto w-full">
          <table class="table w-full bg-base-200">
            <thead class="border-b-2 border-base-content text-white">
              <tr>
                <th>Data</th>
                <th>Hora</th>
                <th>Médico</th>
              </tr>
            </thead>
            <tbody>
              {#each data.upcomingAppointments as appointment, index}
                <tr class="hover:bg-base-300">
                  <td class="text-base-content">{appointment.date}</td>
                  <td class="text-base-content">{appointment.time}</td>
                  <td class="text-base-content">{appointment.doctorName}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      {/if}
    </div>
  </div>
</div>

<div class="card w-96 bg-base-100 shadow-xl">
  <div class="card-body items-center text-center p-5">
    <h2 class="card-title text-base-content text-4xl">Histórico de Consultas</h2>
    <div class="appointments">
      {#if data.isLoading}
        <div class="spinner-container">
          <l-cardio
            size="150"
            stroke="10"
            speed="0.7"
            color="oklch(var(--bc))"
          ></l-cardio>
        </div>
      {:else if data.errorMessage}
        <p class="error">{data.errorMessage}</p>
      {:else if data.pastAppointments.length === 0}
        <p class="info">Não tens nenhuma consulta histórica.</p>
      {:else}
        <div class="overflow-x-auto w-full">
          <table class="table w-full bg-base-200">
            <thead class="border-b-2 border-base-content text-white">
              <tr>
                <th>Data</th>
                <th>Hora</th>
                <th>Médico</th>
              </tr>
            </thead>
            <tbody>
              {#each data.pastAppointments as appointment, index}
                <tr class="hover:bg-base-300">
                  <td class="text-base-content">{appointment.date}</td>
                  <td class="text-base-content">{appointment.time}</td>
                  <td class="text-base-content">{appointment.doctorName}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      {/if}
    </div>
  </div>
</div>

<style>
  .card {
    flex: 1;
    padding: 1rem 1rem;
    margin: 0.5rem;
    position: relative;
  }

  .appointments {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    min-height: 200px;
    width: 100%;
    margin: 20px auto;
    padding: 0 10px;
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
