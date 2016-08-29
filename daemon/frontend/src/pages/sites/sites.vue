<template>
	<div id="sites-page">
		<div class="row">
			<div class="col-lg-12">
				<div class="card card-block">
					<div class="row">
						<div class="col-md-12">
							<h3>
								<i class="fa fa-map-marker"></i>
								Sites
							</h3>
						</div>
					</div>
					<div class="row" id="dashboard">
						<span class="col-md-12 text-xs-right">
							<add-site-button></add-site-button>
						</span>
					</div>

					<br>

					<div class="row">
						<div id="accordion" class="striped" role="tablist" aria-multiselectable="true">
							<div v-for="site in sites" class="panel panel-default">
								<site :site="site"></site>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div class="row">
			<div class="col-lg-12">
				<div class="card card-block">
					<logs></logs>
				</div>
			</div>
		</div>
	</div>
</template>

<script type="text/ecmascript-6">
	import logging from 'services/logging.service';
	import actions from 'vuex/actions';
	import getters from 'vuex/getters';

	import SiteComponent from './site.component.vue'
	import AddSiteButtonComponent from './add-site.component';
	import LogsComponent from './logs/logs.component';

	export default {
		ready(){
			this.getSites();
			this.probeNetwork();
		},
		computed: {
			network() {
				var data = null;

				if (typeof this.networks !== 'undefined') {
					data = this.networks[this.site.hostname];
				}

				return data;
			},
		},
		components: {
			'site': SiteComponent,
			'add-site-button': AddSiteButtonComponent,
			'logs': LogsComponent,
		},
		vuex: {
			actions: {
				getSites: actions.getSites,
				probeNetwork: actions.probeNetwork,
			},
			getters: {
				sites: getters.retrieveSites,
			}
		}
	};
</script>
<style>
	.striped .printer:nth-of-type(2n+1) {
		background-color: hsla(0, 0%, 0%, 0.1);
	}
</style>
