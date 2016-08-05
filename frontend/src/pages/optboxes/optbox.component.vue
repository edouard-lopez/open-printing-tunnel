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
				<div v-for="printer in printers">
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

	import actions from '../../store/actions';
	import getters from '../../store/getters';
	import printersService from '../../services/printers';
	import resource from 'pilou';

	const printers = resource('printers', {get: '/daemon/optboxes/${optbox_id}/${resource}/'});

	export default{
		data(){
			return {
				printers: []
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
		ready() {
			this.getPrinters(this.optbox);
		},
		methods: {
			getPrinters(optbox) {
				printers.get({optbox_id: optbox.id}).then(response => {
					this.printers = response.data.output[0].channels;
				});
			}
		},
		events: {
			'printer-created': (printer) => {
				console.info('printer-created');
				console.log(printer);
				this.getPrinters(printer.optbox);
			},
			'printer-deleted': (printer) => { printersService.remove(this.printers, printer.id) }
		}
	}


</script>
