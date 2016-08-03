<style>
	.expandable {
		cursor: pointer;
	}

	.btn-toolbar {
		margin-bottom: 0;
	}
</style>
<template>
	<div id="accordion-{{optbox.name}}" role="tablist" aria-multiselectable="true">
		<div class="panel panel-default">
			<div class="panel-heading" role="tab">
				<h6 class="panel-title">
					<heading :optbox="optbox"></heading>
				</h6>
			</div>
			<div id="optbox-{{optbox.name}}" class="panel-collapse collapse in" role="tabpanel"
				 aria-labelledby="optbox-{{optbox.hostname}}">
				<div v-for="printer in printers">
					<printer :printer="printer" :optbox="optbox"></printer>
				</div>
				<div class="text-xs-center">
					<add-printer-button :boitier="optbox" label="Ajouter une imprimante"></add-printer-button>
					<button class="btn btn-info" @click="add_bulk_printers()">
						<i class="fa fa-plus-circle"></i>
						Ajouter des imprimantes
					</button>
				</div>
				<br>
			</div>
		</div>
	</div>
</template>
<script>
	import resource from 'pilou';
	import AddPrinterButtonComponent from './add-printer.component.vue';
	import PrinterComponent from '../printers/printer.component.vue';
	import HeadingComponent from './heading.component.vue';

	const printers = resource('printers', {
				get: '/daemon/${resource}/${optbox}',
				update: '/daemon/${resource}/${optbox}'
			}
	);

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
			'printer': PrinterComponent,
			'heading': HeadingComponent,
		},
		ready() {
			this.getPrinters(this.optbox);
		},
		methods: {
			getPrinters(optbox) {
				printers.get({'optbox': optbox.name}).then((response) => {
					this.printers = response.data.output[0].channels;
				})
			},
		}
	}


</script>
