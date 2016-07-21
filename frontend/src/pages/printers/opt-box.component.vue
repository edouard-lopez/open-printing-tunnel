<template>
	<div class="panel panel-default">
		<div class="panel-heading" role="tab" id="heading-host-{{printer.location}}">
			<h5 class="panel-title"
				data-toggle="collapse"
				data-parent="#accordion"
				href="#host-{{printer.opt_box}}"
				aria-expanded="false"
				aria-controls="host-{{printer.location}}"
			>
				<div class="row">
					<span class="col-md-6">
						<span class="hint--top-right" aria-label="Tooltip on top">
							<i class="tunnel-status fa fa-check text-muted"> </i>
						</span>
						<span class="tunnel-name">
							<b>{{printer.location}}</b>
						</span>
						<span class="divider"> – </span>
						<span class="tunnel-fqdn text-muted">{{printer.address}}</span>
					</span>

					<div class="col-md-6">
						<ul class="btn-toolbar pull-md-right" role="toolbar"
							aria-label="Toolbar with button groups">
							<li class="btn-group" role="group" aria-label="Actions publiques">
								<button title="Status" role="button"
										class="btn btn-info btn-sm btn-action hide-btn-content hint--top"
										data-name="{printer.location}}"
										data-action="status"
										data-redirect="false"
										data-href="./"
										data-target="#modal-status"
										aria-label="Status"
								>
									<i class="fa fa-info"> </i>
								</button>
								<button
										role="button"
										class="btn btn-success btn-sm btn-action hide-btn-content hint--top"
										data-name="{printer.location}}"
										data-action="add-channel"
										data-redirect="false"
										data-href="./"
										data-target="#modal-add-channel"
										aria-label="Ajouter un *canal*"
										@click="addPrinter()"
								>
									<i class="fa fa-plus-circle"> </i>
								</button>
								<button
										role="button"
										class="btn btn-primary btn-sm btn-action hide-btn-content hint--top"
										data-name="{printer.location}}"
										data-action="add-bulk-channels"
										data-redirect="false"
										data-href="./"
										data-target="#modal-add-bulk-channels"
										aria-label="Ajouter des *canaux* par lot"
										@click="addPrinter()"
								>
									<i class="fa fa-print"> </i>
								</button>
								<button
										role="button"
										class="btn btn-default btn-sm btn-action hide-btn-content hint--top"
										data-name="{printer.location}}"
										data-action="link"
										data-redirect="true"
										data-href="./home/getScript/PORTS/eyJyZW1vdGVIb3N0IjoiMTcyLjE4LjAuMSIsInJlbW90ZVBvcnQiOjIyLCJjaGFubmVscyI6W3sibG9jYWxIb3N0IjoiKiIsImxvY2FsUG9ydCI6IjkxMDIiLCJyZW1vdGVIb3N0IjoiMS4yLjMuNCIsInJlbW90ZVBvcnQiOiI5MTAwIiwiY29tbWVudCI6ImFrZW1hIn1dLCJzaXRlIjoiYWxiYW4taG9tZSJ9"
										data-target="#modal-link"
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
										data-name="{printer.location}}"
										data-action="restart"
										data-redirect="false"
										data-href="./"
										data-target="#modal-restart"
										aria-label="Redémarrer"
								>
									<i class="fa fa-refresh"> </i>
								</button>
								<button
										role="button"
										class="btn btn-success btn-sm btn-action hide-btn-content hint--top"
										data-name="{printer.location}}"
										data-action="start"
										data-redirect="false"
										data-href="./"
										data-target="#modal-start"
										aria-label="Démarrer"
								>
									<i class="fa fa-play"> </i>
								</button>
								<button
										role="button"
										class="btn btn-danger btn-sm btn-action hide-btn-content hint--top"
										data-name="{printer.location}}"
										data-action="stop"
										data-redirect="false"
										data-href="./"
										data-target="#modal-stop"
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
										data-name="{printer.location}}"
										data-action="remove-host"
										data-redirect="false"
										data-href="./"
										data-target="#modal-remove-host"
										aria-label="Supprimer cet *hôte*"
								>
									<i class="fa fa-trash text-danger"> </i>
								</button>
							</li>
						</ul>

					</div>
				</div>
			</h5>
		</div>
		<div id="host-{{printer.opt_box}}" class="panel-collapse collapse" role="tabpanel"
			 aria-labelledby="heading-host-{{printer.location}}">
			<div class="text-xs-center">
				<button class="btn btn-success" @click="addPrinter()">
					<i class="fa fa-plus-circle"></i>
					Ajouter une imprimante
				</button>
				<button class="btn btn-info" @click="addPrinter()">
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
        	printer: {
				type: Object,
				required: true
			},
		}
    }





</script>
