<template>
	<div id="container-page">
		<div class="row">
			<div class="col-md-8">
				<div class="card">
					<div class="card-header">
						<b>{{container.id}}</b>
						<span class="pull-xs-right">{{ container.created | moment }}</span>
					</div>
					<div class="card-block">
						<p class="card-text">
							{{container.error_message}}
							<pre>{{container.infos | json 4 }}</pre>
						</p>
					</div>
				</div>
			</div>
			<div class="col-md-4">
				<div class="card">
					<h5 class="card-header">
						<i class="fa fa-cog" aria-hidden="true"></i>
						Status
					</h5>
					<div class="card-block">
						<p class="card-text">
                            <span class="label label-lg"
								  v-bind:class="{
								  'label-danger': container.infos.status=='exited' || container.infos.status=='dead',
								  'label-warning': container.infos.status=='paused' || container.infos.status=='restarting',
								  'label-success': container.infos.status=='running' || container.infos.status=='created', }"
							>
                                {{container.infos.status }}
							</span>
						</p>
					</div>
				</div>
				<div class="card">
					<h5 class="card-header">
						<i class="fa fa-home" aria-hidden="true"></i>
						Société
					</h5>
					<div class="card-block">
						<p class="card-text">
							{{ container.company.name }}
						</p>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script type="text/ecmascript-6">
	import Containers from '../../services/containers.service';

	import logging from '../../services/logging.service';
	import moment from 'moment';

	Containers.localStorage = localStorage;
	export default {
		data() {
			return {
				container: {}
			};
		},
		ready(){
			Containers.get(this.$route.params.id).then(container => {
				this.container = container;
			});
		},
		filters: {
			moment: function (date) {
				return moment(date).format('MMMM Do YYYY, h:mm:ss');
			},
		}
	};
</script>

