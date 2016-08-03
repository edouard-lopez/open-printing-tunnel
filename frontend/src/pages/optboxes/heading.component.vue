<style>

</style>
<template>
	<div class="row">
		<div class="col-md-6 expandable"
			 data-toggle="collapse"
			 aria-expanded="false"
			 aria-controls="optbox-{{optbox.name}}"
			 data-target="#optbox-{{optbox.name}}"
		>
			<span class="hint--top-right" aria-label="Tooltip on top">
				<i class="tunnel-status fa fa-check text-muted"> </i>
			</span>
			<span class="tunnel-name">
				<b>{{optbox.name}}</b>
			</span>
			<span class="divider"> – </span>
			<span class="tunnel-fqdn text-muted">{{optbox.hostname}}</span>
		</div>
		<div class="col-md-6">
			<ul class="btn-toolbar" role="toolbar"
				aria-label="Toolbar with button groups">
				<li class="btn-group" role="group"
					aria-label="Actions non-réversibles">
					<button aria-label="Supprimer cet *hôte*"
							role="button"
							class="btn btn-link btn-sm btn-action hide-btn-content hint--top-left"
							@click="remove(optbox.name)"
					>
						<i class="fa fa-trash-o text-danger"> </i>
					</button>
				</li>
				<li class="btn-group" role="group"
					aria-label="Actions d'administration">
					<button aria-label="Redémarrer"
							role="button"
							class="btn btn-warning btn-sm btn-action restart hide-btn-content hint--top"
							@click="restart(optbox.name)"
					>
						<i class="fa fa-refresh"> </i>
					</button>
					<button aria-label="Démarrer"
							role="button"
							class="btn btn-success btn-sm btn-action hide-btn-content hint--top"
							@click="start(optbox.name)"
					>
						<i class="fa fa-play"> </i>
					</button>
					<button aria-label="Arrêter"
							role="button"
							class="btn btn-danger btn-sm btn-action hide-btn-content hint--top"
							@click="stop(optbox.name)"
					>
						<i class="fa fa-stop"> </i>
					</button>
				</li>
				<li class="btn-group" role="group" aria-label="Actions publiques">
					<button aria-label="Status"
							role="button"
							class="btn btn-info btn-sm btn-action hide-btn-content hint--top"
							@click="status(optbox.name)"
					>
						<i class="fa fa-info"> </i>
					</button>
					<add-printer-button :boitier="optbox" class="btn-sm"></add-printer-button>
					<button aria-label="Ajouter des *canaux* par lot"
							role="button"
							class="btn btn-primary btn-sm btn-action hide-btn-content hint--top"
							@click="add_bulk_channels(optbox.name)"
					>
						<i class="fa fa-print"> </i>
					</button>
					<button aria-label="script d'installation d'imprimante"
							role="button"
							class="btn btn-default btn-sm btn-action hide-btn-content hint--top"
							@click="link(optbox.name)"
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
	import resource from 'pilou';

	const optboxes = resource('optboxes', {
		all: '/daemon/${resource}/${id}',
		update: '/daemon/${resource}/${id}'
	});


	export default{
		data(){
			return {}
		},
		components: {
			'add-printer-button': AddPrinterButtonComponent
		},
		props: {
			optbox: {
				type: Object,
				required: true
			},
		},
		methods: {
			status(optbox_id) {
				optboxes.update({id: optbox_id}, {action: 'status'}).then(response => {
					this.$dispatch('log-response', response.data);
				});
			},
			start(optbox_id) {
				optboxes.update({id: optbox_id}, {action: 'start'}).then(response => {
					this.$dispatch('log-response', response.data);
					logging.success(this.$t('optboxes.start.succeed'));
				}).catch(() => {
					logging.error(this.$t('optboxes.start.failed'))
				});
			},
			stop(optbox_id) {
				optboxes.update({id: optbox_id}, {action: 'stop'}).then(response => {
					this.$dispatch('log-response', response.data);
					logging.success(this.$t('optboxes.stop.succeed'));
				}).catch(() => {
					logging.error(this.$t('optboxes.stop.failed'))
				});
			},
			restart(optbox_id) {
				optboxes.update({id: optbox_id}, {action: 'restart'}).then(response => {
					this.$dispatch('log-response', response.data);
					logging.success(this.$t('optboxes.restart.succeed'));
				}).catch(() => {
					logging.error(this.$t('optboxes.restart.failed'))
				});
			},
			remove(optbox_id) {
				optboxes.delete({'optbox': optbox_id}).then((response) => {
					console.log(this.printer.channels[optbox_id])
					logging.success(this.$t('optboxes.remove.succeed'));
				}).catch(() => {
					logging.error(this.$t('optboxes.delete.failed'))
				});
			},
			link(name) {
				// todo
			}
		}
	}
</script>
