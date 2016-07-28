<template>
	<div id="optboxes-page">
		<div class="row">
			<div class="col-lg-12">
				<div class="card card-block">
					<div class="row">
						<div class="col-md-12">
							<h3>Boîtiers OPT-box</h3>
						</div>
					</div>
					<div class="row" id="dashboard">
						<span class="col-md-12 text-xs-right">
							<add-optbox-button></add-optbox-button>
						</span>
					</div>

					<br>

					<div class="row">
						<div id="accordion" role="tablist" aria-multiselectable="true">
							<div v-for="optbox in optboxes" class="panel panel-default">
								<opt-box :optbox="optbox"></opt-box>
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
	import Optboxes from '../../services/optboxes';
	import OptBoxComponent from './opt-box.component.vue';
	import AddOptboxButtonComponent from '../../components/add-optbox-button.vue';
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
				optboxes: [
					{
						id: 1,
						location: 'Coaxis Cenon',
						name: '049fed91-6880-4c08-8cb2-21e8579d4543',
						address: '10.1.4.1'
					},
					{
						id: 2,
						location: 'Fauguerolles',
						name: 'd5d3ce56-0e2f-428f-a6c6-8142616f54c7',
						address: '10.1.4.23'
					}
				]
			};
		},
		ready(){
			 this.getOptboxes().then(()=> {
			 	if (this.count == 0) {
			 		this.no_optbox_message = 'there is no optbox'
			 	}
			 });
		},
		components: {
			OrderingArrow,
			'opt-box': OptBoxComponent,
			'add-optbox-button': AddOptboxButtonComponent,
			'logs': LogsComponent,
		},
		methods: {
			moment: function (date) {
				return moment(date);
			},
			getOptboxes(ordering = this.ordering){
				return Optboxes.all(ordering).then(response => {
					this.optboxes = response.data.results;
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
				this.getOptboxes();
			},
			openOptbox(id){
				this.$router.go(`/optboxes/${id}/`);
			},
			addOptbox(optbox){
				this.$router.go(`/optboxes/create/`);
			},
			deleteOptbox(optbox){
				Optboxes.delete(optbox)
						.then(() => {
							logging.success(this.$t('optboxes.delete.succeed'));
							this.getOptboxes();
						})
						.catch(() => {
							logging.error(this.$t('optboxes.delete.failed'))
						});
			}
		}
	}
</script>
