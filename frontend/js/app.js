"use strict";

const API_BASE = "/api";

const state = {
    token: null,
    user: null,
    authMode: "login",
    transactions: []
};

const elements = {
    authButton: document.getElementById("auth-button"),
    authDialog: document.getElementById("auth-dialog"),
    authTitle: document.getElementById("auth-title"),
    authForm: document.getElementById("auth-form"),
    authSubmit: document.getElementById("auth-submit"),
    authError: document.getElementById("auth-error"),
    fullNameField: document.getElementById("full-name-field"),
    fullName: document.getElementById("full-name"),
    email: document.getElementById("email"),
    password: document.getElementById("password"),
    closeAuth: document.getElementById("close-auth"),
    pageTitle: document.getElementById("page-title"),
    transactionForm: document.getElementById("transaction-form"),
    transactionResult: document.getElementById("transaction-result"),
    submitTransaction: document.getElementById("submit-transaction"),
    recentTransactions: document.getElementById("recent-transactions"),
    allTransactions: document.getElementById("all-transactions"),
    totalTransactions: document.getElementById("total-transactions"),
    allowedCount: document.getElementById("allowed-count"),
    reviewCount: document.getElementById("review-count"),
    blockedCount: document.getElementById("blocked-count"),
    refreshTransactions: document.getElementById("refresh-transactions"),
    feedbackForm: document.getElementById("feedback-form"),
    feedbackResult: document.getElementById("feedback-result")
};

function showMessage(target, message, type = "success") {
    target.hidden = false;
    target.className = `result-box result-${type}`;
    target.replaceChildren();

    const paragraph = document.createElement("p");
    paragraph.textContent = message;
    target.appendChild(paragraph);
}

function showAuthError(message) {
    elements.authError.textContent = message;
    elements.authError.hidden = false;
}

function clearAuthError() {
    elements.authError.textContent = "";
    elements.authError.hidden = true;
}

async function apiRequest(path, options = {}) {
    const headers = new Headers(options.headers || {});

    if (options.body && !(options.body instanceof FormData)) {
        headers.set("Content-Type", "application/json");
    }

    if (state.token) {
        headers.set("Authorization", `Bearer ${state.token}`);
    }

    const response = await fetch(`${API_BASE}${path}`, {
        ...options,
        headers,
        credentials: "same-origin"
    });

    const contentType = response.headers.get("content-type") || "";
    let data = null;

    if (contentType.includes("application/json")) {
        data = await response.json();
    } else {
        const text = await response.text();
        data = text ? { detail: text } : null;
    }

    if (!response.ok) {
        const error = new Error(
            typeof data?.detail === "string"
                ? data.detail
                : `Request failed with status ${response.status}`
        );

        error.status = response.status;
        throw error;
    }

    return data;
}

function openAuthDialog(mode = "login") {
    setAuthMode(mode);

    if (!elements.authDialog.open) {
        elements.authDialog.showModal();
    }
}

function closeAuthDialog() {
    elements.authDialog.close();
    clearAuthError();
    elements.authForm.reset();
}

function setAuthMode(mode) {
    state.authMode = mode === "register" ? "register" : "login";

    const registering = state.authMode === "register";

    elements.authTitle.textContent = registering
        ? "Create your account"
        : "Sign in";

    elements.authSubmit.textContent = registering
        ? "Create account"
        : "Sign in";

    elements.fullNameField.hidden = !registering;
    elements.fullName.required = registering;
    elements.password.autocomplete = registering
        ? "new-password"
        : "current-password";

    document.querySelectorAll("[data-auth-mode]").forEach(button => {
        const active = button.dataset.authMode === state.authMode;
        button.classList.toggle("active", active);
        button.setAttribute("aria-pressed", String(active));
    });

    clearAuthError();
}

function updateAuthUI() {
    if (state.user) {
        const displayName = state.user.full_name || state.user.email;
        elements.authButton.textContent = "Sign out";
        elements.authButton.title = `Signed in as ${displayName}`;
    } else {
        elements.authButton.textContent = "Sign in";
        elements.authButton.removeAttribute("title");
    }

    elements.submitTransaction.disabled = !state.user;
    elements.submitTransaction.title = state.user
        ? ""
        : "Sign in with a test account before submitting a transaction.";
}

function formatAmount(amount, currency = "NGN") {
    const numericAmount = Number(amount);

    if (!Number.isFinite(numericAmount)) {
        return `${currency} ${String(amount)}`;
    }

    try {
        return new Intl.NumberFormat("en-NG", {
            style: "currency",
            currency,
            maximumFractionDigits: 2
        }).format(numericAmount);
    } catch {
        return `${currency} ${numericAmount.toFixed(2)}`;
    }
}

function normalizeDecision(status) {
    const value = String(status || "").toUpperCase();

    if (value.includes("ALLOW") || value === "APPROVED") {
        return "ALLOW";
    }

    if (value.includes("REVIEW") || value.includes("PENDING")) {
        return "REVIEW";
    }

    if (value.includes("BLOCK") || value.includes("REJECT")) {
        return "BLOCK";
    }

    return value || "UNKNOWN";
}

function statusClass(decision) {
    if (decision === "ALLOW") return "status-allow";
    if (decision === "REVIEW") return "status-review";
    if (decision === "BLOCK") return "status-block";
    return "status-unknown";
}

function createEmptyState(title, description) {
    const wrapper = document.createElement("div");
    wrapper.className = "empty-state";

    const heading = document.createElement("strong");
    heading.textContent = title;

    const paragraph = document.createElement("p");
    paragraph.textContent = description;

    wrapper.append(heading, paragraph);
    return wrapper;
}

function renderTransactionList(container, transactions) {
    container.replaceChildren();

    if (!transactions.length) {
        container.appendChild(
            createEmptyState(
                "No transactions yet",
                "Submit a simulated transaction to see it here."
            )
        );
        return;
    }

    transactions.forEach(transaction => {
        const row = document.createElement("article");
        row.className = "transaction-item";

        const main = document.createElement("div");
        main.className = "transaction-main";

        const beneficiary = document.createElement("div");
        beneficiary.className = "transaction-beneficiary";
        beneficiary.textContent = transaction.beneficiary || "Test beneficiary";

        const meta = document.createElement("div");
        meta.className = "transaction-meta";
        meta.textContent = `Transaction #${transaction.id}`;

        main.append(beneficiary, meta);

        const side = document.createElement("div");
        side.className = "transaction-side";

        const amount = document.createElement("div");
        amount.className = "transaction-amount";
        amount.textContent = formatAmount(
            transaction.amount,
            transaction.currency || "NGN"
        );

        const decision = normalizeDecision(transaction.status);
        const badge = document.createElement("span");
        badge.className = `status-badge ${statusClass(decision)}`;
        badge.textContent = decision;

        side.append(amount, badge);
        row.append(main, side);
        container.appendChild(row);
    });
}

function updateStatistics(transactions) {
    const counts = {
        ALLOW: 0,
        REVIEW: 0,
        BLOCK: 0
    };

    transactions.forEach(transaction => {
        const decision = normalizeDecision(transaction.status);

        if (Object.prototype.hasOwnProperty.call(counts, decision)) {
            counts[decision] += 1;
        }
    });

    elements.totalTransactions.textContent = String(transactions.length);
    elements.allowedCount.textContent = String(counts.ALLOW);
    elements.reviewCount.textContent = String(counts.REVIEW);
    elements.blockedCount.textContent = String(counts.BLOCK);
}

async function loadTransactions() {
    if (!state.user) {
        state.transactions = [];
        updateStatistics([]);
        renderTransactionList(
            elements.recentTransactions,
            []
        );
        renderTransactionList(
            elements.allTransactions,
            []
        );
        return;
    }

    const transactions = await apiRequest("/transactions");

    if (!Array.isArray(transactions)) {
        throw new Error("The server returned an unexpected transaction response.");
    }

    state.transactions = transactions;

    updateStatistics(transactions);
    renderTransactionList(
        elements.recentTransactions,
        transactions.slice(0, 5)
    );
    renderTransactionList(
        elements.allTransactions,
        transactions
    );
}

async function loadCurrentUser() {
    const user = await apiRequest("/auth/me");
    state.user = user;
    updateAuthUI();
    await loadTransactions();
}

function clearSession() {
    state.token = null;
    state.user = null;
    state.transactions = [];

    updateAuthUI();
    updateStatistics([]);

    renderTransactionList(
        elements.recentTransactions,
        []
    );

    renderTransactionList(
        elements.allTransactions,
        []
    );
}

async function handleAuthentication(event) {
    event.preventDefault();
    clearAuthError();

    const registering = state.authMode === "register";
    const email = elements.email.value.trim();
    const password = elements.password.value;

    elements.authSubmit.disabled = true;

    try {
        if (registering) {
            const fullName = elements.fullName.value.trim();

            await apiRequest("/users", {
                method: "POST",
                body: JSON.stringify({
                    email,
                    full_name: fullName,
                    password
                })
            });
        }

        const formData = new URLSearchParams();
        formData.set("username", email);
        formData.set("password", password);

        const tokenResponse = await apiRequest("/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: formData.toString()
        });

        if (!tokenResponse?.access_token) {
            throw new Error("The server did not return an access token.");
        }

        state.token = tokenResponse.access_token;

        await loadCurrentUser();

        closeAuthDialog();

        showMessage(
            elements.transactionResult,
            `Welcome${state.user.full_name ? `, ${state.user.full_name}` : ""}. You are signed in.`,
            "success"
        );
    } catch (error) {
        state.token = null;
        state.user = null;
        updateAuthUI();

        let message = error.message || "Authentication failed.";

        if (error.status === 401) {
            message = "We couldn't sign you in. Check your email and password.";
        } else if (error.status === 409) {
            message = "An account with this email already exists. Please sign in.";
        } else if (error.status === 422) {
            message = "Some information is invalid. Check the form and try again.";
        } else if (error.status === 403) {
            message = "This account cannot access the requested resource.";
        } else if (!error.status) {
            message = "Unable to reach SecureFlow. Check that the frontend and backend are running.";
        }

        showAuthError(message);
    } finally {
        elements.authSubmit.disabled = false;
    }
}

async function handleTransactionSubmission(event) {
    event.preventDefault();

    if (!state.user || !state.token) {
        openAuthDialog("login");
        return;
    }

    const formData = new FormData(elements.transactionForm);
    const amount = Number(formData.get("amount"));
    const currency = String(formData.get("currency") || "NGN");
    const beneficiary = String(formData.get("beneficiary") || "").trim();

    if (!Number.isFinite(amount) || amount <= 0) {
        showMessage(
            elements.transactionResult,
            "Enter a valid transaction amount greater than zero.",
            "error"
        );
        return;
    }

    if (!beneficiary) {
        showMessage(
            elements.transactionResult,
            "Enter a test beneficiary.",
            "error"
        );
        return;
    }

    elements.submitTransaction.disabled = true;
    elements.submitTransaction.textContent = "Assessing transaction...";

    try {
        const transaction = await apiRequest("/transactions", {
            method: "POST",
            body: JSON.stringify({
                amount,
                currency,
                beneficiary
            })
        });

        const decision = normalizeDecision(transaction.status);

        showMessage(
            elements.transactionResult,
            `Transaction #${transaction.id} was submitted. Current risk decision: ${decision}. This is a simulated decision from the project's risk rules.`,
            decision === "BLOCK"
                ? "error"
                : decision === "REVIEW"
                    ? "warning"
                    : "success"
        );

        elements.transactionForm.reset();
        await loadTransactions();
    } catch (error) {
        let message = error.message || "Transaction submission failed.";

        if (error.status === 401) {
            clearSession();
            message = "Your session is no longer valid. Please sign in again.";
            openAuthDialog("login");
        } else if (error.status === 403) {
            message = "Your account is not permitted to submit this transaction.";
        } else if (error.status === 422) {
            message = "The transaction details were rejected. Check the amount, currency, and beneficiary.";
        } else if (!error.status) {
            message = "Unable to reach SecureFlow. Check that the application is running.";
        }

        showMessage(elements.transactionResult, message, "error");
    } finally {
        elements.submitTransaction.innerHTML = 'Assess transaction <span>→</span>';
        updateAuthUI();
    }
}

function showView(viewName) {
    const validViews = ["overview", "transactions", "feedback"];
    const view = validViews.includes(viewName) ? viewName : "overview";

    document.querySelectorAll(".view").forEach(section => {
        section.hidden = section.id !== `${view}-view`;
    });

    document.querySelectorAll("[data-view]").forEach(link => {
        const active = link.dataset.view === view;
        link.classList.toggle("active", active);

        if (active) {
            link.setAttribute("aria-current", "page");
        } else {
            link.removeAttribute("aria-current");
        }
    });

    const titles = {
        overview: "Overview",
        transactions: "Transactions",
        feedback: "Feedback"
    };

    elements.pageTitle.textContent = titles[view];

    if (view === "transactions" && state.user) {
        loadTransactions().catch(error => {
            showMessage(
                elements.allTransactions,
                error.message || "Could not load transactions.",
                "error"
            );
        });
    }
}

function handleFeedbackSubmission(event) {
    event.preventDefault();

    showMessage(
        elements.feedbackResult,
        "Feedback submission is not connected yet. We will enable it after adding and testing a feedback endpoint in the backend. Your feedback has not been sent or saved.",
        "warning"
    );
}

function attachEventListeners() {
    elements.authButton.addEventListener("click", () => {
        if (state.user) {
            clearSession();
            elements.transactionResult.hidden = true;
        } else {
            openAuthDialog("login");
        }
    });

    elements.closeAuth.addEventListener("click", closeAuthDialog);

    elements.authDialog.addEventListener("click", event => {
        if (event.target === elements.authDialog) {
            closeAuthDialog();
        }
    });

    document.querySelectorAll("[data-auth-mode]").forEach(button => {
        button.addEventListener("click", () => {
            setAuthMode(button.dataset.authMode);
        });
    });

    elements.authForm.addEventListener("submit", handleAuthentication);
    elements.transactionForm.addEventListener(
        "submit",
        handleTransactionSubmission
    );

    elements.refreshTransactions.addEventListener("click", async () => {
        elements.refreshTransactions.disabled = true;

        try {
            await loadTransactions();
        } catch (error) {
            showMessage(
                elements.allTransactions,
                error.message || "Could not refresh transactions.",
                "error"
            );
        } finally {
            elements.refreshTransactions.disabled = false;
        }
    });

    elements.feedbackForm.addEventListener(
        "submit",
        handleFeedbackSubmission
    );

    document.querySelectorAll("[data-view]").forEach(link => {
        link.addEventListener("click", event => {
            event.preventDefault();
            const view = link.dataset.view;
            showView(view);
            history.replaceState(null, "", `#${view}`);
        });
    });
}

function initialize() {
    attachEventListeners();
    updateAuthUI();
    updateStatistics([]);

    renderTransactionList(elements.recentTransactions, []);
    renderTransactionList(elements.allTransactions, []);

    showView(window.location.hash.slice(1) || "overview");

    // Tokens remain in memory only; refreshing the page signs the user out.
    // This avoids persisting bearer tokens in localStorage or sessionStorage.
}

initialize();
