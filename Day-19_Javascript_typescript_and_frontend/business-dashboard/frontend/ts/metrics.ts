import type {
    Order,
    Segment
} from "./types";


export function calculateTotalSegmentRevenue(
    segments: Segment[]
): number {

    return segments.reduce(
        (total, segment) =>
            total + segment.revenue,
        0
    );
}


export function calculateAverageOrderValue(
    orders: Order[]
): number {

    if (orders.length === 0) {
        return 0;
    }

    const totalRevenue = orders.reduce(
        (total, order) =>
            total + order.revenue,
        0
    );

    return totalRevenue / orders.length;
}


export function getCompletedOrders(
    orders: Order[]
): Order[] {

    return orders.filter(
        order =>
            String(order.status).toLowerCase() === "completed"
    );
}