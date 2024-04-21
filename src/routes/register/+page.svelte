<script lang="ts">
	import Form from './form.svelte';

	let authmode: 'signin' | 'signup' = 'signin';
</script>

<div class=" mx-auto flex h-screen flex-col items-center justify-center">
	<div class="login-form w-full rounded-lg shadow sm:max-w-md md:mt-0 xl:p-0">
		<div class="space-y-4 p-6 sm:p-8 md:space-y-6">
			<h1
				class="font-montserrat text-xl font-bold leading-tight tracking-tight text-white md:text-2xl"
			>
				Register
			</h1>
			<Form />
		</div>
	</div>
</div>

<style>
	:global(.login-form) {
		border-radius: 24px;
		box-shadow:
			50px 50px 100px #2e2e2e,
			-50px -50px 100px #000000;
	}
</style>
