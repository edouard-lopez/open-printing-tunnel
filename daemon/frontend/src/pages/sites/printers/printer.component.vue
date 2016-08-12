<style>
	.btn-toolbar .btn-group {
		float: right;
	}
</style>
<template>
	<div class="row btn-toolbar" id="{{ site.id }}-id:{{ printer.id }}"
		 role="toolbar" aria-label="Toolbar with button groups">
		<div class="col-md-6" role="group" aria-label="Actions publiques">
			<span class="description">{{ printer.description }}</span>
		</div>
		<div class="col-md-4">
			<a href="http://{{printer.hostname}}">{{ printer.hostname }}</a>
			<small class="text-muted">
				<span class="port listening">{{ printer.ports.listen }}</span>
				<abbr class="forward hint--top" aria-label="forwarning {{from}}">
					<i class="fa fa-long-arrow-right" v-show="is_forwarding_remote"></i>
					<i class="fa fa-long-arrow-left" v-show="!is_forwarding_remote"></i>
				</abbr>
				<span class="port destination">{{ printer.ports.send }}</span>
			</small>
		</div>
		<div class="col-md-2">
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
							class="btn btn-sm btn-link btn-action hide-btn-content hint--top"
							@click="getScript(site.id, printer.id)"
					>
						<i class="fa fa-file-o"> </i>
					</button>
				</li>
			</ul>
		</div>
	</div>
</template>
<script type="text/ecmascript-6">
	import http from 'services/http.service';
	import logging from 'services/logging.service';
	import actions from 'vuex/actions';

	const printers = http('printers', localStorage);

	export default {
		data() {
			return {};
		},
		props: {
			printer: {type: Object, required: true},
			site: {type: Object, required: true}
		},
		computed: {
			is_forwarding_remote() {
				return this.printer.ports.forward == 'remote'
			},
			from() {
				return this.printer.ports.forward
			}
		},
		methods: {
			remove(printerId) {
				printers.delete({site_id: this.site.id, printer_id: printerId}).then((response) => {
					this.removePrinter(response.data);
					logging.success('Imprimante supprimée correctement');
				}
			).catch((err) => {
					console.log('deletion failed', err);
					logging.error('Échec de la suppression !')
				}
			);
			}
		},
		vuex: {
			actions: {
				removePrinter: actions.removePrinter,
				getScript: actions.getPrinterScript,
			},
		}
	}
</script>
