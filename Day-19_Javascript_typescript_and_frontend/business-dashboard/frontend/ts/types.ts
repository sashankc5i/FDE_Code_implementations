export type CustomerSegment =
    | "Enterprise"
    | "SMB";


export type OrderStatus =
    | "Completed"
    | "Pending";


export interface KPIResponse {
    period: string;
    revenue: number;
    customers: number;
    orders: number;
    conversionRate: number;
}


export interface CustomerIdentity {
    id: string;
    name: string;
}


export interface RevenueData {
    revenue: number;
}


export type CustomerRevenue =
    CustomerIdentity & RevenueData;


export interface Customer
    extends CustomerIdentity,
        RevenueData {
    segment: CustomerSegment;
}


export interface CustomerResponse {
    customers: Customer[];
}


export interface Order {
    id: string;
    customer: string;
    revenue: number;
    status: OrderStatus;
}


export interface OrderResponse {
    orders: Order[];
}


export interface Segment {
    name: string;
    customers: number;
    revenue: number;
}


export interface SegmentResponse {
    segments: Segment[];
}