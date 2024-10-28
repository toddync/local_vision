<script>
	//@ts-nocheck
	import { Mic, Paperclip, Send, X } from "lucide-svelte";
	import { writable } from "svelte/store";
	import { messageBox, messages } from "./lib/messageStore";
	import context from "./context";

	let message = writable({
		text: "",
		images: [],
	});

	let input = null;
	let img = null;

	function send() {
		if (!$message.text && $message.images.length == 0) return;
		input.focus();
		$messages.push({
			text: $message.text,
			images: $message.images,
			from: "user",
		});
		$messages = $messages;

		res();

		setTimeout(() => {
			$messageBox.scrollTop = $messageBox.scrollHeight;
		}, 100);
	}

	async function res() {
		const data = {
			model: "llava-phi3",
			prompt: $message.text || "",
			stream: false,
			context: $context,
		};

		if ($message.images.length)
			data.images = $message.images.map((img) => img.split(",")[1]);
		$message.text = "";
		$message.images = [];

		let url = "https://cae9-44-204-28-144.ngrok-free.app";

		try {
			const response = await fetch(`${url}/api/generate`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify(data),
			});
			if (!response.ok) return;
			let description = await response.json();

			$context = description.context;

			$messages[$messages.length] = {
				text: description.response,
				images: [],
			};
			$messages = $messages;
			setTimeout(() => {
				$messageBox.scrollTop = $messageBox.scrollHeight;
			}, 100);
		} catch (e) {}
	}

	async function getBase64(file) {
		var reader = new FileReader();
		reader.readAsDataURL(file);
		input.focus();
		reader.onload = function () {
			if ($message.images.length == 3) $message.images.splice(0, 1);
			$message.images.push(reader.result);
			$message.images = $message.images;
		};
	}
</script>

<footer
	class="flex flex-col px-6 py-3 mx-6 mb-2 text-base rounded-xl bg-noble-black-800 text-noble-black-500 font-body-s-semibold"
>
	<div
		data-len={$message.images.length > 0 ? true : null}
		class="grid grid-cols-3 gap-5 h-0 data-[len]:h-40 data-[len]:pb-6 transition-height duration-500 ease-in-out overflow-hidden"
	>
		{#each $message.images as src, i}
			<div
				class="relative flex p-3 transition-all max-h-40 hover:bg-noble-black-400/5 rounded-2xl"
			>
				<button
					class="absolute top-0 right-0 rounded bg-noble-black-600"
					on:click={() => {
						$message.images.splice(i, 1);
						$message.images = $message.images;
					}}
				>
					<X class="stroke-noble-black-400" />
				</button>
				<img
					{src}
					class="max-w-full max-h-full mx-auto my-auto"
					alt=""
				/>
			</div>
		{/each}
	</div>

	<div class="flex flex-1 gap-6">
		<Mic class="hidden w-6 my-auto text-noble-black-400" />
		<div class="flex flex-1">
			<!-- svelte-ignore a11y-autofocus -->
			<input
				class="text-base bg-transparent outline-none text-noble-black-200 placeholder:text-noble-black-400 size-full"
				placeholder="Type here..."
				bind:value={$message.text}
				on:keydown={(e) => e.key == "Enter" && send()}
				bind:this={input}
				autofocus
			/>
			<input
				class="hidden"
				bind:this={img}
				type="file"
				accept="image/png, image/jpeg"
				on:input={(e) => getBase64(e.target.files[0])}
			/>
		</div>

		<button
			class="bg-transparent cursor-pointer group"
			on:click={() => img.click()}
		>
			<Paperclip
				class="my-auto transition-all size-6 text-noble-black-400 group-hover:stroke-lime-500"
			/>
		</button>

		<button
			class="flex p-3 rounded-full cursor-pointer bg-noble-black-600 group"
			on:click={send}
		>
			<Send
				class="w-6 mx-auto my-auto transition-all text-noble-black-400 group-hover:stroke-lime-500"
			/>
		</button>
	</div>
</footer>
