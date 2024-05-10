<script>
    import { navigate } from "svelte-routing";

    let username = "";
    let password = "";
    let errorMessage = "";
  
    async function handleLogin() {
      try {
        const response = await fetch("http://localhost:8000/login/", {
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
      }
    }
  </script>

<div class="flex justify-center items-center h-screen">
  <div class="card w-96 shrink-0 flex flex-col justify-center max-w-sm shadow-2xl bg-base-200">
    <form class="card-body flex justify-center items-center w-full" on:submit|preventDefault={handleLogin}>
      <h2 class="card-title text-secondary text-3xl mb-2 mt-4">Login</h2>
      <div class="form-control">
        <label class="label">
          <span class="label-text">Username</span>
        </label>
        <input type="username" placeholder="username" class="input input-bordered" bind:value={username} required />
      </div>
      <div class="form-control">
        <label class="label">
          <span class="label-text">Password</span>
        </label>
        <input type="password" placeholder="password" class="input input-bordered" bind:value={password} required />
      </div>
      <div class="form-control mt-6">
        <button class="btn btn-primary text-lg">Login</button>
      </div>
      {#if errorMessage}
       <div class="error font-bold text-error alert-error mt-4">{errorMessage}</div>
      {/if}
    </form>
  </div>
</div>