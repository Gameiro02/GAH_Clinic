<script>
  let selectedSpecialty = '';
  let selectedDoctor = '';
  let selectedDate = '';
  let selectedTime = '';
  let themeColor = 'dark'; // Isto ainda pode ser usado para outras partes do tema, se necessário.
</script>

<button class="btn btn-primary mt-4" onclick="modalSa.showModal()">
  Agendar Consulta
</button>

<dialog id="modalSa" class="modal">
  <div class="card w-full max-w-md bg-base-100 flex-1">
    <div class="card-body items-center text-center p-4">
      <h3 class="text-3xl font-bold text-secondary p-2">Schedule Your Appointment</h3>
      <p class="font-bold text-sm text-base-content">Fill in the details below to set up your appointment.</p>

      <div class="space-y-3 mt-3">
        <div>
          <label for="specialty" class="text-md text-center  font-bold text-accent">Specialty:</label>
          <input id="specialty" type="text" bind:value={selectedSpecialty} class="input input-bordered w-full text-base-content" required>
        </div>

        <div>
          <label for="doctor" class="text-md text-center  font-bold text-accent">Doctor:</label>
          <input id="doctor" type="text" bind:value={selectedDoctor} class="input input-bordered w-full text-base-content" required>
        </div>

        <div>
          <label for="date" class="text-md text-center font-bold text-accent">Date:</label>
          <input id="date" type="date" bind:value={selectedDate} class="input input-bordered w-full text-base-content" required>
        </div>

        <div>
          <label for="time" class="text-md text-center  font-bold text-accent">Time:</label>
          <input id="time" type="time" bind:value={selectedTime} class="input input-bordered w-full text-base-content" required>
        </div>
      </div>

      <div class="modal-action mt-4">
        <form method="dialog">
          <button type="submit" class="btn btn-primary">Set Appointment</button>
        </form>
      </div>
    </div>
  </div>
</dialog>
