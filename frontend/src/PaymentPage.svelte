<script>
  import Navbar from "./Navbar.svelte";
  let amount = "50.00"; // Valor predefinido que será mostrado no campo amount
  let paymentMethod = "";
  let vatNumber = "";
  let phoneNumber = "";
  let entity = "11111"; // Entidade fixa para todos os pagamentos Multibanco
  let reference = ""; // Referência que será gerada
  let errorMessage = ""; // Mensagem de erro para validação

  function generateRandomReference() {
    return Math.floor(100000000 + Math.random() * 900000000).toString();
  }

  function processPayment() {
    errorMessage = ""; // Limpar mensagens de erro anteriores

    if (paymentMethod === "MBWay") {
      if (!isValidInput(phoneNumber, 9)) {
        errorMessage = "Invalid phone number.";
        return;
      }
      console.log(
        "Processing MBWay payment of $",
        amount,
        "with phone number",
        phoneNumber
      );
    }

    if (paymentMethod === "Multibanco") {
      if (!isValidInput(vatNumber, 9)) {
        errorMessage = "VAT number must be exactly 9 digits.";
        return;
      }
      reference = generateRandomReference();
      console.log(
        "Processing Multibanco payment of $",
        amount,
        "Entity:",
        entity,
        "Reference:",
        reference
      );
    }
    // Logic to send invoice via email after payment confirmation
  }

  function isValidInput(value, length) {
    return value.length === length && /^\d+$/.test(value);
  }
</script>

<Navbar />

<form on:submit|preventDefault={processPayment}>
  {#if errorMessage}
    <p style="color: red;">{errorMessage}</p>
  {/if}

  <label for="amount">Amount:</label>
  <input
    id="amount"
    type="number"
    min="0"
    step="0.01"
    bind:value={amount}
    placeholder="Enter amount"
    required
    disabled
  />

  <label for="payment-method">Payment Method:</label>
  <select id="payment-method" bind:value={paymentMethod} required>
    <option value="">Select payment method</option>
    <option value="MBWay">MBWay</option>
    <option value="Multibanco">Multibanco</option>
  </select>

  {#if paymentMethod === "MBWay"}
    <label for="phone-number">Phone Number:</label>
    <input
      id="phone-number"
      type="tel"
      bind:value={phoneNumber}
      placeholder="Enter phone number"
      required
    />
  {/if}

  <label for="vat-number">VAT Number (or mark as final consumer):</label>
  <input
    id="vat-number"
    type="text"
    bind:value={vatNumber}
    placeholder="Enter VAT number or leave blank"
  />

  {#if paymentMethod === "Multibanco"}
    <p>Entity: {entity}</p>
    <p>Reference: {reference}</p>
  {/if}

  <button type="submit">Pay</button>
</form>

<style>
  form {
    display: flex;
    flex-direction: column;
    max-width: 300px;
    margin: auto;
  }
  input,
  select,
  button {
    margin: 0.5em 0;
    padding: 0.5em;
  }
</style>
