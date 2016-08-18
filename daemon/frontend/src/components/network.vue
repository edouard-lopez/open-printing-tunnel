<template>
	<span class="hint--top-right" aria-label="ping: {{ping.avg}}ms | telnet: ">
				<i class="tunnel-status fa {{networkIcon}}"> </i>
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
						avg: null,
						max: null,
						mdev: null,
						min: null
					}
				}
			},
		},
		computed: {
			networkIcon: function () {
				let icon = 'fa-ellipsis text-muted';

				if (typeof this.ping !== 'undefined') {
					if (typeof this.ping.avg === 'number' && this.ping.avg > 0) {
						icon = 'fa-check text-success';
					}
					else {
						icon = 'fa-warning text-warning';
					}
				}

				return icon;
			}
		},
		methods: {},
		vuex: {
			actions: {},
			getters: {}

		}
	}
</script>
