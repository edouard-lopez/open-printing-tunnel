<style>
	.expandable {
		cursor: pointer;
	}
</style>
<template>
	<div class="panel panel-default">
		<div class="panel-heading" role="tab">
			<h5 class="panel-title">
				<div class="row">
					<span class="col-md-5 expandable"
						  data-toggle="collapse"
						  aria-expanded="false"
						  aria-controls="optbox-{{optbox.name}}"
						  data-target="#optbox-{{optbox.name}}"
					>
						<span class="hint--top-right" aria-label="Tooltip on top">
							<i class="tunnel-status fa fa-check text-muted"> </i>
						</span>
						<span class="tunnel-name">
							<b>{{optbox.name}}</b>
						</span>
						<span class="divider"> – </span>
						<span class="tunnel-fqdn text-muted">{{optbox.hostname}}</span>
					</span>
					<div class="col-md-7">
						<ul class="row btn-toolbar pull-md-right" role="toolbar"
							aria-label="Toolbar with button groups">
							<li class="btn-group" role="group" aria-label="Actions publiques">
								<button aria-label="Status"
										role="button"
										class="btn btn-info btn-sm btn-action hide-btn-content hint--top"
										@click="status(optbox.name)"
								>
									<i class="fa fa-info"> </i>
								</button>
								<add-printer-button :boitier="optbox"></add-printer-button>
								<button aria-label="Ajouter des *canaux* par lot"
										role="button"
										class="btn btn-primary btn-sm btn-action hide-btn-content hint--top"
										@click="add_bulk_channels(optbox.name)"
								>
									<i class="fa fa-print"> </i>
								</button>
								<button aria-label="script d'installation d'imprimante"
										role="button"
										class="btn btn-default btn-sm btn-action hide-btn-content hint--top"
										@click="link(optbox.name)"
								>
									<i class="fa fa-comment"> </i>
								</button>
							</li>
							<li class="btn-group" role="group"
								aria-label="Actions d'administration">
								<button aria-label="Redémarrer"
										role="button"
										class="btn btn-warning btn-sm btn-action restart hide-btn-content hint--top"
										@click="restart(optbox.name)"
								>
									<i class="fa fa-refresh"> </i>
								</button>
								<button aria-label="Démarrer"
										role="button"
										class="btn btn-success btn-sm btn-action hide-btn-content hint--top"
										@click="start(optbox.name)"
								>
									<i class="fa fa-play"> </i>
								</button>
								<button aria-label="Arrêter"
										role="button"
										class="btn btn-danger btn-sm btn-action hide-btn-content hint--top"
										@click="stop(optbox.name)"
								>
									<i class="fa fa-stop"> </i>
								</button>
							</li>
							<li class="btn-group" role="group"
								aria-label="Actions non-réversibles">
								<button aria-label="Supprimer cet *hôte*"
										role="button"
										class="btn btn-link btn-sm btn-action hide-btn-content hint--top-left"
										@click="remove_optbox(optbox.name)"
								>
									<i class="fa fa-trash-o text-danger"> </i>
								</button>
							</li>
						</ul>

					</div>
				</div>
			</h5>
		</div>
		<div id="optbox-{{optbox.name}}" class="panel-collapse collapse in" role="tabpanel"
			 aria-labelledby="optbox-{{optbox.hostname}}">
			<div class="row">
				<div id="accordion" class="col-lg-12" role="tablist" aria-multiselectable="true">
				</div>
			</div>
			<div class=row>
				<div class="text-xs-center">
					<button class="btn btn-success" @click="add_printer()">
						<i class="fa fa-plus-circle"></i>
						Ajouter une imprimante
					</button>
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
	import 'bootstrap/dist/js/umd/collapse.js';
	import resource from 'pilou';
	import AddPrinterButtonComponent from './add-printer-button.vue';

	const printers = resource('printers', {update: '/daemon/${resource}/${name}'});

	export default{
		data(){
			return {}
		},
		props: {
			optbox: {
				type: Object,
				required: true
			},
		},
		components: {
			'add-printer-button': AddPrinterButtonComponent,
		},
		methods: {
			status(name) {
				printers.update({name: name}, {action: 'status'}).then(response => {
					this.$dispatch('log-response', response.data);
				});
			},
			start(name) {
				printers.update({name: name}, {action: 'start'}).then(response => {
					this.$dispatch('log-response', response.data);
				});
			},
			stop(name) {
				printers.update({name: name}, {action: 'stop'}).then(response => {
					this.$dispatch('log-response', response.data);
				});
			},
			restart(name) {
				printers.update({name: name}, {action: 'restart'}).then(response => {
					this.$dispatch('log-response', response.data);
				});
			},
		}
	}


</script>
