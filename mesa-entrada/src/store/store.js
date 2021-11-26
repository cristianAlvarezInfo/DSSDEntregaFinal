import { writable } from 'svelte/store'

export const cookies = writable(localStorage.getItem('cookies') || '');
export const token = writable(localStorage.getItem('token') || '');
export const userID = writable(localStorage.getItem('userID') || -1);
export const idProcess = writable(localStorage.getItem('idProcess') || -1);
export const isLoggedUser = writable(localStorage.getItem('isLoggedUser') || false);    

cookies.subscribe(value => {
    localStorage.setItem('cookies', value);
})
token.subscribe(value => {
    localStorage.setItem('token', value);
})
userID.subscribe(value => {
    localStorage.setItem('userID', value);
})
idProcess.subscribe(value => {
    localStorage.setItem('idProcess', value);
})
isLoggedUser.subscribe(value => {
    localStorage.setItem('isLoggedUser', value);
})

