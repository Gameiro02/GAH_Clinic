<!-- src/Login.svelte -->
<script>
    import { navigate } from 'svelte-routing';
    let username = '';
    let password = '';
    let errorMessage = '';

    async function handleLogin() {
        try {
            const response = await fetch("http://localhost:8000/auth/login/", {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to login');
            }

            const { access, user } = await response.json();
            localStorage.setItem('jwt', JSON.stringify(access));
            localStorage.setItem('user', user);
            navigate('/dashboard');
        } catch (err) {
            errorMessage = err.message; 
        }
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
    .error {
        color: red;
    }
</style>

<form on:submit|preventDefault={handleLogin}>
    <label for="username">Username</label>
    <input id="username" type="text" bind:value={username} required>

    <label for="password">Password</label>
    <input id="password" type="password" bind:value={password} required>

    <button type="submit">Login</button>
    {#if errorMessage}
        <p class="error">{errorMessage}</p>
    {/if}
</form>