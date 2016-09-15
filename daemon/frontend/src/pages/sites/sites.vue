<template>
	<div id="sites-page">
		<splash>
			<span slot="title">
				<i class="fa fa-warning text-warning"></i>
				Zone dangereuse
			</span>
			<p slot="body">
				Vous êtes sur une interface d'administration, vos actions peuvent <strong>impacter le réseau
				d'entreprise</strong>.
			</p>
			<span slot="accept">
				<i class="fa fa-check text-success"></i>
				Je <b>comprends</b> les risques
			</span>
		</splash>
		<div class="card card-block">
			<div class="row">
				<div class="col-md-6">
					<h2>
						<i class="fa fa-map-marker text-danger"></i>
						Sites
					</h2>
				</div>
				<span class="col-md-6 text-xs-right">
				<add-site-button></add-site-button>
			</span>
			</div>
		</div>
		<div id="accordion" class="striped" role="tablist" aria-multiselectable="true">
			<div v-for="(index, site) in sites" class="site card card-block">
				<site :site="site" :index="index"></site>
			</div>
		</div>
		<div class="card card-block">
			<logs></logs>
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
	import SplashComponent from '../../components/splash.vue';

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
			'splash': SplashComponent,
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
	h2 {
		margin-bottom: 0;
	}

	.striped .printer:nth-of-type(2n+1) {
		background-color: hsla(0, 0%, 0%, 0.1);
	}
	.site {
		padding-bottom: .625rem;
	}
</style>
