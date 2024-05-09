import { writable } from 'svelte/store';

export const appointmentsData = writable({
    upcomingAppointments: [],
    pastAppointments: [],
    isLoading: true,
    errorMessage: ''
});