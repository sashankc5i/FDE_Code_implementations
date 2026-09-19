const API_BASE_URL = "http://127.0.0.1:8000";


async function fetchAPI(endpoint) {
    try {

        const response = await fetch(
            `${API_BASE_URL}${endpoint}`
        );

        if (!response.ok) {
            throw new Error(
                `HTTP ${response.status}: ${response.statusText}`
            );
        }

        return await response.json();

    } catch (error) {

        console.error(
            `API Error [${endpoint}]:`,
            error
        );

        throw error;
    }
}


export async function getKPIs() {
    return await fetchAPI("/api/kpis");
}


export async function getCustomers() {
    return await fetchAPI("/api/customers");
}


export async function getOrders() {
    return await fetchAPI("/api/orders");
}


export async function getSegments() {
    return await fetchAPI("/api/segments");
}