<style>
	.btn-toolbar .btn-group {
		float: right;
	}
</style>
<template>
	<div class="row btn-toolbar" id="{{ site.id }}-id:{{ printer.id }}"
		 role="toolbar" aria-label="Toolbar with button groups">
		<div class="col-md-8" role="group" aria-label="Actions publiques">
			<a href="http://{{printer.hostname}}">{{ printer.hostname }}</a>:
			<span class="">
				<span class="port listening">{{ printer.listening_port }}</span>
				<span class="forward">
					<i class="fa fa-long-arrow-right" v-if="printer.forward=='normal'"></i>
					<i class="fa fa-long-arrow-left" v-if="printer.forward=='reverse'"></i>
				</span>
				<span class="port destination">{{ printer.destination_port }}</span>
			</span>
			<small class="forward text-muted">({{printer.forward}} forwarding)</small>
			<i class="description text-muted">{{ printer.description }}</i>
		</div>
		<div class="col-md-4">
			<ul class="btn-toolbar">
				<li class="btn-group" role="group" aria-label="Actions non-réversibles">
					<button aria-label="Supprimer cette *imprimante*"
							role="button"
							class="btn btn-link btn-sm btn-action hide-btn-content hint--top-left"
							@click="remove(printer.id)"
					>
						<i class="fa fa-trash-o text-danger"> </i>
					</button>
				</li>
				<li class="btn-group" role="group" aria-label="Actions d'administrations">
					<button aria-label="script d'installation d'imprimante"
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
	import actions from '../../../vuex/actions';
	import logging from '../../../services/logging.service';
	import resource from 'pilou';

	const printers = resource('printers', {delete: '/api/sites/${site_id}/${resource}/${printer_id}'});

	export default {
		data() {
			return {};
		},
		props: {
			printer: {type: Object, required: true},
			site: {type: Object, required: true}
		},
		ready(){
		},
		methods: {
			remove(printerId) {
				printers.delete({site_id: this.site.id, printer_id: printerId}).then((response) => {
					this.removePrinter(response.data);
					logging.success(this.$t('sites.remove.succeed'));
				}).catch((err) => {
					console.log('deletion failed', err);
					logging.error(this.$t('sites.delete.failed'))
				});
			}
		},
		vuex: {
			actions: {
				removePrinter: actions.removePrinter,
			},
		}
	}
</script>