function getCookie(name) {
    const cookies = document.cookie.split("; ");
    for (const cookie of cookies) {
        const [key, value] = cookie.split("=");
        if (key === name) {
            return JSON.parse(decodeURIComponent(value));
        }
    }
    return null;
}

const salaryAdvanceData = getCookie("SalaryAdvanceData");

if (salaryAdvanceData) {
    console.log("Retrieved data from cookie:", salaryAdvanceData);
    document.getElementById("total").textContent = salaryAdvanceData.amount || "0.00";
    document.getElementById("tenor").textContent = salaryAdvanceData.tenor || "0";
    document.getElementById("reason").textContent = salaryAdvanceData.reason || "No reason provided.";
    document.getElementById("monthly_payment").textContent = salaryAdvanceData.amount / salaryAdvanceData.tenor;
} else {
    console.log("No SalaryAdvanceData cookie found.");
}
