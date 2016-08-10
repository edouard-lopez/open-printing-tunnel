<style scoped>
	.table thead th, .table td, .table th {
		border: none;
	}
</style>
<template>
	<div>
		<div class="row">
			<div class="col-md-8">
				<div class="card">
					<h5 class="card-header">
						<i class="fa fa-map-marker" aria-hidden="true"></i> Daemon pour {{ daemon.client.name }}
					</h5>
					<div class="card-block">
						<ul class="list-unstyled">
							<li><b>IP</b>: {{ daemon.ip }}</li>
							<li><b>Subnet</b>: {{ daemon.subnet }}</li>
							<li><b>Gateway</b>: {{ daemon.gateway }}</li>
							<li><b>VLAN</b>: {{ daemon.vlan }}</li>
						</ul>
					</div>
				</div>
			</div>
			<div class="col-md-4">
				<div class="card">
					<h5 class="card-header">
						Status
					</h5>
					<div class="card-block">
						<h3>
							<span class="tag tag-lg"
								  v-bind:class="{ 'tag-danger': daemon.container_info.State.Status=='exited', 'tag-warning': daemon.container_info.State.Status=='paused', 'tag-success': daemon.container_info.State.Status=='running'}">
                                {{daemon.container_info.State.Status }}
							</span>
						</h3>
					</div>
				</div>
				<div class="card">
					<h5 class="card-header">
						<i class="fa fa-home" aria-hidden="true"></i>
						Société
					</h5>
					<div class="card-block">
						<p class="card-text">
							{{ daemon.client.name }}
						</p>
					</div>
				</div>
			</div>
		</div>
		<div class="row">
			<div class="col-xs-12">
				<div class="card">
					<h6 class="card-header">
						<i class="fa fa-info-circle" aria-hidden="true"></i> Daemon id : {{daemon.id}}
						<span class="pull-xs-right">{{ daemon.created | moment }}</span>
					</h6>
					<div class="card-block">
						<p class="card-text">
							{{daemon.error_message}}
						<pre>{{daemon | json 4 }}</pre>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script type="text/ecmascript-6">
	import HTTP from 'services/http.service';
	import Logging from 'services/logging.service';
	import moment from 'moment';

	const DaemonService = HTTP('daemons', localStorage);

	export default {
		data() {
			return {
				daemon: null
			};
		},
		ready(){
			this.getDaemon(this.$route.params.id);
		},
		methods: {
			getDaemon(id){
				return DaemonService.get({id}).then(response => {
					this.daemon = response.data;
				});
			},
		},
		filters: {
			moment: function (date) {
				return moment(date).format('MMMM Do YYYY, h:mm:ss');
			},
		}
	};
</script>
