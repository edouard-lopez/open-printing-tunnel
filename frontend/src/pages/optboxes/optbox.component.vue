<style>
	.expandable {
		cursor: pointer;
	}

	.btn-toolbar {
		margin-bottom: 0;
	}
</style>
<template>
	<div id="accordion-{{optbox.id}}" role="tablist" aria-multiselectable="true">
		<div class="panel panel-default">
			<div class="panel-heading" role="tab">
				<h6 class="panel-title">
					<heading :optbox="optbox"></heading>
				</h6>
			</div>
			<div id="optbox-{{optbox.id}}" class="panel-collapse collapse in" role="tabpanel"
				 aria-labelledby="optbox-{{optbox.hostname}}">
				<div v-for="printer in printersList">
					<printer :printer="printer" :optbox="optbox"></printer>
				</div>
				<div class="text-xs-center">
					<add-printer-button :boitier="optbox" label="Ajouter une imprimante"></add-printer-button>
					<add-printers-button :boitier="optbox" label="Ajouter des imprimantes"></add-printers-button>
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

import optboxesService from '../../services/optboxes.service';

	export default{
		data(){
			return {
				printersList: []
			}
		},
		props: {
			optbox: {
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
		created() { this.getPrinters(this.optbox.id); },
		computed: {
			printersList() {
				var index = optboxesService.getIndex(this.optboxesList, this.optbox.id);
				return this.optboxesList[index].printers
			}
		},
		vuex: {
			actions: { getPrinters: actions.getPrinters,},
			getters: { optboxesList: getters.retrieveOptboxes}
		}
	}


</script>
