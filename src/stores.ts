import { writable, type Writable } from 'svelte/store';

export let loginFormData: Writable<{ username: string; password: string }> = writable({
	username: '',
	password: ''
});
