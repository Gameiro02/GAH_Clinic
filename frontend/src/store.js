import { writable } from 'svelte/store';

export const appointmentsData = writable({
    upcomingAppointments: [],
    pastAppointments: [],
    missingPaymentAppointments: [],
    isLoading: true,
    errorMessage: ''
});

export const doctorsAppointments = writable({
    upcomingAppointments: [],
    pastAppointments: [],
    isLoading: true,
    errorMessage: ''
});

// Doctos data: doctor contains doctor id and doctor name
export const doctorsData = writable({
    doctors: []
});

export const theme = writable('light');