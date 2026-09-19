import type {
    KPIResponse,
    CustomerResponse,
    OrderResponse,
    SegmentResponse
} from "./types";


const API_BASE_URL: string =
    "http://127.0.0.1:8000";


async function fetchAPI<T>(
    endpoint: string
): Promise<T> {

    try {
        const response = await fetch(
            `${API_BASE_URL}${endpoint}`
        );

        if (!response.ok) {
            throw new Error(
                `HTTP ${response.status}: ${response.statusText}`
            );
        }

        return await response.json() as T;

    } catch (error) {

        console.error(
            `API Error [${endpoint}]:`,
            error
        );

        throw error;
    }
}


export async function getKPIs(): Promise<KPIResponse> {
    return await fetchAPI<KPIResponse>(
        "/api/kpis"
    );
}


export async function getCustomers(): Promise<CustomerResponse> {
    return await fetchAPI<CustomerResponse>(
        "/api/customers"
    );
}


export async function getOrders(): Promise<OrderResponse> {
    return await fetchAPI<OrderResponse>(
        "/api/orders"
    );
}


export async function getSegments(): Promise<SegmentResponse> {
    return await fetchAPI<SegmentResponse>(
        "/api/segments"
    );
}