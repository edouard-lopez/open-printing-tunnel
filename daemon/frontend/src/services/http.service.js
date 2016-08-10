import pilou from 'pilou';

module.exports = function (resourceName, localStorage) {
  const resources = pilou(resourceName);
  return {
    localStorage,
    getRequestConfig() {
      const token = this.localStorage.getItem('token');
      return {
        headers: {Authorization: `JWT ${token}`}
      };
    },
    create(resource) {
      return resources.create(resource, this.getRequestConfig());
    },
    all(params = {}) {
      const config = this.getRequestConfig();
      config.params = params;
      return resources.all(config);
    },
    get(resource) {
      return resources.get(resource, this.getRequestConfig());
    },
    update(resource) {
      return resources.update({id: resource.id}, resource, this.getRequestConfig());
    },
    delete(resource) {
      return resources.delete(resource, this.getRequestConfig());
    }
  };
};
