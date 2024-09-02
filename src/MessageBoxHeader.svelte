<script>
	import { Folder, MessageCircle, Pyramid } from "lucide-svelte";
	import Part5 from "./Part5.svelte";
</script>

<section
	class="m-3 mb-0 rounded-xl bg-noble-black-800 flex flex-col p-2 text-noble-black-300 font-body-s-semibold"
>
	<Part5 />
	<div class="gap-6 px-5 mt-3 hidden">
		<div>
			<div class="flex gap-3">
				<Pyramid class="h-5 stroke-lime-400" />
				<p class="font-semibold my-auto">Artificium</p>
			</div>
			<div class="h-1 bg-lime-400 rounded mt-4" />
		</div>
		<div>
			<div class="flex gap-3">
				<MessageCircle class="h-5" />

				<p class="font-semibold my-auto">Chat</p>
			</div>
			<div class="h-1 bg-lime-400 rounded mt-4 hidden" />
		</div>
		<div>
			<div class="flex gap-3">
				<Folder class="h-5" />
				<p class="font-semibold my-auto">Library</p>
			</div>
			<div class="h-1 bg-lime-400 rounded mt-4 hidden" />
		</div>
	</div>
</section>
