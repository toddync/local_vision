<script lang="ts">
	//@ts-nocheck
	import { AlertCircle, ChevronDown, Copy } from "lucide-svelte";
	import MessageImage from "./MessageImage.svelte";

	export let message = {
		text: "",
		images: [],
	};
</script>

<div
	class="rounded-2xl border-noble-black-600 border-[3px] border-solid flex flex-col p-4 gap-6"
>
	<header class="flex w-full h-fit gap-1 relative">
		{#if message.from != "user"}
			<!-- content here -->
			<img
				class="size-12 rounded-full my-auto"
				src={message.from == "user" ? "user.svg" : "ai.png"}
				alt=""
			/>
			<span class="flex size-fit my-auto gap-5 text-noble-black-400">
				<b>LLaVa</b>
				<!-- <sup class="text-xs">13sec ago</sup> -->
			</span>
		{/if}
		<button
			class="rounded-md size-fit ml-auto p-2 bg-transparent hover:bg-noble-black-400/20 cursor-pointer group absolute right-0"
			on:click={() => navigator.clipboard.writeText(message.text)}
		>
			<Copy
				class="rotate-180 size-4 stroke-noble-black-400 group-hover:stroke-lime-500 transition-all"
			/>
		</button>
	</header>
	<main class="flex flex-col py-2 gap-6 max-w-full md:pl-10">
		<i class="font-medium text-noble-black-200 not-italic">{message.text}</i
		>
		{#if message.images.length}
			<div class="grid gap-8 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
				{#each message.images as src}
					<MessageImage {src} />
				{/each}
			</div>
		{/if}
		<!-- <div class="hidden">
			<span
				class="flex size-fit gap-3 text-xs text-noble-black-300 *:cursor-pointer *:gap-1.5"
			>
				<button class="rounded-lg bg-noble-black-600 flex px-3">
					<AlertCircle class="w-4 my-auto stroke-noble-black-400" />
					<p class="font-semibold text-noble-black-300">
						Regenerate response
					</p>
				</button>
				<button class="rounded-lg bg-noble-black-600 flex px-3">
					<p class="font-semibold text-noble-black-300">Modify</p>
					<ChevronDown class="w-4 my-auto stroke-noble-black-400" />
				</button>
			</span>
		</div> -->
	</main>
</div>
