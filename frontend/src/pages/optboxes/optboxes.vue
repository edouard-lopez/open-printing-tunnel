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
								<optbox-row :optbox="optbox"></optbox-row>
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
	import OptboxRowComponent from './optbox-row.component.vue';
	import AddOptboxButtonComponent from './add-optbox-button.vue';
	import LogsComponent from './logs.component.vue';
	import logging from '../../services/logging';

	export default {
		data() {
			return {
				no_container_message: 'loading…',
				optboxes: [
					{
						name: 'no-data-01',
						hostname: '10.1.4.1'
					},
					{
						name: 'no-data-02',
						hostname: '10.1.4.23'
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
			'optbox-row': OptboxRowComponent,
			'add-optbox-button': AddOptboxButtonComponent,
			'logs': LogsComponent,
		},
		methods: {
			getOptboxes(){
				return Optboxes.all().then(response => {
					this.optboxes = response.data.output;
				})
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
		},
		events: {
			'log-response': function (message) {
				this.$broadcast('log-response', message);
			}
		}
	}
</script>
