<script>
	import '../../app.pcss';
	import '../styles.css';
	let isLoaded = $state(false);

	$effect(() => {
		isLoaded = true;
	});
</script>

<div class="h-screen w-screen">
	<!-- {#if !isLoaded}
		<div class=" grid h-full w-full place-content-center bg-black">
			<img class="m-auto scale-150" src="200w.gif" alt="loading" />
		</div>
	{:else} -->
	<main>
		<slot />
	</main>
	<!-- {/if} -->
</div>

<style lang="scss">
</style>
