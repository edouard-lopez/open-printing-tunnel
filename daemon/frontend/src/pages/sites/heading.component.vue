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

					<delete :promise="delete_site" :object="site" class="btn-sm">
						<span slot="title">Supprimer ce site</span>
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
							@click="restart(site.id)"
					>
						<i class="fa fa-refresh"> </i>
					</button>
					<button aria-label="Démarrer"
							role="button"
							class="btn btn-success btn-sm btn-action hide-btn-content hint--top"
							@click="start(site.id)"
					>
						<i class="fa fa-play"> </i>
					</button>
					<button aria-label="Arrêter"
							role="button"
							class="btn btn-danger btn-sm btn-action hide-btn-content hint--top"
							@click="stop(site.id)"
					>
						<i class="fa fa-stop"> </i>
					</button>
				</li>
				<li class="btn-group" role="group" aria-label="Actions publiques">
					<button aria-label="Status"
							role="button"
							class="btn btn-info btn-sm btn-action hide-btn-content hint--top"
							@click="status(site.id)"
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
	import actions from '../../vuex/actions';
	import logging from '../../services/logging.service';

	const sites = http('sites', localStorage);
	const scripts = http('scripts', localStorage);


	export default{
		components: {
			'add-printer-button': AddPrinterButtonComponent,
			'delete': DeleteButton
		},
		props: {
			site: {
				type: Object,
				required: true,
				default: {}
			},
		},
		computed: {
			has_printers: function () {
				return this.site.channels.length > 0;
			}
		},
		methods: {
			status(site_id) {
				sites.update({site_id: site_id}, {action: 'status'}).then(response => {
					this.$dispatch('log-response', response.data);
				});
			},
			start(site_id) {
				sites.update({site_id: site_id}, {action: 'start'}).then(response => {
					this.$dispatch('log-response', response.data);
					logging.success(this.$t('sites.start.succeed'));
				}).catch(() => {
					logging.error(this.$t('sites.start.failed'))
				});
			},
			stop(site_id) {
				sites.update({site_id: site_id}, {action: 'stop'}).then(response => {
					this.$dispatch('log-response', response.data);
					logging.success(this.$t('sites.stop.succeed'));
				}).catch(() => {
					logging.error(this.$t('sites.stop.failed'))
				});
			},
			restart(site_id) {
				sites.update({site_id: site_id}, {action: 'restart'}).then(response => {
					this.$dispatch('log-response', response.data);
					logging.success(this.$t('sites.restart.succeed'));
				}).catch(() => {
					logging.error(this.$t('sites.restart.failed'))
				});
			},
			delete_site(site){
				return sites.delete(site).then(() => {
					logging.success('Site supprimé avec succès');
					this.getSites();
				}).catch(() => {
					logging.error('Impossible de supprimer ce site pour l\'instant. Retentez dans quelques instants ou contacter un administrateur')
				});
			},
		},
		events: {
			delete_site(daemon) {
				this.delete_site(daemon);
			}
		},
		vuex: {
			actions: {
				getSites: actions.getSites,
				getSiteScript: actions.getSiteScript,
				removeSite: actions.removeSite,
			}
		}
	}
</script>
