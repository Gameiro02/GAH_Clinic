import { writable } from 'svelte/store';

export const appointmentsData = writable({
    upcomingAppointments: [],
    pastAppointments: [],
    missingPaymentAppointments: [],
    isLoading: true,
    errorMessage: ''
});

export const theme = writable('light');