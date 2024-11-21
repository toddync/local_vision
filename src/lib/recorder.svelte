<script lang="ts">
	//@ts-nocheck
	import { onMount } from "svelte";

	export let codec = 'video/webm;codecs="vp8,opus"';
	export let fps: number = 60;
	export let videoBitrate: number = 2000;
	export let audioBitrate: number = 320;
	export let systemAudio: boolean = true;
	export const useMicrophone: boolean = true;
	export let useTimer: boolean = true;

	type State = "ready" | "ready.countdown" | "recording";
	let recorder: State = "ready";
	let videoStream: MediaStream;
	let audioStream: MediaStream;
	let mediaRecorder: MediaRecorder;
	let chunks: Blob[] = [];
	let timer: number;
	let seconds = 3;

	function kbpsToBits(kbps: number) {
		return kbps * 1000;
	}

	async function getMediaStream() {
		try {
			videoStream = await navigator.mediaDevices.getDisplayMedia({
				video: { frameRate: fps },
				audio: true,
				selfBrowserSurface: "include",
				systemAudio: systemAudio ? "include" : "exclude",
			});
			videoStream.oninactive = stopRecording;
			audioStream = await navigator.mediaDevices.getUserMedia({
				audio: true,
			});
			const [microphone] = audioStream.getAudioTracks();
			videoStream.addTrack(microphone);
			audioStream.oninactive = stopRecording;
		} catch (e) {
			console.error(e);
		}
	}

	async function startRecording() {
		if (useTimer) {
			await countdown();
		}
		recorder = "recording";
		mediaRecorder = new MediaRecorder(videoStream, {
			mimeType: codec,
			videoBitsPerSecond: kbpsToBits(videoBitrate),
			// audioBitsPerSecond: kbpsToBits(audioBitrate),
		});
		mediaRecorder.ondataavailable = (e) => {
			chunks.push(e.data);
			download();
		};
		mediaRecorder.start();
	}

	function stopRecording() {
		recorder = "ready";
		mediaRecorder?.stop();
		clearInterval(timer);
		seconds = 3;
	}

	function countdown(): Promise<number> {
		recorder = "ready.countdown";
		return new Promise((resolve) => {
			timer = setInterval(() => {
				if (seconds === 0) {
					clearInterval(timer);
					resolve(seconds);
				}
				seconds--;
			}, 1000);
		});
	}

	function download() {
		const blob = new Blob(chunks, { type: codec });
		const a = document.createElement("a");
		a.href = URL.createObjectURL(blob);
		a.download = "video.mp4";
		a.click();
		URL.revokeObjectURL(a.href);
		chunks = [];
	}

	async function handleKeydown(event: KeyboardEvent) {
		switch (event.key) {
			case "R":
				if (recorder === "ready") {
					await getMediaStream();
					startRecording();
				}
				break;
			case "S":
				recorder !== "ready" && stopRecording();
				break;
		}
	}

	// Bind keydown event listener
	onMount(() => {
		window.addEventListener("keydown", handleKeydown);
		return () => window.removeEventListener("keydown", handleKeydown);
	});
</script>

<svelte:window onkeydown={handleKeydown} />

{#if recorder.includes("ready")}
	<div class="recorder" data-state={recorder}>
		<button onclick={startRecording} class="record">
			<div class="circle">
				{#if recorder === "ready.countdown"}
					{seconds}
				{/if}
			</div>
		</button>

		<div class="info">
			{#if recorder === "ready"}
				<p class="shortcut">Shift + R</p>
				<p class="description">To start recording</p>
			{/if}

			{#if recorder === "ready.countdown"}
				<p class="shortcut">Shift + S</p>
				<p class="description">To stop recording</p>
			{/if}
		</div>
	</div>
{/if}

<style>
	.recorder {
		--txt-clr: oklch(98% 0% 0);
		--circle-bg-clr: oklch(64% 100% 26);
		--circle-border-clr: oklch(98% 0% 0);

		position: fixed;
		left: 50%;
		bottom: 80px;
		transform: translateX(-50%);
		font-family: var(--r-main-font);
		color: var(--txt-clr);
		text-align: center;
		z-index: 10;
	}

	.recorder[data-state="ready.countdown"] .circle {
		--txt-clr: oklch(10% 0% 0);
		--circle-bg-clr: oklch(98% 0% 0);
	}

	.recorder .record {
		width: 80px;
		height: 80px;
		padding: 4px;
		border: 4px solid var(--circle-border-clr);
		border-radius: 50%;
	}

	.recorder .record:hover {
		cursor: pointer;
	}

	.recorder .record .circle {
		width: 100%;
		height: 100%;
		display: grid;
		place-content: center;
		font-size: 2rem;
		font-weight: 700;
		color: var(--txt-clr);
		background: var(--circle-bg-clr);
		border-radius: 50%;
		transition: background-color 0.6s;
	}

	.recorder .info {
		margin-block-start: 1rem;
	}

	.recorder .info .shortcut {
		font-weight: 700;
	}

	.recorder .info .description {
		margin-block-start: 4px;
		opacity: 0.6;
	}
</style>
