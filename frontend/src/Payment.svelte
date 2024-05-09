<!-- src/Payment.svelte -->
<script>
    let amount = '';

    function processPayment() {
        // Add logic to process payment
        console.log("Processing payment of $", amount);
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

<form on:submit|preventDefault={processPayment}>
    <label for="amount">Amount:</label>
    <input id="amount" type="number" min="0" step="0.01" bind:value={amount} placeholder="Enter amount" required>

    <button type="submit">Pay</button>
</form>