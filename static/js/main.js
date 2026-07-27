// ===============================
// DiseasePred Clean main.js
// ===============================

// Health Tips
const TIPS = {
    diabetes: {
        positive: ["Monitor blood sugar regularly", "Exercise daily", "Reduce sugar intake"],
        negative: ["Maintain healthy diet", "Regular health checkups"]
    },
    heart: {
        positive: ["Consult cardiologist", "Reduce salt intake", "Exercise regularly"],
        negative: ["Maintain healthy weight", "Avoid smoking"]
    },
    parkinsons: {
        positive: ["Consult neurologist", "Physical therapy recommended"],
        negative: ["Maintain brain activity", "Exercise regularly"]
    },
    lung: {
        positive: ["Consult pulmonologist", "Stop smoking immediately"],
        negative: ["Avoid smoking", "Maintain lung health"]
    },
    kidney: {
        positive: ["Consult nephrologist", "Reduce salt intake", "Drink proper water"],
        negative: ["Maintain healthy diet", "Avoid excessive salt"]
    }
};

function saveToHistory(disease, label, prediction, confidence) {

    let history = JSON.parse(localStorage.getItem("prediction_history")) || [];

    history.push({
        disease: disease,
        label: label,
        prediction: prediction,
        confidence: confidence,
        time: new Date().toLocaleString()
    });

    localStorage.setItem("prediction_history", JSON.stringify(history));
}
// ===============================
// Helper function
// ===============================

function getPayload() {

    const inputs = document.querySelectorAll("input, select");
    let data = {};

    inputs.forEach(el => {
        let v = el.value;

        if (v === "Yes") v = 1;
        if (v === "No") v = 0;
        if (v === "Male") v = 1;
        if (v === "Female") v = 0;

        if (el.id === "patient_name") {
            data["patient_name"] = v;
        } else {
            data[el.id.toLowerCase()] = Number(v) || 0;
        }
    });

    return data;
}

// ===============================
// Show Tips
// ===============================

function showTips(disease, isPositive) {

    const tipsBox = document.getElementById("health-tips");
    const tipsList = document.getElementById("tips-list");

    if (!tipsBox || !tipsList) return;

    let tips = TIPS[disease][isPositive ? "positive" : "negative"];

    tipsList.innerHTML = tips.map(t => `<li>${t}</li>`).join("");

    tipsBox.style.display = "block";
}

// ===============================
// Risk Meter
// ===============================

function showRiskMeter(confidence, isPositive) {

    const meter = document.getElementById("risk-meter");
    const fill = document.getElementById("risk-fill");
    const label = document.getElementById("risk-label");

    if (!meter) return;

    meter.style.display = "block";

    fill.className = "risk-fill " + (isPositive ? "high" : "low");
    fill.style.width = confidence + "%";

    label.textContent = confidence + "% Confidence";
}



// ===============================
// Prediction
// ===============================

async function predict(disease) {

    const resultBox = document.getElementById("result");

    resultBox.style.display = "none";

    try {

        const res = await fetch(`/predict/${disease}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(getPayload())
        });

        const data = await res.json();

        if (data.error) {

            resultBox.className = "result-box positive";
            resultBox.innerHTML = `<h3>⚠️ Error</h3><p>${data.error}</p>`;
            resultBox.style.display = "block";
            return;

        }

        let positive = data.prediction === 1;

        saveToHistory(disease, data.label, data.prediction, data.confidence);

        resultBox.className = `result-box ${positive?"positive":"negative"}`;

        resultBox.innerHTML = `
<h3>${positive?"⚠️":"✅"} ${data.label}</h3>
<p>Confidence Score: <strong>${data.confidence}%</strong></p>
<h3 style="margin-top:10px; color:${positive ? 'red' : 'green'};">
    ${data.advice}
</h3>
`;

        resultBox.style.display = "block";

        showRiskMeter(data.confidence, positive);
        showTips(disease, positive);

        resultBox.scrollIntoView({ behavior: "smooth" });

    } catch (err) {

        console.log(err);

        resultBox.className = "result-box positive";

        resultBox.innerHTML = `
<h3>⚠️ Connection Error</h3>
<p>Flask server not responding.</p>
`;

        resultBox.style.display = "block";

    }

}

function toggleSymptom(el) {

    // toggle checked class
    el.classList.toggle("checked");

    // show check mark
    const check = el.querySelector(".sym-check");

    if (check) {
        check.textContent = el.classList.contains("checked") ? "✓" : "";
    }

    // update count automatically
    const panel = el.closest(".checker-panel");
    const count = panel.querySelectorAll(".symptom-item.checked").length;

    const counter = panel.querySelector(".checker-count");

    if (counter) {
        counter.textContent = count + " symptoms selected";
    }

}

function updateCheckerCount(disease) {

    const panel = document.getElementById("panel-" + disease);

    const count = panel.querySelectorAll(".symptom-item.checked").length;

    const counter = panel.querySelector(".checker-count");

    if (counter) {
        counter.textContent = count + " symptoms selected";
    }

}

function runChecker(disease) {

    const panel = document.getElementById("panel-" + disease);

    const total = panel.querySelectorAll(".symptom-item").length;
    const checked = panel.querySelectorAll(".symptom-item.checked").length;

    const result = panel.querySelector(".checker-result");

    if (!result) return;

    if (checked === 0) {

        result.innerHTML = `
<p>Please select at least one symptom.</p>
`;

    } else if (checked < 4) {

        result.innerHTML = `
<div style="
background:#fff8e1;
border:1px solid #f6c343;
padding:20px;
border-radius:12px;
margin-top:20px;
">

<h4>🟡 Low symptom match</h4>

<p>You selected ${checked} out of ${total} symptoms. The likelihood appears low.</p>

<a href="/${disease}" style="
display:inline-block;
margin-top:12px;
background:#1e73be;
color:white;
padding:10px 18px;
border-radius:8px;
text-decoration:none;
font-weight:500;
">
Go to ${disease.charAt(0).toUpperCase()+disease.slice(1)} Predictor →
</a>

</div>
`;

    } else if (checked < 8) {

        result.innerHTML = `
<div style="
background:#fff3cd;
border:1px solid #ff9800;
padding:20px;
border-radius:12px;
margin-top:20px;
">

<h4>🟠 Moderate symptom match</h4>

<p>You selected ${checked} out of ${total} symptoms. The risk level is moderate.</p>

<p>Consider running the full AI prediction tool.</p>

<a href="/${disease}" style="
display:inline-block;
margin-top:12px;
background:#1e73be;
color:white;
padding:10px 18px;
border-radius:8px;
text-decoration:none;
font-weight:500;
">
Go to ${disease.charAt(0).toUpperCase()+disease.slice(1)} Predictor →
</a>

</div>
`;

    } else {

        result.innerHTML = `
<div style="
background:#fdecea;
border:1px solid #f44336;
padding:20px;
border-radius:12px;
margin-top:20px;
">

<h4>🔴 High symptom match</h4>

<p>You selected ${checked} out of ${total} symptoms. Please use the prediction tool and consult a doctor soon.</p>

<a href="/${disease}" style="
display:inline-block;
margin-top:12px;
background:#1e73be;
color:white;
padding:10px 18px;
border-radius:8px;
text-decoration:none;
font-weight:500;
">
Go to ${disease.charAt(0).toUpperCase()+disease.slice(1)} Predictor →
</a>

</div>
`;

    }

    result.style.display = "block";
}

function clearChecker(disease) {

    const panel = document.getElementById("panel-" + disease);

    panel.querySelectorAll(".symptom-item").forEach(el => {
        el.classList.remove("checked");

        const c = el.querySelector(".sym-check");
        if (c) c.textContent = "";
    });

    const result = panel.querySelector(".checker-result");
    if (result) result.innerHTML = "";

    const counter = panel.querySelector(".checker-count");
    if (counter) counter.textContent = "0 symptoms selected";

}

function switchTab(tab) {

    document.querySelectorAll(".checker-tab").forEach(t => {
        t.classList.remove("active");
    });

    document.querySelectorAll(".checker-panel").forEach(p => {
        p.classList.remove("active");
    });

    document.querySelector(`[data-tab="${tab}"]`).classList.add("active");

    document.getElementById("panel-" + tab).classList.add("active");

}

function saveToHistory(disease, label, prediction, confidence) {

    let history = JSON.parse(localStorage.getItem("prediction_history")) || [];

    history.push({
        disease: disease,
        label: label,
        prediction: prediction,
        confidence: confidence,
        time: new Date().toLocaleString()
    });

    localStorage.setItem("prediction_history", JSON.stringify(history));

    console.log("History Saved:", history);

}