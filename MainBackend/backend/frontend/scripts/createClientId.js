async function createClientId(serverUrl, ) {
    const clientId = sessionStorage.getItem('ClientId');

    if (clientId == null) {
        const response = await fetch(serverUrl + '/create_client');

        const data = await response.json();
        sessionStorage.setItem('ClientId', data['id'])
    }
}