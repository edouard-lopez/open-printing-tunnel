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
						<div id="accordion" role="tablist" aria-multiselectable="true">
							<div v-for="site in sites" class="panel panel-default">
								{{site}}
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
	import http from 'services/http.service';
	import logging from 'services/logging.service';
	import actions from 'vuex/actions';
	import getters from 'vuex/getters';

	import SiteComponent from './site.component.vue'
	import AddSiteButtonComponent from './add-site.component';
	import LogsComponent from './logs/logs.component';

	const sites = http('sites', localStorage);

	export default {
		ready(){
			this.getSites();
		},
		components: {
			'site': SiteComponent,
			'add-site-button': AddSiteButtonComponent,
			'logs': LogsComponent,
		},
		methods: {
			getSites() {
				sites.all().then((response) => {
					this.setSites(response.data.results);
				}).catch(() => {
					this.no_site_message = 'there is no site';
					logging.error(this.$t('sites.get.failed'))
				});
			}
		},
		events: {
			'log-response': function (message) {
				this.$broadcast('log-response', message);
			},
		},
		vuex: {
			actions: {
				setSites: actions.setSites,
			},
			getters: {
				sites: getters.retrieveSites
			}
		}
	};
</script>
