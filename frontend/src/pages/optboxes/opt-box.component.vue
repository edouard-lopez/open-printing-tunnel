<style>
	.expandable {
		cursor: pointer;
	}
</style>
<template>
	<div class="panel panel-default">
		<div class="panel-heading" role="tab" id="heading-host-{{optbox.location}}">
			<h5 class="panel-title">
				<div class="row">
					<span class="col-md-6 expandable"
						  data-toggle="collapse"
						  aria-expanded="false"
						  aria-controls="host-{{optbox.hostname}}"
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

					<div class="col-md-6">
						<ul class="btn-toolbar pull-md-right" role="toolbar"
							aria-label="Toolbar with button groups">
							<li class="btn-group" role="group" aria-label="Actions publiques">
								<button title="Status" role="button"
										class="btn btn-info btn-sm btn-action hide-btn-content hint--top"
										@click="status(optbox.name)"
										aria-label="Status"
								>
									<i class="fa fa-info"> </i>
								</button>
								<button
										role="button"
										class="btn btn-success btn-sm btn-action hide-btn-content hint--top"
										@click="add_channel(optbox.name)"
										aria-label="Ajouter un *canal*"
								>
									<i class="fa fa-plus-circle"> </i>
								</button>
								<button
										role="button"
										class="btn btn-primary btn-sm btn-action hide-btn-content hint--top"
										@click="add_bulk_channels(optbox.name)"
										aria-label="Ajouter des *canaux* par lot"
								>
									<i class="fa fa-print"> </i>
								</button>
								<button
										role="button"
										class="btn btn-default btn-sm btn-action hide-btn-content hint--top"
										@click="link(optbox.name)"
										aria-label="script d'installation d'imprimante"
								>
									<i class="fa fa-comment"> </i>
								</button>
							</li>
							<li class="btn-group" role="group"
								aria-label="Actions d'administration">
								<button
										role="button"
										class="btn btn-warning btn-sm btn-action restart hide-btn-content hint--top"
										@click="restart(optbox.name)"
										aria-label="Redémarrer"
								>
									<i class="fa fa-refresh"> </i>
								</button>
								<button
										role="button"
										class="btn btn-success btn-sm btn-action hide-btn-content hint--top"
										@click="start(optbox.name)"
										aria-label="Démarrer"
								>
									<i class="fa fa-play"> </i>
								</button>
								<button
										role="button"
										class="btn btn-danger btn-sm btn-action hide-btn-content hint--top"
										@click="stop(optbox.name)"
										aria-label="Arrêter"
								>
									<i class="fa fa-stop"> </i>
								</button>
							</li>
							<li class="btn-group" role="group"
								aria-label="Actions non-réversibles">
								<button
										role="button"
										class="btn btn-link btn-sm btn-action hide-btn-content hint--top-left"
										@click="remove_host(optbox.name)"
										aria-label="Supprimer cet *hôte*"
								>
									<i class="fa fa-trash-o text-danger"> </i>
								</button>
							</li>
						</ul>

					</div>
				</div>
			</h5>
		</div>
		<div id="host-{{optbox.name}}" class="panel-collapse collapse" role="tabpanel"
			 aria-labelledby="heading-host-{{optbox.hostname}}">
			<div class="text-xs-center">
				<button class="btn btn-success" @click="add_printer()">
					<i class="fa fa-plus-circle"></i>
					Ajouter une imprimante
				</button>
				<button class="btn btn-info" @click="add_printer()">
					<i class="fa fa-plus-circle"></i>
					Ajouter des imprimantes
				</button>
			</div>
			<br>
		</div>
	</div>
</template>
<script>
    export default{
        data(){
            return{
                msg:'hello vue'
            }
        },
        props: {
        	optbox: {
				type: Object,
				required: true
			},
		}
    }





</script>
