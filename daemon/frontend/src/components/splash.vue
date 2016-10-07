<template>
	<div class="modal fade in " id="splash" tabindex="-1" role="dialog" aria-labelledby="splashLabel"
		 aria-hidden="true">
		<div class="modal-dialog" role="document">
			<div class="modal-content bg-danger">
				<div class="modal-header">
					<button type="button" class="close" data-dismiss="modal" aria-label="Close">
						<span aria-hidden="true">&times;</span>
					</button>
					<h4 class="modal-title" id="splashLabel">
						<slot name="title"></slot>
					</h4>
				</div>
				<div class="modal-body">
					<slot name="body"></slot>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-danger pull-left" data-dismiss="modal">
						<slot name="accept"></slot>
					</button>
				</div>
			</div>
		</div>
	</div>
</template>
<script type="text/ecmascript-6">
	export default {
		ready(){
			$('#splash').modal({
				backdrop: 'static',
				show: true
			})
		}
	}
</script>
<style>
	.bg-danger .modal-header {
		border-bottom-color: hsl(2, 64%, 48%);
	}

	.bg-danger .modal-footer {
		border-top-color: hsl(2, 64%, 48%);
	}

	.bg-danger .btn-danger {
		border-color: hsl(2, 64%, 48%);
	}

	.modal-backdrop.in {
		opacity: .75;
	}
</style>
