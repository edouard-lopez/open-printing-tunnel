<style>
	.expandable {
		cursor: pointer;
	}

	.vertical-align-text {
		line-height: 2em;
		height: 2em;
	}
</style>
<template>
	<div class="row">
		<div class="col-xs-7 col-md-5 vertical-align-text ">
			<network :device="device"></network>
			<span class="tunnel-name"
				  data-toggle="collapse"
				  aria-expanded="false"
				  aria-controls="site-{{site.id}}"
				  data-target="#site-{{site.id}}"
			>
				<b>{{site.id}}</b>
			</span>
			<span class="divider"> – </span>
			<a href="//{{site.hostname}}" class="tunnel-fqdn" target="_blank">
				{{site.hostname}}
			</a>
		</div>
		<div class="hidden-sm-down col-md-2 expandable"
			 data-toggle="collapse"
			 aria-expanded="false"
			 aria-controls="site-{{site.id}}"
			 data-target="#site-{{site.id}}"
		>
			<span class="invisible">expandable area</span>
		</div>
		<div class="col-xs-5 col-md-5">
			<ul class="btn-toolbar list-inline" role="toolbar"
				aria-label="Printer toolbar">
				<li class="btn-group hidden-sm-down" role="group"
					aria-label="Actions non-réversibles">

					<delete :promise="delete_site" :object="site" class="btn-sm btn-link">
						<span slot="title">Supprimer le site <var>{{site.id}}</var></span>
						<span slot="body">Confirmer la suppression du site et des tunnels associés.</span>
						<span slot="in-progress">Suppression en cours</span>
						<span slot="action">Supprimer le site</span>
					</delete>

				</li>
				<li class="btn-group" role="group"
					aria-label="Actions d'administration">
					<button aria-label="Redémarrer"
							role="button"
							class="btn btn-warning btn-sm restart hide-btn-content hint--top"
							@click="restart(site)"
					>
						<i class="fa fa-refresh"> </i>
					</button>
					<button aria-label="Démarrer"
							role="button"
							class="btn btn-success btn-sm hide-btn-content hint--top"
							@click="start(site)"
					>
						<i class="fa fa-play"> </i>
					</button>
					<button aria-label="Arrêter"
							role="button"
							class="btn btn-danger btn-sm hide-btn-content hint--top"
							@click="stop(site)"
					>
						<i class="fa fa-stop"> </i>
					</button>
					<scanner :site="site"></scanner>
				</li>
				<li class="btn-group " role="group" aria-label="Actions publiques">
					<button aria-label="Status"
							role="button"
							class="btn btn-info btn-sm hide-btn-content hint--top"
							@click="status(site)"
					>
						<i class="fa fa-info"> </i>
					</button>
					<add-printer-button :site="site" class="btn-sm"></add-printer-button>
					<add-printers-button :site="site" class="hidden-sm-down btn-sm"></add-printers-button>
					<button v-show="has_printers" aria-label="script d'installation d'imprimante"
							role="button"
							class="hidden-sm-down btn btn-link btn-sm hide-btn-content hint--top"
							@click="getScript(site)"
					>
						<i class="fa fa-file-o"> </i>
					</button>
				</li>
			</ul>
		</div>
	</div>
</template>
<script type="text/ecmascript-6">
	import AddPrinterButtonComponent from './add-printer.component.vue';
	import AddPrintersButtonComponent from './add-printers.component.vue';
	import DeleteButton from 'components/delete-button';
	import Network from 'components/network';
	import Scanner from 'components/scanner';

	import http from 'services/http.service';
	import actions from 'vuex/actions';
	import getters from "vuex/getters";
	import logging from 'services/logging.service';

	export default{
		components: {
			'add-printer-button': AddPrinterButtonComponent,
			'add-printers-button': AddPrintersButtonComponent,
			'delete': DeleteButton,
			'network': Network,
			"scanner": Scanner
		},
		props: {
			site: {type: Object, required: true},
		},
		computed: {
			has_printers: function () {
				return this.site.channels.length > 0;
			},
			device() {
				var data = null;

				if (typeof this.networks !== 'undefined') {
					data = this.networks[this.site.hostname];
				}

				return data;
			},
		},
		methods: {
			status(site) {
				this.siteStatus(site);
			},
			start(site) {
				this.siteStart(site);
			},
			stop(site) {
				this.siteStop(site);
			},
			restart(site) {
				this.siteRestart(site);
			},
			delete_site(site){
				return this.deleteSite(site).then(response => {
					this.getSites();
				});
			},
			getScript(site) {
				this.getSiteScript(site).then(response => {
					this.saveFile(response);
				}).catch(err => {
					console.error('Échec du téléchargement du script.', err);
				})
			},
		},
		vuex: {
			actions: {
				getSites: actions.getSites,
				getSiteScript: actions.getSiteScript,
				deleteSite: actions.deleteSite,
				saveFile: actions.saveFile,
				siteStatus: actions.siteStatus,
				siteStart: actions.siteStart,
				siteStop: actions.siteStop,
				siteRestart: actions.siteRestart,
			},
			getters: {
				networks: getters.retrieveNetworks,
			}
		}
	}
</script>
