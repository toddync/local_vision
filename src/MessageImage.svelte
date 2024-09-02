<script>
	import { MoreVertical } from "lucide-svelte";
	export let src = "";
</script>

<div class="rounded-2xl relative flex">
	<img class="w-full my-auto mx-auto" {src} alt="" />
	<div class="hidden">
		<div
			class="size-10 absolute top-1 right-1 bg-gradient-to-b from-noble-black-700 to-noble-black-500 rounded-lg flex"
		>
			<MoreVertical
				class="size-5 mx-auto my-auto stroke-noble-black-200"
			/>
		</div>
	</div>
</div>
