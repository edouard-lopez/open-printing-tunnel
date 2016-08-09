<template>
	<div id="delete-button">
		<button type="button" class="btn btn-danger {{class}}"
				data-toggle="modal"
				data-target="#delete-button-modal">
			<i class="fa fa-trash"></i>
			<span v-if="label">{{label}}</span>
		</button>
		<div class="modal fade" id="delete-button-modal" tabindex="-1" role="dialog" aria-labelledby="action-label"
			 aria-hidden="true">
			<div class="modal-dialog" role="document">
				<div class="modal-content text-xs-left">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
						<h4 class="modal-title" id="action-label">Supprimer le client</h4>
					</div>
					<div class="modal-body">
						<p>Confirmer la suppression du client et des tunnels associés.</p>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-link text-danger" v-on:click="confirm()">
							Supprimer le client
						</button>
						<button type="button" class="btn btn-secondary" data-dismiss="modal">
							Annuler
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script type="text/ecmascript-6">
	export default {
		props: {
			'event-name': {type: String, required: true},
			object: {type: Object, required: true},
			label: {type: String},
			class: {type: String}
		},
		methods: {
			confirm() {
				this.$dispatch(this.eventName, this.object);
			}
		},
		events: {
			'deleted': (status) => {
				this.actionCompleted = status;
			}
		}
	}
</script>
