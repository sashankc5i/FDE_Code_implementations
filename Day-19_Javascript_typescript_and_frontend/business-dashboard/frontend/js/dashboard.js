function formatCurrency(value) {
    return new Intl.NumberFormat(
        "en-IN",
        {
            style: "currency",
            currency: "INR",
            maximumFractionDigits: 0,
        }
    ).format(value);
}


export function renderKPIs(kpis) {

    const {
        revenue,
        customers,
        orders,
        conversionRate,
    } = kpis;

    document.querySelector(
        "#revenue"
    ).textContent = formatCurrency(revenue);

    document.querySelector(
        "#customers"
    ).textContent =
        customers.toLocaleString();

    document.querySelector(
        "#orders"
    ).textContent =
        orders.toLocaleString();

    document.querySelector(
        "#conversion"
    ).textContent =
        `${conversionRate}%`;
}


export function renderSegments(segments) {

    const container =
        document.querySelector(
            "#segments"
        );

    container.innerHTML = "";

    segments.forEach(
        ({ name, customers, revenue }) => {

            const row =
                document.createElement("div");

            row.className =
                "segment-row";

            row.innerHTML = `
                <span>${name}</span>
                <span>
                    ${customers.toLocaleString()}
                </span>
                <span>
                    ${formatCurrency(revenue)}
                </span>
            `;

            container.appendChild(row);
        }
    );
}


export function renderOrders(orders) {

    const tbody =
        document.querySelector(
            "#orders"
        );

    tbody.innerHTML = "";

    orders.forEach(
        ({
            id,
            customer,
            revenue,
            status,
        }) => {

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