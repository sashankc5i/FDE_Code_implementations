import type {
    KPIResponse,
    Order,
    Segment
} from "./types";


function formatCurrency(
    value: number
): string {

    return new Intl.NumberFormat(
        "en-IN",
        {
            style: "currency",
            currency: "INR",
            maximumFractionDigits: 0
        }
    ).format(value);
}


export function renderKPIs(
    kpis: KPIResponse
): void {

    const {
        revenue,
        customers,
        orders,
        conversionRate
    } = kpis;

    document.getElementById("revenue")!
        .textContent = formatCurrency(revenue);

    document.getElementById("customers")!
        .textContent = customers.toLocaleString();

    document.getElementById("orders")!
        .textContent = orders.toLocaleString();

    document.getElementById("conversion")!
        .textContent = `${conversionRate}%`;
}


export function renderSegments(
    segments: Segment[]
): void {

    const container =
        document.getElementById("segments");

    if (!container) {
        return;
    }

    container.innerHTML = "";

    segments.forEach(
        ({ name, customers, revenue }) => {

            const row =
                document.createElement("div");

            row.className = "segment-row";

            row.innerHTML = `
                <span>${name}</span>
                <span>${customers.toLocaleString()}</span>
                <span>${formatCurrency(revenue)}</span>
            `;

            container.appendChild(row);
        }
    );
}


export function renderOrders(
    orders: Order[]
): void {

    const tbody =
        document.getElementById("orders");

    if (!tbody) {
        return;
    }

    tbody.innerHTML = "";

    orders.forEach(
        ({ id, customer, revenue, status }) => {

            const row =
                document.createElement("tr");

            row.innerHTML = `
                <td>${id}</td>
                <td>${customer}</td>
                <td>${formatCurrency(revenue)}</td>
                <td>${status}</td>
            `;

            tbody.appendChild(row);
        }
    );
}