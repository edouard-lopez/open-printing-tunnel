<template>
	<div id="container-page">
		<div class="row">
			<div class="col-md-8">
				<div class="card">
					<h5 class="card-header">
						<i class="fa fa-print" aria-hidden="true"></i> Imprimantes
					</h5>
					<div class="card-block">
						<p class="card-text">

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
						<h3>
							<span class="tag tag-lg"
								  v-bind:class="{
								  'tag-danger': container.container_info.State.Status=='exited' || container.container_info.State.Status=='dead',
								  'tag-warning': container.container_info.State.Status=='paused' || container.container_info.State.Status=='restarting',
								  'tag-success': container.container_info.State.Status=='running' || container.container_info.State.Status=='created', }">
                                {{container.container_info.State.Status }}
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
							{{ container.company.name }}
						</p>
					</div>
				</div>
			</div>
		</div>
		<div class="row">
			<div class="col-xs-12">
				<div class="card">
					<h6 class="card-header">
						<i class="fa fa-info-circle" aria-hidden="true"></i> Conteneur id : {{container.id}}
						<span class="pull-xs-right">{{ container.created | moment }}</span>
					</h6>
					<div class="card-block">
						<p class="card-text">
							{{container.error_message}}
						<pre>{{container.container_info | json 4 }}</pre>
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

