<style>
.btn-toolbar .btn-group {
	float: right;
}
</style>
<template>
	<div class="row" id="{{ site.id }}-id:{{ printer.id }}"
		 aria-label="Printer information">
		<div class="col-xs-6 col-sm-6 col-md-6" role="group" aria-label="Actions publiques">
			<network :device="device"></network>
			<span class="description">{{ printer.description }}</span>
		</div>
		<div class="col-xs-6 col-sm-6 col-md-4 text-xs-right">
			<a href="http://{{printer.hostname}}" target="_blank">{{ printer.hostname }}</a>
			<small class="text-muted">
				<span class="port listening">{{ printer.ports.listen }}</span>
				<abbr class="forward hint--top" aria-label="forwarding {{from}}">
					<i class="fa fa-long-arrow-right" v-show="is_forwarding_remote"></i>
					<i class="fa fa-long-arrow-left" v-show="!is_forwarding_remote"></i>
				</abbr>
				<span class="port destination">{{ printer.ports.send }}</span>
			</small>
		</div>
		<div class="hidden-sm-down col-sm-2 col-md-2">
			<ul class="btn-toolbar list-inline">
				<li class="btn-group" role="group"
					aria-label="Actions non-réversibles">
					<delete :promise="delete_printer" :object="printer" class="btn-sm btn-link">
						<span slot="title">Supprimer l'imprimante <var>{{printer.hostname}}</var></span>
						<span slot="body">Confirmer la suppression l'imprimante.</span>
						<span slot="in-progress">Suppression en cours</span>
						<span slot="action">Supprimer l'imprimante</span>
					</delete>
				</li>
				<li class="btn-group" role="group" aria-label="Actions d'administrations">
					<script-printer-installation :site="site" :printer="printer"></script-printer-installation>
				</li>
			</ul>
		</div>
	</div>
</template>
<script type="text/ecmascript-6">
import DeleteButton from 'components/delete-button';
import Network from 'components/network';
import ScriptPrinterInstallation from 'components/script-printer-installation.component';

import logging from 'services/logging.service';
import actions from 'vuex/actions';
import getters from 'vuex/getters';

export default {
	components: {
		delete: DeleteButton,
		network: Network,
		'script-printer-installation': ScriptPrinterInstallation
	},
	props: {
		printer: { type: Object, required: true },
		site: { type: Object, required: true }
	},
	created() {
		this.printer.site = this.site.id;
	},
	computed: {
		is_forwarding_remote() {
			return this.printer.ports.forward == 'remote';
		},
		from() {
			return this.printer.ports.forward;
		},
		device() {
			var data = null;

			if (
				typeof this.networks !== 'undefined' &&
				typeof this.networks[this.site.hostname] !== 'undefined'
			) {
				data = this.networks[this.site.hostname][this.printer.hostname];
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
		}
	},
	vuex: {
		actions: {
			deletePrinter: actions.deletePrinter,
			getSites: actions.getSites,
			saveFile: actions.saveFile,
			siteRestart: actions.siteRestart
		},
		getters: {
			networks: getters.retrieveNetworks
		}
	}
};
</script>
