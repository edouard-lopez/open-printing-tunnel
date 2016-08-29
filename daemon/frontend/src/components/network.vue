<template>
	<span class="ping hint--top-right" aria-label="ping: {{ device.ping | currency '' 2 }} ms">
		<i class="tunnel-status fa {{ device.ping | networkIcon 'ping' }}"> </i>
	</span>
	<span class="telnet hint--top-right" aria-label="telnet: {{ device.telnet | currency '' 2 }} ms">
		<i class="tunnel-status fa {{ device.telnet | networkIcon 'telnet' }}"> </i>
	</span>
</template>
<script type="text/ecmascript-6">
	export default {
		props: {
			device: {
				type: Object,
				required: true,
				default: function () {
					return {
						ping: null,
						telnet: null
					}
				}
			},
		},
		filters: {
			networkIcon: function (probe, type) {
//				let icon = 'fa-pulsing fa-fw text-warning';
				let icon = 'fa-warning text-warning';

				if (type == 'ping' && probe > 0) {
					icon = 'fa-check text-success';
				}
				else if (type == 'telnet' && probe > 0) {
					icon = 'fa-check text-primary';
				}

				return icon;
			}
		}
	}
</script>
<style>
	.ping {
		text-shadow: 2px 0 0px #fff;
		z-index: 1;
	}

	.telnet {
		left: -12px;
	}

	.fa-pulsing {
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
