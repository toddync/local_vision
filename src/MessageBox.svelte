<script>
	//@ts-nocheck
	import { messages, messageBox } from "./lib/messageStore";
	import Message from "./Message.svelte";
</script>

<section
	class="h-full overflow-y-scroll flex flex-col p-5 gap-4"
	bind:this={$messageBox}
>
	{#each $messages as message}
		<Message {message} />
	{/each}
</section>
