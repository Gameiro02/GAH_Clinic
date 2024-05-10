<script>
  import { appointmentsData } from "../store.js";
  import { cardio } from 'ldrs'

  cardio.register();

  $: data = $appointmentsData;
</script>

<div class="card w-96 bg-base-200 shadow-xl flex-1">
  <div class="card-body items-center text-center p-1">
    <h2 class="card-title text-secondary text-3xl mb-2 mt-4">Próximas Consultas</h2>
    <div class="appointments flex flex-col w-full">
      {#if data.isLoading}
        <div class="spinner-container flex items-center justify-center mt-20">
          <l-cardio
            size="150"
            stroke="10"
            speed="0.7"
            color="oklch(var(--s))"
          ></l-cardio>
        </div>
      {:else if data.errorMessage}
        <p class="error">{data.errorMessage}</p>
      {:else if data.upcomingAppointments.length === 0}
        <p class="info">Não tens nenhuma consulta agendada.</p>
      {:else}
        <div class="overflow-y-auto max-h-72">
          <table class="table w-full min-w-full bg-base-200">
            <thead class="border-b-2 border-base-content text-accent">
              <tr>
                <th>Data</th>
                <th>Hora</th>
                <th>Médico</th>
              </tr>
            </thead>
            <tbody>
              {#each data.upcomingAppointments as appointment, index}
                <tr class="hover:bg-primary">
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