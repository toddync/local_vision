<script lang="ts">
	//@ts-nocheck
	import { AlertCircle, ChevronDown, Copy } from "lucide-svelte";
	import MessageImage from "./MessageImage.svelte";

	export let message = {
		text: "",
		images: [],
	};

	("https://d1xzdqg8s8ggsr.cloudfront.net/66d0cda62408ec967bf49655/fb57bae7-c701-429a-8363-1563aee7c5b4_1725018654862709769?Expires=-62135596800&Signature=a0NsztgbF0pXzZVL7M-vXDBs1~QuUnTYQbQsQTf29XJk7WyQFoAXLbTbDrmucjg11weKgx9mmP9iWdGd-GV2VPww8-6APV1MNNV~zTyB80ExwyhY5AkE4oDEvxJlP5gMe82XaWmLBm3v3BFJd07lJ3n7hByqnyJUJqYWXbwq7ZwWjU4fayV9ghoKI70dAGZWgOn1xHN~MKuRr0W~v2OZ5GpDqnNA8g2JJ5L2Q0pdqG-2HK2GPlou-4CpzCPtIZnMZ-QUCOYVX6RQE-N-Xi69X20Vu1Qm-L4cWoivDA6Hfh0TU2VPV6cKJQl02yllGmmv6qeAALbwONsMe42VHSutIw__&Key-Pair-Id=K1P54FZWCHCL6J");
</script>

<div
	class="rounded-2xl border-noble-black-600 border-[3px] border-solid flex flex-col p-4 gap-6"
>
	<div class="flex w-full h-fit">
		<img class="size-12 my-auto" src="user.svg" alt="" />
		<div class="flex size-fit my-auto gap-5 text-noble-black-400">
			<span class="font-semibold">Ryan Lee</span>
			<span class="text-xs">13sec ago</span>
		</div>
		<button
			class="rounded-md size-fit ml-auto p-2 bg-transparent hover:bg-noble-black-400/20 cursor-pointer"
		>
			<Copy class="rotate-180 size-4 stroke-noble-black-400" />
		</button>
	</div>
	<div class="flex flex-col py-2 gap-6 max-w-full md:pl-10">
		<div class="font-medium text-noble-black-200">
			{message.text}
		</div>
		<div class="grid gap-8 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
			{#each message.images as src}
				<MessageImage {src} />
			{/each}
		</div>

		<div class="hidden">
			<div class="flex size-fit gap-3 text-xs text-noble-black-300">
				<button
					class="rounded-lg bg-noble-black-600 flex px-3 gap-1.5 cursor-pointer"
				>
					<AlertCircle class="w-4 my-auto stroke-noble-black-400" />
					<p class="font-semibold text-noble-black-300">
						Regenerate response
					</p>
				</button>
				<button
					class="rounded-lg bg-noble-black-600 flex px-3 gap-1.5 cursor-pointer"
				>
					<p class="font-semibold text-noble-black-300">Modify</p>
					<ChevronDown class="w-4 my-auto stroke-noble-black-400" />
				</button>
			</div>
		</div>
	</div>
</div>
