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
								<optbox :optbox="optbox"></optbox>
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
	import OptboxComponent from './optbox.component.vue';
	import AddOptboxButtonComponent from './add-optbox.component.vue';
	import LogsComponent from './logs/logs.component.vue';
	import logging from '../../services/logging';
	import getters from '../../store/getters'
	import actions from '../../store/actions'
	import resource from 'pilou';

	const optboxes = resource('optboxes', {all: '/daemon/${resource}/'});


	export default {
		data() {
			return {
				no_optbox_message: 'loading…'
			};
		},
		ready(){
			this.getOptboxes();
		},
		components: {
			'optbox': OptboxComponent,
			'add-optbox-button': AddOptboxButtonComponent,
			'logs': LogsComponent,
		},
		methods: {
			getOptboxes() {
				optboxes.all().then((response) => {
					this.setOptboxes(response.data.output);
				}).catch(() => {
					this.no_optbox_message = 'there is no optbox';
				});
			}
		},
		events: {
			'log-response': function (message) {
				this.$broadcast('log-response', message);
			},
		},
		vuex: {
			actions: {
				setOptboxes: actions.setOptboxes,
			},
			getters: {
				optboxes: getters.retrieveOptboxes
			}
		}
	}
</script>
