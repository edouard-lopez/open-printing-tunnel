<style>
	.btn-toolbar .btn-group {
		float: right;
	}
</style>
<template>
	<div class="row btn-toolbar" id="{{ site.id }}-id:{{ printer.id }}"
		 role="toolbar" aria-label="Toolbar with button groups">
		<div class="col-md-6" role="group" aria-label="Actions publiques">
			<network :ping="ping" :telnet="telnet"></network>
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
				<li class="btn-group" role="group" aria-label="Actions d'administrations">
					<button aria-label="script d'installation d'imprimante"
							role="button"
							class="btn btn-sm btn-link btn-action hide-btn-content hint--top"
							@click="getScript(site, printer)"
					>
						<i class="fa fa-file-o"> </i>
					</button>
					<delete :promise="delete_printer" :object="printer" class="btn-sm btn-link">
						<span slot="title">Supprimer l'imprimante <var>{{printer.hostname}}</var></span>
						<span slot="body">Confirmer la suppression l'imprimante.</span>
						<span slot="in-progress">Suppression en cours</span>
						<span slot="action">Supprimer l'imprimante</span>
					</delete>
				</li>
			</ul>
		</div>
	</div>
</template>
<script type="text/ecmascript-6">
	import DeleteButton from 'components/delete-button';
	import Network from 'components/network';

	import logging from 'services/logging.service';
	import actions from 'vuex/actions';
	import getters from "vuex/getters";

	export default {
		components: {
			'delete': DeleteButton,
			'network': Network
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
			},
//			ping() {
//				return this.pings[this.site.id][this.printer.hostname];
//			}
			ping() {
				var data = null;

				if (typeof this.pings !== 'undefined' && typeof this.pings[this.site.hostname] !== 'undefined') {
					data = this.pings[this.site.hostname][this.printer.hostname];
				}

				return data;
			},
			telnet() {
				var data = null;

				if (typeof this.telnets !== 'undefined' && typeof this.telnets[this.site.hostname] !== 'undefined') {
					data = this.telnets[this.site.hostname][this.printer.hostname];
				}

				return data;
			}
		},
		methods: {
			delete_printer(printer) {
				return this.deletePrinter(this.site, printer).then(response => {
					this.getSites();
					this.siteRestart(this.site);
				});
			},
			getScript(site, printer) {
				this.getPrinterScript(site, printer)
						.then(response => {
							this.saveFile(response);
						})
						.catch(err => {
							console.error('Échec du téléchargement du script.', err);
						})
			}
		},
		vuex: {
			actions: {
				deletePrinter: actions.deletePrinter,
				getPrinterScript: actions.getPrinterScript,
				getSites: actions.getSites,
				saveFile: actions.saveFile,
				siteRestart: actions.siteRestart
			},
			getters: {
				pings: getters.retrievePings,
				telnets: getters.retrieveTelnets,
			}
		}
	}
</script>
