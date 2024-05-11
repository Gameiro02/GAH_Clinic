<script>
    import { navigate } from "svelte-routing";
    import { DOMAIN } from "./config.js";
    import { cardio } from 'ldrs'

  cardio.register();

    let username = "";
    let password = "";
    let errorMessage = "";
    let isLoading = false;
  
    async function handleLogin() {
      isLoading = true;
      try {
        const response = await fetch(`${DOMAIN}/login/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, password }),
        });
  
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || "Failed to login");
        }
  
        const { access, user } = await response.json();
        localStorage.setItem("jwt", JSON.stringify(access));
        localStorage.setItem("user", user);
        navigate("/dashboard");
      } catch (err) {
        errorMessage = err.message;
      } finally {
        isLoading = false;
      }
    }
  </script>

<div class="flex justify-center items-center h-screen">
  <div class="card w-96 shrink-0 flex flex-col justify-center max-w-sm shadow-2xl bg-base-200">
    <form class="card-body flex justify-center items-center w-full" on:submit|preventDefault={handleLogin}>
      <h2 class="card-title text-secondary text-3xl mb-2 mt-4">Login</h2>
      <div class="form-control">
        <label for="username">Username</label>
        <input type="username" placeholder="username" class="input input-bordered" bind:value={username} required />
      </div>
      <div class="form-control">
        <label for="password">Password</label>
        <input type="password" placeholder="password" class="input input-bordered" bind:value={password} required />
      </div>
      <div class="form-control mt-6">
        {#if isLoading}
        <div class="spinner-container">
          <l-cardio
            size="50"
            stroke="4"
            speed="0.7"
            color="oklch(var(--s))"
          ></l-cardio>
        </div>
        {:else}
          <button class="btn btn-primary text-lg">Login</button>
        {/if}
      </div>
      {#if errorMessage}
       <div class="error font-bold text-error alert-error mt-4">{errorMessage}</div>
      {/if}
    </form>
  </div>
</div>