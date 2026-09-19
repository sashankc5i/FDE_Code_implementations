import {
    getKPIs,
    getCustomers,
    getOrders,
    getSegments
} from "./api";

import {
    calculateAverageOrderValue,
    getCompletedOrders
} from "./metrics";

import {
    renderKPIs,
    renderSegments,
    renderOrders
} from "./dashboard";


async function loadDashboard(): Promise<void> {

    showLoading();
    hideError();

    try {

        const results = await Promise.allSettled([
            getKPIs(),
            getCustomers(),
            getOrders(),
            getSegments()
        ]);


        const [
            kpisResult,
            customersResult,
            ordersResult,
            segmentsResult
        ] = results;


        if (kpisResult.status === "fulfilled") {

            renderKPIs(
                kpisResult.value
            );
        }


        if (segmentsResult.status === "fulfilled") {

            renderSegments(
                segmentsResult.value.segments
            );
        }


        if (ordersResult.status === "fulfilled") {

            renderOrders(
                ordersResult.value.orders
            );

            const averageOrderValue =
                calculateAverageOrderValue(
                    ordersResult.value.orders
                );

            const completedOrders =
                getCompletedOrders(
                    ordersResult.value.orders
                );

            console.log(
                "Average Order Value:",
                averageOrderValue
            );

            console.log(
                "Completed Orders:",
                completedOrders.length
            );
        }


        if (customersResult.status === "fulfilled") {

            console.log(
                "Customers:",
                customersResult.value.customers
            );
        }


        const failedAPIs: string[] = [];


        if (kpisResult.status === "rejected") {
            failedAPIs.push("KPIs");
        }

        if (customersResult.status === "rejected") {
            failedAPIs.push("Customers");
        }

        if (ordersResult.status === "rejected") {
            failedAPIs.push("Orders");
        }

        if (segmentsResult.status === "rejected") {
            failedAPIs.push("Segments");
        }


        if (failedAPIs.length > 0) {

            showError(
                `Some dashboard services are unavailable: ${failedAPIs.join(", ")}`
            );
        }

    } catch (error) {

        console.error(
            "Unexpected dashboard error:",
            error
        );

        showError(
            "Unable to load dashboard."
        );

    } finally {

        hideLoading();
    }
}


function showLoading(): void {

    const loading =
        document.getElementById("loading");

    if (loading) {
        loading.style.display = "block";
    }
}


function hideLoading(): void {

    const loading =
        document.getElementById("loading");

    if (loading) {
        loading.style.display = "none";
    }
}


function showError(
    message: string
): void {

    const errorElement =
        document.getElementById("error");

    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = "block";
    }
}


function hideError(): void {

    const errorElement =
        document.getElementById("error");

    if (errorElement) {
        errorElement.style.display = "none";
    }
}


loadDashboard();