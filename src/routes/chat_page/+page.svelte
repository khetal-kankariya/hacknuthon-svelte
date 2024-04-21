<script lang="ts">
	import Button from '$lib/components/ui/button/button.svelte';
	import { slide } from 'svelte/transition';

	let inputMode: 'audio' | 'text' | 'default' = $state('default');
	let isListening = $state(false);
	let recognition: SpeechRecognition | undefined;
	let chatStarted = $state(false);
	let text_input = $state('');

	let userRole: 1 | 2 = $state(1);
	let useMode: 'train' | 'interview' | null = $state(null);
	let isUseModeChosen = $state(false);
	let avatarSize = $state(700);

	let questions: string[] = $state([
		'For what job post you are hiring for?',
		'How much experience do you have?'
	]);
	let responses: string[] = $state([]);

	let chats: { text: string; type: 'question' | 'response' }[] = $state([]);

	let ques_resp_obj: Object;
	let numberOfQuestionsAsked = 0;

	let toStop = false;

	function speak(text: string) {
		if ('speechSynthesis' in window) {
			const speech = new SpeechSynthesisUtterance(text);
			window.speechSynthesis.speak(speech);
		} else {
			console.error('Speech synthesis not supported');
		}
	}

	const startChat = () => {
		sendChat('question', questions[0]);
		chatStarted = true;
	};

	function sendChat(type: 'question' | 'response', text: string) {
		isListening = false;
		if (text == '') return;

		if (type == 'question' && questions) questions.shift();

		chats = [...chats, { text: text, type: type }];
	}

	function stopListening() {
		recognition?.stop();
		text_input = '';
	}

	function startListening() {
		if (!('webkitSpeechRecognition' in window)) {
			alert('Speech recognition not supported in this browser.');
			return;
		}

		// function speechrecognition(recognition) {}

		if (!recognition) {
			recognition = new webkitSpeechRecognition();
			recognition.interimResults = false;
			recognition.continuous = false;

			// Handle speech recognition results
			recognition.onresult = (event: SpeechRecognitionEvent) => {
				const result = event.results[0][0].transcript;
				text_input = result;
			};

			// Handle speech recognition errors
			recognition.onerror = (event: SpeechRecognitionError) => {
				console.error('Speech recognition error:', event.error);
			};

			// Handle end of speech recognition
			recognition.onspeechend = () => {
				stopListening();
			};
		}

		recognition.start();
	}

	function startSpeaking() {
		console.log('yapp');
	}

	function stopSpeaking() {
		console.log('stop the yapp');
	}

	function responseSubmitted(
		event: SubmitEvent & {
			currentTarget: HTMLFormElement;
		}
	) {
		event.preventDefault();
		sendChat('response', text_input);
		event.currentTarget.reset();
	}

	function chatSubmit() {
		console.log('raaahhhh');
	}

	$effect(() => {
		if (chats[chats.length - 1]?.type == 'response') {
			if (chats[chats.length - 1].text.toLowerCase() == 'stop') {
				chatSubmit();
			}
			if (questions.length != 0) {
				sendChat('question', questions[0]);
			}

			if (questions.length == 0) sendChat('question', 'Next question');
		}
	});

	$effect(() => {
		if (isListening) {
			inputMode = 'audio';
			startListening();
		} else {
			inputMode = 'default';
			stopListening();
		}
	});
</script>

<div class="grid h-screen w-screen place-content-center bg-[#000]">
	{#if userRole == 1 && isUseModeChosen == false}
		<form
			onsubmit={(e) => {
				isUseModeChosen = true;
				e.preventDefault();
			}}
			class="flex flex-col items-center gap-16"
		>
			<h1 class="text-3xl">What do you want to do?</h1>
			<div class="mx-auto flex gap-4">
				<label for="train" class="rounded-xl border border-white p-8 text-2xl">
					<input type="radio" name="usemode" id="train" /> <span>Train</span>
				</label>
				<label for="interview" class="rounded-xl border border-white p-8 text-2xl">
					<input type="radio" name="usemode" id="interview" />
					<span>Mock Interview</span>
				</label>
			</div>
			<Button variant="default" class="mx-auto  rounded-xl px-8" type="submit">Let's begin</Button>
		</form>
	{:else}
		<div class="flex h-screen w-screen flex-col">
			<div class="_avatar w-full flex-[4] items-end transition-all" class:flex-\[2\]={chatStarted}>
				<div class="flex w-full items-end justify-center">
					<video src="alhamdulillah.mp4" autoplay loop width={avatarSize} muted></video>
				</div>
			</div>

			{#if !chatStarted}
				<Button class="mx-auto w-52 rounded-xl" onclick={startChat}>Start Chat</Button>
			{:else}
				<!-- Chats -->
				<div class="mx-auto w-4/5" transition:slide={{ axis: 'y' }}>
					{#each chats as chat}
						<div
							class="chat"
							class:chat-start={chat.type == 'question'}
							class:chat-end={chat.type == 'response'}
							transition:slide={{ axis: 'y' }}
						>
							<span class="chat-bubble">{chat.text}</span>
						</div>
					{/each}
				</div>

				<!-- Input area -->
				<div class="flex w-full">
					<form
						onsubmit={responseSubmitted}
						class="m-auto flex min-w-[600px] items-center justify-between align-middle"
					>
						{#if inputMode == 'text'}
							<input
								type="text"
								class="w-full rounded-full border-none bg-[#333] px-4 py-2 text-xl"
								id="chat_input"
								name="chat_input"
								bind:value={text_input}
							/>
							<div class="mic rounded-full bg-cyan-500">
								{#if text_input.length == 0}
									<button
										class="mic-logo border-none p-2"
										onclick={() => {
											isListening = true;
											inputMode = 'audio';
										}}
									>
										<svg
											height="32"
											viewBox="0 0 512 512"
											width="32"
											xmlns="http://www.w3.org/2000/svg"
										>
											<g>
												<path
													fill="#fff"
													d="M256,353.5c43.7,0,79-37.5,79-83.5V115.5c0-46-35.3-83.5-79-83.5c-43.7,0-79,37.5-79,83.5V270   C177,316,212.3,353.5,256,353.5z"
												/>
												<path
													fill="#fff"
													d="M367,192v79.7c0,60.2-49.8,109.2-110,109.2c-60.2,0-110-49-110-109.2V192h-19v79.7c0,67.2,53,122.6,120,127.5V462h-73v18   h161v-18h-69v-62.8c66-4.9,117-60.3,117-127.5V192H367z"
												/>
											</g>
										</svg>
									</button>
								{:else}
									<button type="submit" class="p-2">
										<svg
											height="32"
											width="32"
											viewBox="0 0 24 24"
											xmlns="http://www.w3.org/2000/svg"
										>
											<g id="icons">
												<path
													fill="white"
													d="M21.5,11.1l-17.9-9C2.7,1.7,1.7,2.5,2.1,3.4l2.5,6.7L16,12L4.6,13.9l-2.5,6.7c-0.3,0.9,0.6,1.7,1.5,1.2l17.9-9   C22.2,12.5,22.2,11.5,21.5,11.1z"
													id="send"
												>
												</path></g
											>
										</svg>
									</button>
								{/if}
							</div>
						{:else if inputMode == 'audio'}
							<div class="flex w-full flex-col items-center">
								<input
									bind:value={text_input}
									class="pointer-events-none w-full rounded-full border-none bg-none px-4 py-2 text-xl outline-none"
									id="chat_input"
								/>

								<div class="flex flex-shrink">
									<div class="stop rounded-full bg-red-500">
										<button type="submit" class="m-2 rounded-full border-none p-4">
											<div class="pointer-events-none aspect-square h-4 bg-white"></div>
										</button>
									</div>
									<div class="cancel rounded-full bg-destructive">
										<button
											class="m-2 rounded-full border-none p-3"
											onclick={() => {
												text_input = '';
												isListening = false;
											}}
											><svg
												height="24"
												viewBox="0 0 20 20"
												width="24"
												xmlns="http://www.w3.org/2000/svg"
												><g
													fill="none"
													fill-rule="evenodd"
													id="Page-1"
													stroke="none"
													stroke-width="1"
													><g
														fill="#ffffff"
														id="Core"
														transform="translate(-380.000000, -44.000000)"
														><g id="cancel" transform="translate(380.000000, 44.000000)"
															><path
																d="M10,0 C4.5,0 0,4.5 0,10 C0,15.5 4.5,20 10,20 C15.5,20 20,15.5 20,10 C20,4.5 15.5,0 10,0 L10,0 Z M15,13.6 L13.6,15 L10,11.4 L6.4,15 L5,13.6 L8.6,10 L5,6.4 L6.4,5 L10,8.6 L13.6,5 L15,6.4 L11.4,10 L15,13.6 L15,13.6 Z"
																id="Shape"
															></path></g
														></g
													></g
												></svg
											>
										</button>
									</div>
								</div>
							</div>
						{:else}
							<div>
								<div class="pointer-events-none opacity-0"></div>
							</div>
							<div class="mic rounded-full bg-cyan-500 p-2">
								<button
									class="mic-logo border-none p-2"
									onclick={() => {
										isListening = true;
									}}
								>
									<svg
										height="32"
										viewBox="0 0 512 512"
										width="32"
										xmlns="http://www.w3.org/2000/svg"
									>
										<g>
											<path
												fill="#fff"
												d="M256,353.5c43.7,0,79-37.5,79-83.5V115.5c0-46-35.3-83.5-79-83.5c-43.7,0-79,37.5-79,83.5V270   C177,316,212.3,353.5,256,353.5z"
											/>
											<path
												fill="#fff"
												d="M367,192v79.7c0,60.2-49.8,109.2-110,109.2c-60.2,0-110-49-110-109.2V192h-19v79.7c0,67.2,53,122.6,120,127.5V462h-73v18   h161v-18h-69v-62.8c66-4.9,117-60.3,117-127.5V192H367z"
											/>
										</g>
									</svg>
								</button>
							</div>
							<div class="keyboard">
								<button
									class="keyboard-logo rounded-full p-2"
									onclick={() => {
										isListening = false;
										inputMode = 'text';
									}}
								>
									<svg
										viewBox="0 0 576 512"
										xmlns="http://www.w3.org/2000/svg"
										height="24"
										width="24"
									>
										<path
											fill="white"
											d="M512 64H64C28.65 64 0 92.65 0 128v256c0 35.35 28.65 64 64 64h448c35.35 0 64-28.65 64-64V128C576 92.65 547.3 64 512 64zM528 384c0 8.822-7.178 16-16 16H64c-8.822 0-16-7.178-16-16V128c0-8.822 7.178-16 16-16h448c8.822 0 16 7.178 16 16V384zM140 152h-24c-6.656 0-12 5.344-12 12v24c0 6.656 5.344 12 12 12h24c6.656 0 12-5.344 12-12v-24C152 157.3 146.7 152 140 152zM196 200h24c6.656 0 12-5.344 12-12v-24c0-6.656-5.344-12-12-12h-24c-6.656 0-12 5.344-12 12v24C184 194.7 189.3 200 196 200zM276 200h24c6.656 0 12-5.344 12-12v-24c0-6.656-5.344-12-12-12h-24c-6.656 0-12 5.344-12 12v24C264 194.7 269.3 200 276 200zM356 200h24c6.656 0 12-5.344 12-12v-24c0-6.656-5.344-12-12-12h-24c-6.656 0-12 5.344-12 12v24C344 194.7 349.3 200 356 200zM460 152h-24c-6.656 0-12 5.344-12 12v24c0 6.656 5.344 12 12 12h24c6.656 0 12-5.344 12-12v-24C472 157.3 466.7 152 460 152zM140 232h-24c-6.656 0-12 5.344-12 12v24c0 6.656 5.344 12 12 12h24c6.656 0 12-5.344 12-12v-24C152 237.3 146.7 232 140 232zM196 280h24c6.656 0 12-5.344 12-12v-24c0-6.656-5.344-12-12-12h-24c-6.656 0-12 5.344-12 12v24C184 274.7 189.3 280 196 280zM276 280h24c6.656 0 12-5.344 12-12v-24c0-6.656-5.344-12-12-12h-24c-6.656 0-12 5.344-12 12v24C264 274.7 269.3 280 276 280zM356 280h24c6.656 0 12-5.344 12-12v-24c0-6.656-5.344-12-12-12h-24c-6.656 0-12 5.344-12 12v24C344 274.7 349.3 280 356 280zM460 232h-24c-6.656 0-12 5.344-12 12v24c0 6.656 5.344 12 12 12h24c6.656 0 12-5.344 12-12v-24C472 237.3 466.7 232 460 232zM400 320h-224C167.1 320 160 327.1 160 336V352c0 8.875 7.125 16 16 16h224c8.875 0 16-7.125 16-16v-16C416 327.1 408.9 320 400 320z"
										></path></svg
									>
								</button>
							</div>
						{/if}
					</form>
				</div>
			{/if}
		</div>
	{/if}
</div>
