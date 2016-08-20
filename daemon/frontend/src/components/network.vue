<template>
	<span class="ping hint--top-right" aria-label="ping: {{ping.ping}} ms">
		<i class="tunnel-status fa {{ping | networkIcon}}"> </i>
	</span>
	<span class="telnet hint--top-right" aria-label="telnet: {{telnet.telnet}} ms">
		<i class="tunnel-status fa {{telnet | networkIcon}}"> </i>
	</span>
</template>
<script type="text/ecmascript-6">
	export default {
		props: {
			ping: {
				type: Object,
				required: true,
				default: function () {
					return {
						ping: null
					}
				}
			},
			telnet: {
				type: Object,
				required: true,
				default: function () {
					return {
						telnet: null
					}
				}
			},
		},
		filters: {
			networkIcon: function (probe) {
				let icon = 'fa-circle-o-notch fa-spin text-muted';
				console.log('probe', probe);

				if (typeof probe !== 'undefined') {
					if (typeof probe.ping !== 'undefined' && probe.ping > 0) {
						icon = 'fa-check text-success';
					}
					else if (typeof probe.telnet !== 'undefined' && probe.telnet > 0) {
						icon = 'fa-check text-primary';
					}
				} else {
					icon = 'fa-warning text-warning';
				}

				console.log('icon', icon)
				return icon;
			},
		},
		methods: {},
		vuex: {
			actions: {},
			getters: {}

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
</style>
