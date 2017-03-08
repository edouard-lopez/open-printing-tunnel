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
			<span v-if="!restarting" @click="restart(container.id)"
				  class="tag tag-warning tag-lg hint--bottom"
				  aria-label="Redémarrer">
				<i class="fa fa-refresh fa-fw"></i>
			</span>
		</div>
	</div>
</template>
<script type="text/ecmascript-6">
	import axios from 'axios';

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
			restart(id){
				this.restarting = true;
				return axios.post('/api/containers/' + id, {action: 'restart'}).then(response => {
					this.restarting = false;
				})
			}
		}
	}
</script>
