<template>
	<button class="scan btn btn-sm btn-secondary hint--top-right"
			aria-label="{{site.hostname}}"
			@click="scan(site)"
	>
		<i class="fa fa-wifi" v-if="!scanning"> </i>
		<i class="fa fa-pulsing" v-else> </i>
	</button>
</template>
<script type="text/ecmascript-6">
	import http from 'services/http.service';
	import actions from 'vuex/actions';

	export default {
		data() {
			return {
				scanning: false,
			};
		},
		props: {
			site: {
				type: Object,
				required: true
			}
		},
		methods: {
			scan(site) {
				if (!this.scanning) {
					this.scanning = true;
					this.scanSite(site).then((response) => this.scanning = false);
				}
			}
		},
		vuex: {
			actions: {
				scanSite: actions.scanSite,
			}
		}

	}
</script>
<style>
	.scan .fa-pulsing {
		border: .2rem solid #999;
		border-radius: 5rem !important;
		height: 1em;
		width: 1em;
		position: relative;
		top: .1rem;
		animation: pulsate 2s infinite ease-out;
		opacity: 1;
	}

	@-webkit-keyframes pulsate {
		0% {
			border-width: .4rem;
			border-color: #aaa;
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
