<script>
    import { DOMAIN } from "./config.js";

    export let appointment;
    export let showModal = false;
    let isLoading = false;
    let sucessfullMessage = "";
    let errorMessage = "";

    function close() {
        showModal = false;
        sucessfullMessage = "";
        errorMessage = "";
        isLoading = false;
    }

    async function makePayment(appointment_id) {
        isLoading = true;
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
                    if (response.status === 409) {
                        throw new Error('Payment already made');
                    }
                    throw new Error('Failed to make payment');
                }

                sucessfullMessage = "Pagamento realizado com sucesso";
                console.log("Payment made successfully");
            }

        } catch (error) {
            if (error.message === 'Payment already made') {
                errorMessage = "Pagamento já realizado";
            } else {
                errorMessage = "Erro ao realizar pagamento";
            }
        } finally {
            isLoading = false;
        }
    }

</script>

{#if showModal}
    <dialog class="modal" open>
        <div class="modal-box flex flex-col">
            <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2" on:click={close}>X</button>
            <h3 class="flex-grow font-bold text-primary text-center text-3xl">Pagar consulta</h3>
            <div class="text flex-grow">
                <p class="pt-4 text-center font-bold text-xl">Consulta de <span class="text-secondary font-bold">{appointment.specialty}</span> com <span class="text-secondary font-bold">Dr. {appointment.doctorId}</span></p>
                <p class="pt-2 text-center text-gray text-s pb-5">Agendada para o dia <span class="text-secondary font-bold">{appointment.date}</span> às <span class="text-secondary font-bold">{appointment.time}</span> horas</p>
            </div>
            {#if !sucessfullMessage}
                {#if isLoading}
                    <div class="spinner-container flex items-center justify-center h-12 mt-auto">
                        <l-cardio
                            size="60"
                            stroke="4"
                            speed="0.7"
                            color="oklch(var(--s))"
                        ></l-cardio>
                    </div>
                {:else}
                    {#if errorMessage}
                        <p class="text-center flex items-center justify-center mt-auto text-error font-bold text-l mb-3">{errorMessage}</p>
                    {/if}
                    <button class="btn btn-primary h-12 flex items-center justify-center mt-auto" on:click={() => makePayment(appointment.appointmentId)}>Pagar</button>
                {/if}
            {:else}
                <p class="text-center flex items-center justify-center mt-auto text-accent font-bold text-2xl">{sucessfullMessage}</p>
            {/if}
        </div>
    </dialog>
{/if}