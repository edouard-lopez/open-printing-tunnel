<template>
	<div>
		<div class="row">
			Sites

			<pre>{{sites | json 4}}</pre>
		</div>
	</div>
</template>

<script type="text/ecmascript-6">
	import logging from 'services/logging.service';
	import resources from 'pilou';

	import http from 'services/http.service';

	const sites = http('sites', localStorage);

	export default {
		data() {
			return {
				sites: null
			};
		},
		ready(){
			this.getSites();
		},
		methods: {
			getSites(){
				sites.all().then(response => {
					this.sites = response.data;
				})
			}
		}
	};
</script>
