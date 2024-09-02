<script>
	import {
		Circle,
		CreditCard,
		Search,
		Settings,
		Square,
		Triangle,
	} from "lucide-svelte";
	import ChatName from "./ChatName.svelte";
</script>

<div class="px-4 h-svh font-body-s-semibold text-stone-400 min-w-[314px] flex">
	<div
		class="rounded-xl bg-noble-black-800 flex flex-col h-[98svh] my-auto w-full"
	>
		<div class="flex flex-col py-6 px-2 gap-6">
			<p class="pl-4 font-semibold">GENERAL</p>
			<div class="flex flex-col gap-2 text-sm text-noble-black-100">
				<div class="rounded-lg flex py-3 px-4 gap-4">
					<div class="h-5 flex-1 flex gap-4">
						<Search class="text-noble-black-400" />
						<div class="font-semibold size-fit my-auto">Search</div>
					</div>
					<div
						class=" shadow-[0px_1px_2px_-1px_rgba(0,_0,_0,_0.05),_0px_1px_3px_rgba(0,_0,_0,_0.05)] rounded [background:linear-gradient(117.58deg,_rgba(215,_237,_237,_0.16),_rgba(205,_235,_235,_0))] border-glass-stroke border-[1px] border-solid box-border flex flex-row items-center justify-end py-0.5 pl-1.5 pr-[7px] text-xs text-noble-black-300 font-inter"
					>
						<div
							class="relative tracking-[0.15px] leading-[18px] inline-block min-w-[23px] whitespace-nowrap"
						>
							<span class="font-semibold">⌘</span>
							<span class="font-semibold font-body-s-semibold">
								S</span
							>
						</div>
					</div>
				</div>
				<div class="rounded-lg flex py-3.5 px-4 gap-4">
					<div class="flex w-full gap-4">
						<CreditCard class="my-auto text-noble-black-400" />
						<p class="font-semibold">Billing</p>
					</div>
				</div>
			</div>
		</div>
		<div class="bg-noble-black-500 h-0.5 w-[90%] rounded mx-auto" />
		<div class="flex flex-col flex-1 px-2 gap-6">
			<div class="flex px-4">
				<p class="font-semibold">PROJECTS</p>
			</div>

			<ChatName active>
				<Square class="text-lime-400 my-auto stroke-2" />
				<p class="size-fit my-auto font-semibold">Orbital Oddysey</p>
			</ChatName>

			<ChatName>
				<Triangle class="text-red-600 my-auto stroke-2" />
				<p class="size-fit my-auto font-semibold">
					Digital Product Launch
				</p>
			</ChatName>

			<ChatName>
				<Square class="text-orange-600 my-auto stroke-2" />
				<p class="size-fit my-auto font-semibold">Brand Refresh</p>
			</ChatName>

			<ChatName>
				<Circle class="text-cyan-400 my-auto stroke-2" />
				<p class="size-fit my-auto font-semibold">
					Social Media Strategy
				</p>
			</ChatName>

			<button
				class="cursor-pointer [border:none] py-3.5 px-4 bg-[transparent] self-stretch rounded-lg flex flex-row items-center justify-start gap-4 hidden"
			>
				<button
					class="cursor-pointer [border:none] py-0 pl-0 pr-[114px] bg-[transparent] flex-1 flex flex-row items-center justify-start gap-4"
				>
					<img
						class="h-5 w-5 relative min-h-[20px]"
						loading="lazy"
						alt=""
						src="/public/pluscircle.svg"
					/>

					<div
						class="relative text-sm tracking-[0.15px] leading-[20px] font-semibold font-body-s-semibold text-noble-black-400 text-center inline-block"
					>
						Add new project
					</div>
				</button>
				<div
					class="shadow-[0px_1px_2px_-1px_rgba(0,_0,_0,_0.05),_0px_1px_3px_rgba(0,_0,_0,_0.05)] rounded [background:linear-gradient(117.58deg,_rgba(215,_237,_237,_0.16),_rgba(205,_235,_235,_0))] border-glass-stroke border-[1px] border-solid flex py-0.5 pl-1.5 pr-[7px]"
				>
					<div class="text-xs text-noble-black-300 flex p-0.5 gap-1">
						<span class="font-semibold font-inter">⌘</span>
						<span class="font-semibold font-body-s-semibold">
							S</span
						>
					</div>
				</div>
			</button>
		</div>
		<div class="h-24 p-2 text-noble-black-0">
			<div
				class="rounded-2xl [background:linear-gradient(117.58deg,_rgba(215,_237,_237,_0.16),_rgba(205,_235,_235,_0))] border-glass-stroke border-t-[1px] border-solid flex p-4 gap-5"
			>
				<div class="flex gap-4">
					<img
						class="size-12 rounded-full my-auto"
						src="https://d1xzdqg8s8ggsr.cloudfront.net/66d0cda62408ec967bf49655/a0c8d374-880e-468b-924d-10e5a5842108_1725018559356739593?Expires=-62135596800&Signature=oZEKVimt0YItI1VapN8Ai5O-lXTfLIcYiOrOY3ZqfT5mJqSm~MCtjuPF59zXG4geb3~VH4MojCU8-~CaMvoNbE9cHeFQh-KhiO9k42oOfQEOKS9vCQnxHl5k55l2SGhvmK0H2iVf6hKAx75q3ZGIEwlqD933lPnv2aUQC4-5LuxWEf1Hc2GU8o-XFvOpRr2Cvf9R3li-m4ghDE5ctd23MU24KjvXd5UCNMXnkUNW137ffLGg5lLJAWL1CUZyHyOwK8Vzp-1UlsR7S2dl7EHSYR11SAwWC2Ef9De7UXoVrSq383ARWxUs9ofZ8Wi1nszBvnkMT15WlXMw5Od0zG0oIA__&Key-Pair-Id=K1P54FZWCHCL6J"
						alt=""
					/>
					<div class="flex flex-col gap-1.5 my-auto">
						<span class="font-semibold">Ryan Lee</span>
						<span class="text-lightgreen"> Premium </span>
					</div>
				</div>
				<Settings class="ml-auto my-auto stroke-noble-black-400 w-6" />
			</div>
		</div>
	</div>
</div>
