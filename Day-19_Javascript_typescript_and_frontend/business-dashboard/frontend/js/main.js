import {
    getKPIs,
    getCustomers,
    getOrders,
    getSegments
} from "./api.js";

import {
    calculateAverageOrderValue,
    getCompletedOrders
} from "./metrics.js";

import {
    renderKPIs,
    renderSegments,
    renderOrders
} from "./dashboard.js";


async function loadDashboard() {
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


        // Render KPI data if available
        if (kpisResult.status === "fulfilled") {
            renderKPIs(kpisResult.value);
        }


        // Render segment data if available
        if (segmentsResult.status === "fulfilled") {
            renderSegments(
                segmentsResult.value.segments
            );
        }


        // Render order data if available
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


        // Log customer data if available
        if (customersResult.status === "fulfilled") {
            console.log(
                "Customers:",
                customersResult.value.customers
            );
        }


        // Identify failed APIs
        const failedAPIs = [];


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


        // Show partial failure warning
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


function showLoading() {
    const loading = document.getElementById("loading");

    if (loading) {
        loading.style.display = "block";
    }
}


function hideLoading() {
    const loading = document.getElementById("loading");

    if (loading) {
        loading.style.display = "none";
    }
}


function showError(message) {
    const errorElement = document.getElementById("error");

    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = "block";
    }
}


function hideError() {
    const errorElement = document.getElementById("error");

    if (errorElement) {
        errorElement.style.display = "none";
    }
}


loadDashboard();