<script>
    import { DOMAIN } from "./config.js";

    export let appointment;
    export let showModal = false;

    function close() {
        showModal = false;
    }

    async function makePayment(appointment_id) {
        try {
            const tokenString = localStorage.getItem("jwt");
            if (tokenString) {
                const token = JSON.parse(tokenString);

                const requestData = JSON.stringify({
                    appointment_id
                });

                const response = await fetch(`${DOMAIN}/payment/`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: requestData
                });

                if (!response.ok) {
                    throw new Error('Failed to make payment');
                }

                console.log("Payment made successfully");
            }

        } catch (error) {
            console.error("Error making payment:", error.message);
        }
    }

</script>

{#if showModal}
    <dialog class="modal" open>
        <div class="modal-box">
            <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" on:click={close}>X</button>
            <h3 class="font-bold text-primary text-center text-2xl">Pagar Consulta</h3>
            <p class="py-4">Especialidade: {appointment.specialty} with Dr. {appointment.doctorId}</p>
            <button class="btn btn-primary" on:click={() => makePayment(appointment.id)}>Pagar</button>
        </div>
    </dialog>
{/if}