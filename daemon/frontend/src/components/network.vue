<template>
	<span class="ping hint--top-right" aria-label="ping: {{ device.ping | time }}">
		<i class="tunnel-status fa {{ device.ping | icon 'ping' }}"> </i>
	</span>
	<span class="telnet hint--top-right" aria-label="telnet (via tunnel): {{ device.telnet | reachable }}">
		<i class="tunnel-status fa {{ device.telnet | icon 'telnet' }}"> </i>
	</span>
</template>
<script type="text/ecmascript-6">
	import network from './network.filter';

	export default {
		props: {
			device: {
				type: Object,
				default: function () {
					return {
						ping: null,
						telnet: null
					}
				}
			},
		},
		filters: {
			time: network.time,
			icon: network.icon,
			reachable: network.reachable
		}
	}
</script>
<style>
	.ping {
		text-shadow: 2px 0 0px #fff;
		z-index: 1;
		margin-left: .5em;
	}

	.telnet {
		left: -12px;
	}

	.ping .fa-pulsing, .telnet .fa-pulsing {
		border: .2rem solid #ccc;
		border-radius: 5rem !important;
		height: 1rem;
		width: 1rem;
		position: relative;
		top: .2rem;
		left: .3rem;
		animation: pulsate 2s infinite ease-out;
		opacity: 1;
	}

	@-webkit-keyframes pulsate {
		0% {
			border-width: .4rem;
			border-color: #eee;
			transform: scale(0.05, 0.05);
			opacity: 0;
		}
		50% {
			opacity: 1;
		}
		100% {
			transform: scale(1, 1);
			opacity: 0;
		}
	}
</style>
