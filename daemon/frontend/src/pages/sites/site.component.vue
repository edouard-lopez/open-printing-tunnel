<style>
.btn-toolbar {
  margin-bottom: 0;
}
</style>
<template>
	<div id="accordion-{{site.id}}" role="tablist" aria-multiselectable="true">
		<div class="panel panel-default">
			<div class="panel-heading" role="tab">
				<h6 class="panel-title">
					<heading :site="site"></heading>
				</h6>
			</div>
			<div id="site-{{site.id}}" class="panel-collapse collapse" v-bind:class="expand" role="tabpanel"
				 aria-labelledby="site-{{site.hostname}}" data-e2e="site">
				<div class="printer" v-for="printer in printers">
					<printer :printer="printer" :site="site"></printer>
				</div>

				<div class="text-xs-center">
					<br>
					<add-printer-button :site="site" label="Ajouter une imprimante"></add-printer-button>
					<add-printers-button :site="site" label="Ajouter des imprimantes"></add-printers-button>
				</div>
			</div>
		</div>
	</div>
</template>
<script>
import AddPrinterButtonComponent from './add-printer.component';
import AddPrintersButtonComponent from './add-printers.component';
import HeadingComponent from './site-heading.component.vue';
import PrinterComponent from './printers/printer.component';

import actions from 'vuex/actions';
import getters from 'vuex/getters';
import logging from 'services/logging.service';

export default {
  props: {
    site: {
      type: Object,
      required: true
    },
    index: { type: Number }
  },
  components: {
    'add-printer-button': AddPrinterButtonComponent,
    'add-printers-button': AddPrintersButtonComponent,
    printer: PrinterComponent,
    heading: HeadingComponent
  },
  computed: {
    printers: function() {
      return this.site.channels;
    },
    expand: function() {
      const expandClass = this.index === 0 ? 'in' : '';
      return expandClass;
    }
  }
};
</script>
