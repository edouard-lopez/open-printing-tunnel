<template>
	<div class="row xx-large">
		<div class="col-xs-12">
			<span v-if="!restarting" class="tag tag-lg"
				  v-bind:class="{ 'tag-danger': status=='exited', 'tag-warning': status=='paused', 'tag-success': status=='running'}">
				{{status}}
			</span>
			<span v-if="restarting" class="tag tag-warning tag-lg">
				Redémarrage…
				<i class="fa fa-refresh fa-spin fa-fw"></i>
			</span>
			<span v-if="!restarting" @click="restart(container)"
				  class="tag tag-warning tag-lg hint--top"
				  aria-label="Redémarrer">
				<i class="fa fa-refresh fa-fw"></i>
			</span>
		</div>
	</div>
</template>
<script type="text/ecmascript-6">
	import HTTP from 'services/http.service';

	const ContainersService = HTTP('containers', localStorage);

	export default {
		data() {
			return {
				restarting: false,

			}
		},
		props: {
			container: {
				type: Object, default: {id: null, container_info: {State: {status: 'paused'}}}
			},
		},
		computed: {
			status: function () {
				return this.container.container_info.State.Status;
			}
		},
		methods: {
			restart(container){
				this.restarting = true;
				ContainersService.create({id: container.id, action: 'restart'}).then(response => {
					this.restarting = false;
				})
			}
		}
	}
</script>
