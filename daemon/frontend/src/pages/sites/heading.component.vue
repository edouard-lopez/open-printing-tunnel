<style>
	.expandable {
		cursor: pointer;
	}
</style>
<template>
	<div class="row">
		<div class="col-md-6 expandable"
		>
			<span class="hint--top-right" aria-label="Tooltip on top">
				<i class="tunnel-status fa fa-check text-muted"> </i>
			</span>
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
		<div class="col-md-6">
			<ul class="btn-toolbar" role="toolbar"
				aria-label="Toolbar with button groups">
				<li class="btn-group" role="group"
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
							class="btn btn-warning btn-sm btn-action restart hide-btn-content hint--top"
							@click="restart(site)"
					>
						<i class="fa fa-refresh"> </i>
					</button>
					<button aria-label="Démarrer"
							role="button"
							class="btn btn-success btn-sm btn-action hide-btn-content hint--top"
							@click="start(site)"
					>
						<i class="fa fa-play"> </i>
					</button>
					<button aria-label="Arrêter"
							role="button"
							class="btn btn-danger btn-sm btn-action hide-btn-content hint--top"
							@click="stop(site)"
					>
						<i class="fa fa-stop"> </i>
					</button>
				</li>
				<li class="btn-group" role="group" aria-label="Actions publiques">
					<button aria-label="Status"
							role="button"
							class="btn btn-info btn-sm btn-action hide-btn-content hint--top"
							@click="status(site)"
					>
						<i class="fa fa-info"> </i>
					</button>
					<add-printer-button :site="site" class="btn-sm"></add-printer-button>
					<button aria-label="Ajouter des *canaux* par lot"
							role="button"
							class="btn btn-primary btn-sm btn-action hide-btn-content hint--top"
							@click="add_bulk_channels(site.id)"
					>
						<i class="fa fa-print"> </i>
					</button>
					<button v-show="has_printers" aria-label="script d'installation d'imprimante"
							role="button"
							class="btn btn-link btn-sm btn-action hide-btn-content hint--top"
							@click="getSiteScript(site.id)"
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
	import DeleteButton from 'components/delete-button';

	import http from 'services/http.service';
	import actions from 'vuex/actions';
	import logging from 'services/logging.service';

	const sites = http('sites', localStorage);


	export default{
		components: {
			'add-printer-button': AddPrinterButtonComponent,
			'delete': DeleteButton
		},
		props: {
			site: {type: Object, required: true},
		},
		computed: {
			has_printers: function () {
				return this.site.channels.length > 0;
			}
		},
		methods: {
			status(site) {
				site['action'] = 'status';
				sites.update(site).then(response => {
					this.$dispatch('log-response', response.data);
				});
			},
			start(site) {
				site['action'] = 'start';
				sites.update(site).then(response => {
					this.$dispatch('log-response', response.data);
					logging.success(this.$t('Démarrage réussi.'));
				}).catch(() => {
					logging.error(this.$t('Échec du démarrage.'))
				});
			},
			stop(site) {
				site['action'] = 'stop';
				sites.update(site).then(response => {
					this.$dispatch('log-response', response.data);
					logging.success(this.$t('Arrêt réussi.'));
				}).catch(() => {
					logging.error(this.$t('Échec de l\'arrêt.'))
				});
			},
			restart(site) {
				site['action'] = 'restart';
				sites.update(site).then(response => {
					this.$dispatch('log-response', response.data);
					logging.success(this.$t('Redémarrage réussi.'));
				}).catch(() => {
					logging.error(this.$t('Échec du redémarrage.'))
				});
			},
			delete_site(site){
				return this.deleteSite(site);
			},
		},
		vuex: {
			actions: {
				getSites: actions.getSites,
				getSiteScript: actions.getSiteScript,
				deleteSite: actions.deleteSite,
			}
		}
	}
</script>
