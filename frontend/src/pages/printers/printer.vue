<template>
	<div id="printer-page">
		<div class="row">
			<div class="col-md-8">
				<div class="card">
					<div class="card-header">
						<b>{{printer.id}}</b>
						<span class="pull-xs-right">{{ printer.created | moment }}</span>
					</div>
					<div class="card-block">
						<p class="card-text">
							{{printer.error_message}}
							<pre>{{printer.infos | json 4 }}</pre>
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
								  'label-danger': printer.infos.status=='exited' || printer.infos.status=='dead',
								  'label-warning': printer.infos.status=='paused' || printer.infos.status=='restarting',
								  'label-success': printer.infos.status=='running' || printer.infos.status=='created', }"
							>
                                {{printer.infos.status }}
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
							{{ printer.company }}
						</p>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script type="text/ecmascript-6">
	import Printers from '../../services/printers';
	import logging from '../../services/logging';
	import moment from 'moment';

	Printers.localStorage = localStorage;
	export default {
		data() {
			return {
				printer: {}
			};
		},
		ready(){
			Printers.get(this.$route.params.id).then(printer => {
				this.printer = printer;
			});
		},
		filters: {
			moment: function (date) {
				return moment(date).format('MMMM Do YYYY, h:mm:ss');
			},
		}
	};
</script>

