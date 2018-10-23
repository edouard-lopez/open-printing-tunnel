<template>
	<span v-if="device" class="ping hint--top-right" aria-label="ping: {{ device.ping | time }}">
		<i class="tunnel-status fa {{ device.ping | icon 'ping' }}"> </i>
	</span>
	<span v-if="device" class="telnet hint--top-right" aria-label="telnet (via tunnel): {{ device.telnet | reachable }}">
		<i class="tunnel-status fa {{ device.telnet | icon 'telnet' }}"> </i>
	</span>
</template>
<script type="text/ecmascript-6">
import network from './network.filter';

export default {
  props: {
    device: {
      type: Object,
      default: function() {
        return { ping: 0, telnet: 0 };
      }
    }
  },
  filters: {
    time: network.time,
    icon: network.icon,
    reachable: network.reachable
  }
};
</script>
<style>
.ping {
  text-shadow: 2px 0 0px #fff;
  z-index: 1;
  margin-left: 0.5em;
}

.telnet {
  left: -12px;
}
</style>
