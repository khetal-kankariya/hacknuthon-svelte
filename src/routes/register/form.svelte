<script lang="ts">
	import { enhance } from '$app/forms';
	import Button from '$lib/components/ui/button/button.svelte';
	import * as Form from '$lib/components/ui/form';
	import Input from '$lib/components/ui/input/input.svelte';
	import * as Select from '$lib/components/ui/select';

	let email = '';
	let password = '';
	let role = 2;

	// const { form: formData, enhance } = form;

	async function postData() {
		let newFormData = {
			role: role,
			email: email,
			password: password
		};
		try {
			const response = await fetch('http://localhost:5000/login', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(newFormData)
			});

			if (!response.ok) {
				throw new Error('Failed to post data');
			}

			// const responseData = await response?.json();
			console.log('Response from server:', response);
		} catch (error) {
			console.error('Error posting data:', error);
		}
	}

	async function handleSubmit(
		event: SubmitEvent & { currentTarget: EventTarget & HTMLFormElement }
	) {
		event.preventDefault();

		await postData();
	}
</script>

<form method="post" onsubmit={handleSubmit} class="flex flex-col gap-4">
	<span>Role</span>
	<Select.Root
		name="role"
		onSelectedChange={(v) => {
			v && (role = Number(v.value));
		}}
	>
		<Select.Trigger class="w-[180px]">
			<Select.Value placeholder="Interviewee" />
			<Select.Content>
				<Select.Item value="1">HR Manager</Select.Item>
				<Select.Item value="2">Interviewee</Select.Item>
			</Select.Content>
		</Select.Trigger>
	</Select.Root>

	<label for="email">EMail</label>
	<Input
		id="email"
		type="email"
		placeholder="name@company.com"
		autocomplete="on"
		bind:value={email}
	/>

	<label for="password">Password</label>
	<Input id="password" type="password" placeholder="****" bind:value={password} />

	<Button type="submit" class="w-full">Register</Button>
</form>
