<style scoped>
	.table thead th, .table td, .table th {
		border: none;
	}
</style>
<template>
	<div id="container-page">
		{{ client | json 4}}
	</div>
</template>
<script type="text/ecmascript-6">
	import HTTP from 'services/http.service';
	import Logging from '../../services/logging.service';
	import Moment from 'moment';

	const ClientsService = HTTP('clients', localStorage);

	ClientsService.localStorage = localStorage;
	export default {
		data() {
			return {
				client: null
			};
		},
		ready(){
			this.getClient(this.$route.params.id);
		},
		methods: {
			getClient(id){
				return ClientsService.get({id}).then(response => {
					this.client = response.data;
				});
			},
		},
		filters: {
			moment: function (date) {
				return Moment(date).format('MMMM Do YYYY, h:mm:ss');
			}
		}
	};
</script>

