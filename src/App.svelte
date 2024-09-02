<script lang="ts">
	import MessageBox from "./MessageBox.svelte";
	import MessageBoxHeader from "./MessageBoxHeader.svelte";
	import MessageInput from "./MessageInput.svelte";
	import Sidebar from "./Sidebar.svelte";
</script>

<div class="w-svw h-svh flex bg-noble-black-700 overflow-hidden">
	<!-- <Sidebar /> -->
	<div class="flex flex-col flex-1">
		<!-- <MessageBoxHeader /> -->
		<MessageBox />
		<MessageInput />
	</div>
</div>
