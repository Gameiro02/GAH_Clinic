<script>
    import { navigate } from "svelte-routing";
    import logo from "../public/logo.svg";
    import Button from "./Button.svelte";

    let username = "";
    let password = "";
    let errorMessage = "";
  
    async function handleLogin() {
      try {
        const response = await fetch("http://gah-clinic.us-east-1.elasticbeanstalk.com/auth/login/", {
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

  <div class="p-4 max-w-md mx-auto bg-blue-500 text-white rounded-lg shadow-lg">
    Hello, Tailwind CSS!
  </div>
  
  <h2>Login</h2>
  <form class="login-form" on:submit|preventDefault={handleLogin}>
    <img class="logo" src={logo} alt="GAH Logo" />
    <input id="username" type="text" placeholder="User name" bind:value={username} required />
    <input id="password" type="password" placeholder="Password" bind:value={password} required />

    <Button text="Submit"/>
    {#if errorMessage}
      <p class="error">{errorMessage}</p>
    {/if}
  </form>
  
  <style>
    .login-form {
      display: flex;
      flex-direction: column;
      max-width: 300px;
      margin: 20vh auto;
      padding: 2em;
      background: #fff;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      border-radius: 25px;
      align-items: center;
    }

    input {
        background-color: #eee;
    }
  
    input {
      margin: 0.5em 0;
      padding: 0.8em;
      border: 1px solid #ccc;
      border-radius: 4px;
      transition: border-color 0.3s;
    }
    input:focus {
      border-color: #0056b3;
      outline: none;
    }
    
    .error {
      color: red;
    }
  
    img.logo {
      max-width: 100px;
      height: auto;
    }
  </style>