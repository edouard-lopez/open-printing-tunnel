<style>
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
				<div v-for="printer in printers">
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
	import AddPrinterButtonComponent from './add-printer.component';
	import AddPrintersButtonComponent from './add-printers.component';
	import HeadingComponent from './heading.component';
	import PrinterComponent from './printers/printer.component';

	import actions from '../../vuex/actions';
	import getters from '../../vuex/getters';
	import logging from '../../services/logging.service';

	import sitesService from '../../services/sites.service';

	export default{
		props: {
			site: {
				type: Object,
				required: true
			}
		},
		components: {
			'add-printer-button': AddPrinterButtonComponent,
			'add-printers-button': AddPrintersButtonComponent,
			'printer': PrinterComponent,
			'heading': HeadingComponent,
		},
		computed() {
			this.printers = this.site.channels;
		}
 	}


</script>
