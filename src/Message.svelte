<script lang="ts">
	//@ts-nocheck
	import { AlertCircle, ChevronDown, Copy } from "lucide-svelte";
	import MessageImage from "./MessageImage.svelte";

	export let message = {
		text: "",
		images: [],
		from: "ai", // define o remetente como "ai" ou "user"
	};

	export let focus = false;

	// Função para copiar a mensagem para a área de transferência com feedback audível
	function copyMessage() {
		navigator.clipboard.writeText(message.text).then(() => {
			const copiedMessage = document.getElementById("copiedMessage");
			if (copiedMessage) {
				copiedMessage.textContent =
					"Mensagem copiada para a área de transferência.";
				// Usamos aria-live para que o leitor de tela leia a mensagem de feedback
				copiedMessage.setAttribute("aria-live", "assertive");
			}
		});
	}
</script>

<div
	class="rounded-2xl border-noble-black-600 border-[3px] border-solid flex flex-col p-4 gap-6"
>
	<header class="flex w-full h-fit gap-1 relative">
		{#if message.from != "user"}
			<!-- Avatar acessível com descrição de imagem e papel semântico -->
			<img
				class="size-12 rounded-full my-auto"
				src={message.from == "user" ? "user.svg" : "ai.png"}
				alt={message.from == "user"
					? "Avatar do usuário"
					: "Avatar da inteligência artificial"}
				role="img"
			/>
			<span class="flex size-fit my-auto gap-5 text-noble-black-400">
				<b aria-label={message.from == "user" ? "Usuário" : "LLaVa"}>
					{message.from == "user" ? "Usuário" : "LLaVa"}
				</b>
			</span>
		{/if}
		<!-- Botão de cópia com aria-label descritivo e feedback auditivo -->
		<button
			class="rounded-md size-fit ml-auto p-2 bg-transparent hover:bg-noble-black-400/20 cursor-pointer group absolute right-0"
			on:click={copyMessage}
			name="Copiar mensagem para a área de transferência"
			aria-label="Copiar mensagem para a área de transferência"
		>
			<Copy
				class="rotate-180 size-4 stroke-noble-black-400 group-hover:stroke-lime-500 transition-all"
			/>
		</button>
		<!-- Mensagem invisível para feedback de cópia, lida pelo leitor de tela -->
		<div id="copiedMessage" class="sr-only" aria-live="polite"></div>
	</header>
	<main class="flex flex-col py-2 gap-6 max-w-full md:pl-10">
		<!-- Texto da mensagem com atributos ARIA para leitura imediata -->
		<i
			class="font-medium text-noble-black-200 not-italic"
			role="status"
			aria-live="assertive"
			aria-atomic="true"
			aria-selected={focus}
		>
			{message.text}
		</i>
		{#if message.images.length}
			<!-- Lista de imagens com descrição de contexto e papel semântico -->
			<div
				class="grid gap-8 grid-cols-1 md:grid-cols-2 lg:grid-cols-3"
				role="list"
				aria-label="Imagens anexadas à mensagem"
			>
				{#each message.images as src, index}
					<div role="listitem" aria-label={`Imagem ${index + 1}`}>
						<MessageImage
							{src}
							alt={`Imagem da mensagem ${index + 1}`}
						/>
					</div>
				{/each}
			</div>
		{/if}
	</main>
</div>
