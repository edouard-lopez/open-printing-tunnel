<style>
.btn-link .fa-trash-o:focus,
.btn-link .fa-trash-o:hover {
  color: hsl(2, 64%, 48%);
}

.btn-link .fa-trash-o {
  color: hsl(2, 64%, 58%) !important;
}

.delete-button {
  display: inline-block;
}
</style>
<template>
	<div id="delete-button-{{object.site}}-{{object.id}}" class="delete-button">
		<button type="button" class="btn btn-danger {{class}} hint--top-left"
				aria-label="Supprimer {{object.site}}-{{object.id}}…"
				data-toggle="modal"
				data-target="#delete-button-modal-{{object.site}}-{{object.id}}">
			<i class="fa fa-trash-o"></i>
			<slot name="label"></slot>
		</button>
		<div class="modal fade" id="delete-button-modal-{{object.site}}-{{object.id}}" tabindex="-1" role="dialog"
			 aria-labelledby="action-label"
			 aria-hidden="true">
			<div class="modal-dialog" role="document">
				<div class="modal-content text-xs-left">
					<div class="modal-header">
						<button type="button" class="close" data-dismiss="modal" aria-label="Close">
							<span aria-hidden="true">&times;</span>
						</button>
						<h4 class="modal-title" id="action-label">
							<slot name="title"></slot>
						</h4>
					</div>
					<div class="modal-body">
						<slot name="body"></slot>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-link text-danger" v-on:click="confirm()">
							<span v-if="pending">
								<i class="fa fa-spinner fa-pulse fa-fw"></i>
								<slot name="in-progress"></slot>
							</span>
							<span v-else><slot name="action"></slot></span>
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
  data() {
    return {
      pending: false
    };
  },
  props: {
    promise: { type: Function },
    object: { type: Object, required: true },
    class: { type: String }
  },
  methods: {
    confirm() {
      this.pending = true;
      let id = this.object.id;
      this.promise(this.object).then(function() {
        $('#delete-button-modal-' + id).modal('hide');
        $('.modal-backdrop').remove();
      });
    }
  }
};
</script>
