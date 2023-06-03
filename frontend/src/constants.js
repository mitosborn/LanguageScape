let DEV_BACKEND_ENDPOINT = 'http://127.0.0.1:8000';
let IS_DEV = true;

export function getBackendEndpoint() {
    if(IS_DEV) {
        return DEV_BACKEND_ENDPOINT;
    }
}