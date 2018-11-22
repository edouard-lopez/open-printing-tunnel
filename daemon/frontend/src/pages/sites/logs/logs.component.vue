<template>
	<div id="logs">
		<div class="row">
			<h3 class="col-md-8">
				<i class="fa fa-newspaper-o text-muted"></i>
				Console
			</h3>
			<div class="col-md-4">
				<ul class="btn-toolbar pull-right" role="toolbar"
					aria-label="Toolbar with button groups">
					<li class="btn-group" role="group" aria-label="Actions publiques">
						<button aria-label="Nettoyer le log"
								data-e2e=clear-logs
								title="Clear" 
								role="button"
								class="btn btn-default btn-sm hide-btn-content hint--top-left"
								@click="clear()"
						>
							<i class="fa fa-trash-o"> </i>
						</button>
					</li>
				</ul>
			</div>
		</div>
		<div class="row">
			<div class="col-xs-12 highlight">
				<pre class="stdout" data-e2e=stdout><samp v-for="line in log" class="line">{{line | json }}</samp></pre>
			</div>
		</div>
	</div>
</template>

<script type="text/ecmascript-6">
import logging from 'services/logging.service';
import actions from 'vuex/actions';
import getters from 'vuex/getters';

export default {
  vuex: {
    actions: {
      clear: actions.clearLog
    },
    getters: {
      log: getters.retrieveLog
    }
  }
};
</script>
<style>
.highlight {
  margin-right: 0;
  margin-left: 0;
}

.stdout {
  background-color: #f7f7f9;
  margin-bottom: 0;
  padding: 0.5rem;
}

.line {
  display: block;
}
</style>
