<script>
	import { Edit, Share2 } from "lucide-svelte";
</script>

<div
	class="flex text-noble-black-0 border-noble-black-700 border-b-[px] border-solid p-6"
>
	<div class="flex flex-col items-start justify-start gap-1 text-xl">
		<span class="font-bold">Orbital Oddysey</span>
		<div class="text-sm font-medium text-noble-black-300">
			Marketing Campaign for a new TV series Launch
		</div>
	</div>
	<div class="flex flex-col pt-2 text-noble-black-400 ml-auto hidden">
		<div class="flex gap-6 h-full">
			<div class="pt-1">
				<div class="flex">
					<img
						class="h-8 w-8 relative rounded-xl shrink-0"
						alt=""
						src="/public/avatar-11.svg"
					/>

					<img
						class="h-8 w-8 relative rounded-xl shrink-0 z-[1] ml-[-4px]"
						alt=""
						src="/public/avatar-12.svg"
					/>

					<img
						class="h-8 w-8 relative rounded-xl shrink-0 z-[2] ml-[-4px]"
						alt=""
						src="/public/avatar-13.svg"
					/>

					<img
						class="h-8 w-8 relative rounded-xl shrink-0 z-[3] ml-[-4px]"
						loading="lazy"
						alt=""
						src="/public/avatar-14.svg"
					/>

					<div
						class="h-[38px] flex-1 rounded-xl bg-noble-black-600 border-noble-black-800 border-[3px] border-solid box-border overflow-hidden flex flex-row items-start justify-start pt-1.5 px-2 pb-2 shrink-0 z-[4] ml-[-4px]"
					>
						<div
							class="relative tracking-[0.15px] leading-[18px] font-semibold inline-block min-w-[16px]"
						>
							+4
						</div>
					</div>
				</div>
			</div>
			<div class="flex gap-4 text-sm">
				<div class="flex gap-2.5">
					<Share2 class="my-auto w-5" />
					<span class="my-auto font-semibold">Share</span>
				</div>
				<div
					class="size-7 my-auto rounded-3xs bg-noble-black-600 p-1.5"
				>
					<Edit class=" my-auto" />
				</div>
			</div>
		</div>
	</div>
</div>
