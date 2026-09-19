export function calculateTotalSegmentRevenue(
    segments
) {
    return segments.reduce(
        (total, segment) =>
            total + segment.revenue,
        0
    );
}


export function calculateAverageOrderValue(
    orders
) {
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


export function getCompletedOrders(orders) {
    return orders.filter(
        order => order.status === "Completed"
    );
}