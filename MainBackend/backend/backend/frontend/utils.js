class ApiRequests {
    constructor(serverUrl, prefix) {
        this.serverUrl = serverUrl
        this.prefix = prefix
    }

    createUrl(url, query) {
        return this.serverUrl + '/' + this.prefix + '/' + url + "?" + query
    }

    async get(url, query='') {
        const response = await fetch(this.createUrl(url, query));
        return response;
    }

    async post(url, query='', body={}) {
        const response = await fetch(this.createUrl(url, query),
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body:JSON.stringify(body)
            }
        );

        return response;
    }
}

class ClientApiRequests extends ApiRequests {
    constructor(serverUrl, prefix, clientId) {
        super(serverUrl, prefix)
        this.clientId = clientId
    }

    createUrl(url, query) {
        return this.serverUrl + "/" + this.prefix + '/' +url + '?client_id=' + this.clientId + '&' + query
    }
}