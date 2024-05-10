<script>
  let showButton = true;
</script>

<div class="card w-full bg-base-200 shadow-2xl flex-1">
  <div class="card-body flex justify-center items-center w-full">
    {#if showButton}
      <button
        class="btn btn-primary text-lg"
        on:click={() => (showButton = false)}>Agendar Consulta</button
      >
    {:else}
      <div class="space-y-4">
        <label class="input input-bordered flex items-center gap-2">
          <input type="text" class="grow" placeholder="Specialty" />
        </label>
        <select class="select select-bordered w-full max-w-xs">
          <option>1</option>
          <option>2</option>
          <option>3</option>
          <option>4</option>
          <option>5</option>
        </select>
      </div>
    {/if}
  </div>
</div>
