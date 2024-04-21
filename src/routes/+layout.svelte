<script>
	import '../app.pcss';
	let isLoaded = $state(false);

	$effect(() => {
		isLoaded = true;
	});
</script>

<div class="app h-screen w-screen">
	<!-- {#if !isLoaded}
		<div class=" grid h-full w-full place-content-center bg-black">
			<img class="m-auto scale-150" src="200w.gif" alt="loading" />
		</div>
	{:else} -->
	<slot></slot>
	<!-- {/if} -->
</div>

<style lang="scss">
</style>
