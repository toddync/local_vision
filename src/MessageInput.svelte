<script>
	//@ts-nocheck
	import { Mic, Paperclip, Send, X } from "lucide-svelte";
	import { writable } from "svelte/store";
	import { messageBox, messages } from "./lib/messageStore";

	let message = writable({
		text: "",
		images: [],
	});

	let input = null;
	let img = null;

	function send() {
		if (!$message.text && $message.images.length == 0) return;
		input.focus();
		console.log($message.images[0]);
		$messages.push({ text: $message.text, images: $message.images });
		$messages = $messages;
		$message.text = "";
		$message.images = [];
		setTimeout(() => {
			$messageBox.scrollTop = $messageBox.scrollHeight;
		}, 100);
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
	class="rounded-xl bg-noble-black-800 flex flex-col py-3 px-6 mx-6 mb-2 text-base text-noble-black-500 font-body-s-semibold"
>
	<div
		data-len={$message.images.length > 0 ? true : null}
		class="grid grid-cols-3 h-0 data-[len]:h-40 data-[len]:pb-6 transition-height duration-500 ease-in-out overflow-hidden"
	>
		{#each $message.images as src, i}
			<div
				class="max-h-40 relative flex hover:bg-noble-black-400/5 p-3 transition-all rounded-2xl"
			>
				<button
					class="absolute top-0 right-0 bg-noble-black-600 rounded"
					on:click={() => {
						$message.images.splice(i, 1);
						$message.images = $message.images;
					}}
				>
					<X class="stroke-noble-black-400" />
				</button>
				<img {src} class="shrink max-h-40 mx-auto" alt="" />
			</div>
		{/each}
	</div>

	<div class="flex flex-1 gap-6">
		<Mic class="w-6 my-auto text-noble-black-400  hidden" />
		<div class="flex-1 flex">
			<!-- svelte-ignore a11y-autofocus -->
			<input
				class="text-base bg-transparent text-noble-black-200 placeholder:text-noble-black-400 size-full outline-none"
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
				class="my-auto size-6 text-noble-black-400 group-hover:stroke-lime-500 transition-all"
			/>
		</button>

		<button
			class="rounded-full bg-noble-black-600 flex p-3 cursor-pointer group"
			on:click={send}
		>
			<Send
				class="w-6 my-auto mx-auto text-noble-black-400 group-hover:stroke-lime-500 transition-all"
			/>
		</button>
	</div>
</footer>
