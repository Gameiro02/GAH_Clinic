<!-- src/Login.svelte -->
<script>
    let username = '';
    let password = '';

    function handleLogin() {
        // Add logic to authenticate user
        console.log("Logging in with", username, password);
    }
</script>

<style>
    form {
        display: flex;
        flex-direction: column;
        max-width: 300px;
        margin: auto;
    }
    input, button {
        margin: 0.5em 0;
        padding: 0.5em;
    }
</style>

<form on:submit|preventDefault={handleLogin}>
    <label for="username">Username</label>
    <input id="username" type="text" bind:value={username} required>

    <label for="password">Password</label>
    <input id="password" type="password" bind:value={password} required>

    <button type="submit">Login</button>
</form>