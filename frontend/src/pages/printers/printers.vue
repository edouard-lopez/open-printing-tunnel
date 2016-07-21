<template>
	<div id="printers-page">
		<div class="row">
			<div class="col-lg-12">
				<div class="card card-block">
					<h2 class="row" id="dashboard">
						<span class="col-md-8">
							<span>Boitiers OPT</span>
						</span>
						<span class="col-md-4 text-xs-right">
							<button class="btn btn-success" @click="addPrinter()">
								<i class="fa fa-plus-circle"></i>
								Ajouter un boitier
							</button>
						</span>
					</h2>

					<br>

					<div class="row">
						<div id="accordion" role="tablist" aria-multiselectable="true">
							<div v-for="printer in printers" class="panel panel-default">
								<opt-box :printer="printer"></opt-box>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div class="row">
			<div class="col-lg-12">
				<div class="card card-block">
					<logs></logs>
				</div>

			</div>
		</div>
	</div>
</template>

<script type="text/ecmascript-6">
	import Printers from '../../services/printers';
	import OptBoxComponent from './opt-box.component.vue';
	import LogsComponent from './logs.component.vue';
	import OrderingArrow from '../../components/ordering-arrow';
	import moment from 'moment';
	import logging from '../../services/logging';
	import 'bootstrap/dist/js/umd/collapse.js';

	export default {
		data() {
			return {
				count: 1,
				ordering: '-created',
				sorting: 'asc',
				no_container_message: 'loading…',
				printers: [
					{
						id: 1,
						location: 'salle de réunion (Cenon)',
						opt_box: '049fed91-6880-4c08-8cb2-21e8579d4543',
						address: '10.1.4.1'
					},
					{
						id: 2,
						location: 'Secrétariat',
						opt_box: 'd5d3ce56-0e2f-428f-a6c6-8142616f54c7',
						address: '10.1.4.23'
					},
				]
			};
		},
		ready(){
			// this.getPrinters().then(()=> {
			// 	if (this.count == 0) {
			// 		this.no_printer_message = 'there is no printer'
			// 	}
			// });
		},
		components: {
			OrderingArrow,
			'opt-box': OptBoxComponent,
			'logs': LogsComponent,
		},
		methods: {
			moment: function (date) {
				return moment(date);
			},
			getPrinters(ordering = this.ordering){
				return Printers.all(ordering).then(response => {
					this.printers = response.data.results;
					this.count = response.data.count;
					this.numberPages = Math.ceil(this.count / this.limit);
				})
			},
			sort(field){
				if (this.sorting == 'asc') {
					this.sorting = 'desc';
					this.ordering = field;
				} else {
					this.sorting = 'asc';
					this.ordering = `-${field}`;
				}
				this.getPrinters();
			},
			openPrinter(id){
				this.$router.go(`/printers/${id}/`);
			},
			addPrinter(printer){
				this.$router.go(`/printers/create/`);
			},
			deletePrinter(printer){
				Printers.delete(printer)
						.then(() => {
							logging.success(this.$t('printers.delete.succeed'));
							this.getPrinters();
						})
						.catch(() => {
							logging.error(this.$t('printers.delete.failed'))
						});
			}
		}
	}
</script>
