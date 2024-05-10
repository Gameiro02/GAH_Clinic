import { writable } from 'svelte/store';

export const appointmentsData = writable({
    upcomingAppointments: [],
    pastAppointments: [],
    missingPaymentAppointments: [],
    isLoading: true,
    errorMessage: ''
});