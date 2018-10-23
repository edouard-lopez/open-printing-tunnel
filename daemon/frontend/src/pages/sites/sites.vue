<template>
	<div id="sites-page">
		<splash>
			<span slot="title">
				<i class="fa fa-warning text-warning"></i>
				Zone Dangereuse
			</span>
			<p slot="body">
				Vous êtes sur une interface d'administration, vos actions peuvent <strong>impacter le réseau
				d'entreprise</strong>.
			</p>
			<span slot="accept">
				<i class="fa fa-check text-success"></i>
				<b>Accepter</b> les risques
			</span>
		</splash>
		<div data-e2e="header" class="card card-block">
			<div class="row">
				<div class="col-xs-6 col-md-6">
					<h2>
						<i class="fa fa-map-marker text-danger"></i>
						Sites
					</h2>
				</div>
				<span class="col-xs-6 col-md-6 text-xs-right">
					<add-site-button></add-site-button>
				</span>
			</div>
		</div>
		<div id="accordion" class="striped" role="tablist" aria-multiselectable="true">
			<div v-show="!has_sites" data-e2e="no-site-available" class="card card-block bg-warning ">
				<span>
					<i class="fa fa-spinner fa-pulse fa-lg fa-fw"></i>
					<span class="sr-only">Loading…</span>
					Aucun site détecté…
				</span>
				<span>ou navigateur non supporté</span>.
			</div>
			<div v-for="(index, site) in sites | orderBy 'id' " class="site card card-block" data-e2e="sites">
				<site :site="site" :index="index"></site>
			</div>
		</div>
		<div class="card card-block">
			<logs></logs>
		</div>
	</div>
</template>

<script type="text/ecmascript-6">
import actions from 'vuex/actions';
import getters from 'vuex/getters';

import SiteComponent from './site.component.vue';
import AddSiteButtonComponent from './add-site.component';
import LogsComponent from './logs/logs.component';
import SplashComponent from '../../components/splash.vue';

export default {
  ready() {
    this.getSites();
    this.probeNetwork().then(() => {
      let SECOND = 1000;
      let PROBE_BASE_INTERVAL = 15;

      let probeDynamicInterval =
        PROBE_BASE_INTERVAL + Math.round(this.devicesCount / 5);
      console.info(`ping devices every ${probeDynamicInterval}s`);
      this.interval = setInterval(
        () => this.probeNetwork(),
        probeDynamicInterval * SECOND
      );
    });
  },
  beforeDestroy() {
    clearInterval(this.interval);
  },
  computed: {
    devicesCount: function() {
      let devicesCount = Object.keys(this.networkDevices).length || 0;
      for (let siteHostname in this.networkDevices) {
        for (let device in this.networkDevices[siteHostname]) {
          let notDevices = ['telnet', 'ping'];
          if (!notDevices.includes(device)) {
            devicesCount++;
          }
        }
      }
      return devicesCount;
    },
    has_sites: function() {
      return this.sites.length > 0;
    },
    network() {
      let data = null;

      if (typeof this.networks !== 'undefined') {
        data = this.networks[this.site.hostname];
      }

      return data;
    }
  },
  components: {
    site: SiteComponent,
    'add-site-button': AddSiteButtonComponent,
    logs: LogsComponent,
    splash: SplashComponent
  },
  vuex: {
    actions: {
      getSites: actions.getSites,
      probeNetwork: actions.probeNetwork
    },
    getters: {
      sites: getters.retrieveSites,
      networkDevices: getters.retrieveNetworks
    }
  }
};
</script>
<style>
h2 {
  margin-bottom: 0;
}

.striped .printer:nth-of-type(2n + 1) {
  background-color: hsla(0, 0%, 0%, 0.1);
}

.site {
  padding-bottom: 0.625rem;
}
</style>
