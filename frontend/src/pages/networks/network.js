export default {
	isEmptyNetwork(network){
		return Object.keys(network.Containers).length === 0
	},
	addLowercaseId(networks) {
		for (const network of networks) {
				network['id'] = network['Id'];
		}
		return networks;
	}
}
