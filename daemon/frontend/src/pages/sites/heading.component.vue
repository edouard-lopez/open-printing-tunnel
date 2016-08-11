<style>
	.expandable {
		cursor: pointer;
	}
</style>
<template>
	<div class="row">
		<div class="col-md-6 expandable"
			 data-toggle="collapse"
			 aria-expanded="false"
			 aria-controls="site-{{site.id}}"
			 data-target="#site-{{site.id}}"
		>
			<span class="hint--top-right" aria-label="Tooltip on top">
				<i class="tunnel-status fa fa-check text-muted"> </i>
			</span>
			<span class="tunnel-name">
				<b>{{site.id}}</b>
			</span>
			<span class="divider"> – </span>
			<span class="tunnel-fqdn text-muted">{{site.hostname}}</span>
		</div>
		<div class="col-md-6">
			<ul class="btn-toolbar" role="toolbar"
				aria-label="Toolbar with button groups">
				<li class="btn-group" role="group"
					aria-label="Actions non-réversibles">
					<button aria-label="Supprimer cet *hôte*"
							role="button"
							class="btn btn-link btn-sm btn-action hide-btn-content hint--top-left"
							@click="remove(site.id)"
					>
						<i class="fa fa-trash-o text-danger"> </i>
					</button>
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
					<add-printer-button :boitier="site" class="btn-sm"></add-printer-button>
					<button aria-label="Ajouter des *canaux* par lot"
							role="button"
							class="btn btn-primary btn-sm btn-action hide-btn-content hint--top"
							@click="add_bulk_channels(site.id)"
					>
						<i class="fa fa-print"> </i>
					</button>
					<button v-if="has_printers()" aria-label="script d'installation d'imprimante"
							role="button"
							class="btn btn-default btn-sm btn-action hide-btn-content hint--top"
							@click="link(site.id)"
					>
						<i class="fa fa-comment"> </i>
					</button>
				</li>
			</ul>
		</div>
	</div>
</template>
<script type="text/ecmascript-6">
	import AddPrinterButtonComponent from './add-printer.component.vue';

	import http from 'services/http.service';
	import FileSaver from 'file-saver';
	import actions from '../../vuex/actions';
	import logging from '../../services/logging.service';
	import resource from 'pilou';

	const sites = http('sites', localStorage);
	const scripts = http('scripts', localStorage);


	export default{
		ready() {console.log(this.site.channels)},
		components: {
			'add-printer-button': AddPrinterButtonComponent
		},
		props: {
			site: {
				type: Object,
				required: true
			},
		},
		computed: {
			has_printers: () => this.site.channels.length > 0
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
			remove(site_id) {
				sites.delete({site_id: site_id}).then((response) => {
					this.removeSite(response.data);
					logging.success(this.$t('sites.remove.succeed'));
				}).catch((err) => {
					console.log('deletion failed', err);
					logging.error(this.$t('sites.delete.failed'))
				});
			},
			link(site_id) {
				scripts.get({id: site_id}).then((response) => {
					var filename = response.headers['content-disposition'].split('=')[1];
					var blob = new Blob([response.data], {type: response.headers['content-type']});
					FileSaver.saveAs(blob, filename);
					logging.success(this.$t('scripts.creation.succeed'));
				}).catch((err) => {
					console.log('deletion failed', err);
					logging.error(this.$t('scripts.creation.failed'))
				});
			}
		},
		vuex: {
			actions: {
				removeSite: actions.removeSite,
			}
		}
	}
</script>
