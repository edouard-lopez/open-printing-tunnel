<style scoped>
	.table thead th, .table td, .table th {
		border: none;
	}
</style>
<template>
	<div id="container-page">
		<div class="row">
			<div class="col-md-12">
				<div class="card">
					<h5 class="card-header">
						<i class="fa fa-map-marker" aria-hidden="true"></i> Sites
					</h5>
					<div class="card-block">
						<div v-for="site in sites">
							<site :site="site"></site>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script type="text/ecmascript-6">
	import http from 'services/http.service';
	import Site from './site.component';

	const SitesService = http('sites', localStorage);
	export default {
		data() {
			return {
				sites: []
			};
		},
		ready(){
			this.getSites();
		},
		components: {
			'site': Site
		},
		methods: {
			getSites(){
				return SitesService.all().then(response => {
					console.log(response.data);
					this.sites = response.data;
				});
			}
		}
	};
</script>
