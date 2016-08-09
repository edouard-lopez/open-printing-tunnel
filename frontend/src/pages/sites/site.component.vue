<style>
	.expandable {
		cursor: pointer;
	}

	.btn-toolbar {
		margin-bottom: 0;
	}
</style>
<template>
	<div id="accordion-{{site.id}}" role="tablist" aria-multiselectable="true">
		<div class="panel panel-default">
			<div class="panel-heading" role="tab">
				<h6 class="panel-title">
					<heading :site="site"></heading>
				</h6>
			</div>
			<div id="site-{{site.id}}" class="panel-collapse collapse in" role="tabpanel"
				 aria-labelledby="site-{{site.hostname}}">
				<div v-for="printer in printersList">
					<printer :printer="printer" :site="site"></printer>
				</div>
				<div class="text-xs-center">
					<add-printer-button :boitier="site" label="Ajouter une imprimante"></add-printer-button>
					<add-printers-button :boitier="site" label="Ajouter des imprimantes"></add-printers-button>
				</div>
				<br>
			</div>
		</div>
	</div>
</template>
<script>
	import AddPrinterButtonComponent from './add-printer.component.vue';
	import AddPrintersButtonComponent from './add-printers.component.vue';
	import HeadingComponent from './heading.component.vue';
	import PrinterComponent from './printers/printer.component.vue';

	import actions from '../../vuex/actions';
	import getters from '../../vuex/getters';
	import logging from '../../services/logging.service';

import sitesService from '../../services/sites.service';

	export default{
		data(){
			return {
				printersList: []
			}
		},
		props: {
			site: {
				type: Object,
				required: true
			},
		},
		components: {
			'add-printer-button': AddPrinterButtonComponent,
			'add-printers-button': AddPrintersButtonComponent,
			'printer': PrinterComponent,
			'heading': HeadingComponent,
		},
		created() { this.getPrinters(this.site.id); },
		computed: {
			printersList() {
				var index = sitesService.getIndex(this.sitesList, this.site.id);
				return this.sitesList[index].printers
			}
		},
		vuex: {
			actions: { getPrinters: actions.getPrinters,},
			getters: { sitesList: getters.retrieveSites}
		}
	}


</script>
