<script>
	export let active = null;
</script>

<div
	data-active={active}
	class="rounded-lg data-[active]:[background:linear-gradient(117.58deg,_rgba(215,_237,_237,_0.16),_rgba(205,_235,_235,_0))] border-glass-stroke border-t-[1px] border-solid flex pt-3 px-4 pb-3.5 gap-4"
>
	<div class="flex-1 flex gap-4">
		<slot />
	</div>
</div>
